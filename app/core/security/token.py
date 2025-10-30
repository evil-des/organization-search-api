from datetime import datetime, UTC
from typing import Optional

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from jose import jwt
from starlette import status

from core.config import core_settings
from core.security.globals import HEADER_TOKEN_KEY
from schemas.token import TokenSchema


def create_jwt_token(data: dict) -> str:
    return jwt.encode(
        data,
        core_settings.JWT_KEY.get_secret_value(),
        algorithm="HS256",
    )


def parse_jwt_token(token: str) -> TokenSchema:
    data = jwt.decode(
        token,
        core_settings.JWT_KEY.get_secret_value(),
        algorithms=['HS256'],
    )
    return TokenSchema.model_validate(data)


def issue_token(subject: Optional[str] = None) -> tuple[str, TokenSchema]:
    payload = TokenSchema()
    if subject:
        payload.sub = subject
    token = create_jwt_token(payload.model_dump(mode="json"))
    return token, payload


async def get_token(
        access_token: Optional[str] = Security(
            APIKeyHeader(name=HEADER_TOKEN_KEY, auto_error=False),
        )
) -> TokenSchema:
    if not access_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    token = parse_jwt_token(access_token)
    if token.expires_at <= datetime.now(UTC):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token
