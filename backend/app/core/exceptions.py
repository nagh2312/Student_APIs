"""Application exceptions mapped to standard error responses."""

from __future__ import annotations


class AppError(Exception):
    def __init__(
        self,
        message: str,
        *,
        code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details=None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, message: str = "Resource not found", details=None):
        super().__init__(
            message,
            code="RESOURCE_NOT_FOUND",
            status_code=404,
            details=details,
        )


class ValidationAppError(AppError):
    def __init__(self, message: str, details=None):
        super().__init__(
            message,
            code="VALIDATION_ERROR",
            status_code=400,
            details=details,
        )


class ProviderError(AppError):
    def __init__(self, message: str = "Upstream provider error", details=None):
        super().__init__(
            message,
            code="PROVIDER_ERROR",
            status_code=503,
            details=details,
        )
