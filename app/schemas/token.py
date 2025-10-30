from datetime import UTC, datetime
import secrets

from pydantic import BaseModel, Field, field_serializer

from core.security.globals import TOKEN_EXPIRES_IN
from enums.token import TokenType


class TokenSchema(BaseModel):
    type: TokenType = TokenType.access
    sub: str = Field(default_factory=lambda: secrets.token_urlsafe(16))
    expires_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC) + TOKEN_EXPIRES_IN,
    )

    @field_serializer("expires_at")
    def serialize_expires_at(self, expires_at: datetime) -> int:
        return int(expires_at.timestamp())
