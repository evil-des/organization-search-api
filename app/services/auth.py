from core.security.token import issue_token
from schemas.auth import TokenResponseSchema
from services.base import BaseService


class AuthService(BaseService):
    async def issue_token(self) -> TokenResponseSchema:
        token, payload = issue_token()
        return TokenResponseSchema(
            access_token=token,
            token_type=payload.type,
            expires_at=int(payload.expires_at.timestamp()),
        )

    @classmethod
    def get_service(cls) -> "AuthService":
        return cls()
