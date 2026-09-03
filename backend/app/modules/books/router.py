"""Books API with Open Library + mock providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel, Field

from app.core.config import get_settings
from app.core.dependencies import optional_api_key
from app.core.exceptions import NotFoundError, ProviderError
from app.core.responses import clamp_pagination, success
from app.data import books as load_books

router = APIRouter(prefix="/books", tags=["Books"])


class BookOut(BaseModel):
    id: str
    title: str
    authors: list[str] = Field(default_factory=list)
    isbn: str | None = None
    isbn13: str | None = None
    publisher: str | None = None
    publish_date: str | None = None
    categories: list[str] = Field(default_factory=list)
    language: str | None = None
    description: str | None = None
    cover_url: str | None = None
    source: str = "mock"


MOCK_BOOKS: list[dict] = load_books()


class BooksProvider(ABC):
    @abstractmethod
    async def search(
        self,
        *,
        q: str | None,
        title: str | None,
        author: str | None,
        page: int,
        limit: int,
    ) -> tuple[list[BookOut], int]:
        ...

    @abstractmethod
    async def get(self, book_id: str) -> BookOut:
        ...

    @abstractmethod
    async def by_isbn(self, isbn: str) -> BookOut:
        ...


class MockBooksProvider(BooksProvider):
    async def search(self, *, q, title, author, page, limit):
        items = list(MOCK_BOOKS)
        if q:
            n = q.lower()
            items = [
                b
                for b in items
                if n in b["title"].lower()
                or any(n in a.lower() for a in b["authors"])
                or n in (b.get("isbn") or "")
            ]
        if title:
            n = title.lower()
            items = [b for b in items if n in b["title"].lower()]
        if author:
            n = author.lower()
            items = [b for b in items if any(n in a.lower() for a in b["authors"])]
        total = len(items)
        start = (page - 1) * limit
        return [BookOut.model_validate(b) for b in items[start : start + limit]], total

    async def get(self, book_id: str) -> BookOut:
        for b in MOCK_BOOKS:
            if b["id"] == book_id:
                return BookOut.model_validate(b)
        raise NotFoundError(f"Book '{book_id}' not found")

    async def by_isbn(self, isbn: str) -> BookOut:
        clean = isbn.replace("-", "")
        for b in MOCK_BOOKS:
            if (b.get("isbn") or "").replace("-", "") == clean or (
                b.get("isbn13") or ""
            ).replace("-", "") == clean:
                return BookOut.model_validate(b)
        raise NotFoundError(f"Book with ISBN '{isbn}' not found")


class OpenLibraryProvider(BooksProvider):
    async def search(self, *, q, title, author, page, limit):
        params: dict = {"page": page, "limit": limit}
        if q:
            params["q"] = q
        if title:
            params["title"] = title
        if author:
            params["author"] = author
        if not any([q, title, author]):
            params["q"] = "programming"
        async with httpx.AsyncClient(timeout=20.0) as client:
            try:
                r = await client.get("https://openlibrary.org/search.json", params=params)
                r.raise_for_status()
                data = r.json()
            except httpx.HTTPError as exc:
                raise ProviderError("Open Library search failed") from exc
        docs = data.get("docs") or []
        total = int(data.get("numFound") or len(docs))
        books = [self._from_doc(d) for d in docs[:limit]]
        return books, total

    async def get(self, book_id: str) -> BookOut:
        # Accept OL work keys like OL45804W or our ol- prefixed mock-style IDs
        key = book_id if book_id.startswith("OL") else book_id
        path = key if key.startswith("/") else f"/works/{key}"
        if not path.startswith("/works"):
            path = f"/works/{key}"
        async with httpx.AsyncClient(timeout=20.0) as client:
            try:
                r = await client.get(f"https://openlibrary.org{path}.json")
                if r.status_code == 404:
                    raise NotFoundError(f"Book '{book_id}' not found")
                r.raise_for_status()
                data = r.json()
            except NotFoundError:
                raise
            except httpx.HTTPError as exc:
                raise ProviderError("Open Library lookup failed") from exc
        return BookOut(
            id=book_id,
            title=data.get("title") or "Unknown",
            authors=[],
            description=_extract_desc(data.get("description")),
            categories=[c.get("key", "").split("/")[-1] for c in (data.get("subjects") or [])[:5]
            if isinstance(c, dict)],
            language=None,
            source="openlibrary",
        )

    async def by_isbn(self, isbn: str) -> BookOut:
        clean = isbn.replace("-", "")
        async with httpx.AsyncClient(timeout=20.0) as client:
            try:
                r = await client.get(
                    f"https://openlibrary.org/isbn/{clean}.json",
                    follow_redirects=True,
                )
                if r.status_code == 404:
                    raise NotFoundError(f"Book with ISBN '{isbn}' not found")
                r.raise_for_status()
                data = r.json()
            except NotFoundError:
                raise
            except httpx.HTTPError as exc:
                raise ProviderError("Open Library ISBN lookup failed") from exc
        return BookOut(
            id=data.get("key", clean).split("/")[-1],
            title=data.get("title") or "Unknown",
            authors=[],
            isbn=clean if len(clean) == 10 else None,
            isbn13=clean if len(clean) == 13 else None,
            publisher=(data.get("publishers") or [None])[0],
            publish_date=data.get("publish_date"),
            cover_url=f"https://covers.openlibrary.org/b/isbn/{clean}-M.jpg",
            source="openlibrary",
        )

    @staticmethod
    def _from_doc(doc: dict) -> BookOut:
        cover_id = doc.get("cover_i")
        return BookOut(
            id=doc.get("key", "").split("/")[-1] or doc.get("edition_key", ["unknown"])[0],
            title=doc.get("title") or "Unknown",
            authors=doc.get("author_name") or [],
            isbn=(doc.get("isbn") or [None])[0],
            publisher=(doc.get("publisher") or [None])[0],
            publish_date=str(doc.get("first_publish_year") or ""),
            categories=doc.get("subject") or [],
            language=(doc.get("language") or [None])[0],
            cover_url=(
                f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else None
            ),
            source="openlibrary",
        )


def _extract_desc(desc) -> str | None:
    if isinstance(desc, str):
        return desc
    if isinstance(desc, dict):
        return desc.get("value")
    return None


def get_books_provider() -> BooksProvider:
    s = get_settings()
    if s.mock_mode or s.books_provider == "mock":
        return MockBooksProvider()
    return OpenLibraryProvider()


@router.get("", summary="List / search books")
@router.get("/search", summary="Search books")
async def search_books(
    request: Request,
    q: str | None = None,
    title: str | None = None,
    author: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    page, limit = clamp_pagination(page, limit)
    data, total = await get_books_provider().search(
        q=q, title=title, author=author, page=page, limit=limit
    )
    return success(
        [b.model_dump() for b in data],
        request_id=getattr(request.state, "request_id", None),
        page=page,
        limit=limit,
        total=total,
    )


@router.get("/isbn/{isbn}", summary="Get book by ISBN")
async def book_by_isbn(
    isbn: str,
    request: Request,
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    book = await get_books_provider().by_isbn(isbn)
    return success(book.model_dump(), request_id=getattr(request.state, "request_id", None))


@router.get("/{book_id}", summary="Get book by ID")
async def get_book(
    book_id: str,
    request: Request,
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    book = await get_books_provider().get(book_id)
    return success(book.model_dump(), request_id=getattr(request.state, "request_id", None))
