"""Validate scripts placeholder — extend per dataset."""

from app.modules.universities.mock_data import MOCK_UNIVERSITIES


def validate_universities() -> None:
    assert all("id" in u and "name" in u for u in MOCK_UNIVERSITIES)
    print(f"OK: {len(MOCK_UNIVERSITIES)} mock universities")


if __name__ == "__main__":
    validate_universities()
