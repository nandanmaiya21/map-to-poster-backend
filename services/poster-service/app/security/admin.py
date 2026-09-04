import os

from fastapi import (
    Header,
    HTTPException,
    status,
)


ADMIN_API_KEY = os.getenv(
    "ADMIN_API_KEY"
)


def require_admin(
    x_admin_key: str | None = Header(
        default=None,
    ),
):
    """
    Require a valid admin API key.
    """

    if not ADMIN_API_KEY:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Admin authentication is not configured",
        )

    if not x_admin_key:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin API key is required",
        )

    if x_admin_key != ADMIN_API_KEY:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin API key",
        )

    return True