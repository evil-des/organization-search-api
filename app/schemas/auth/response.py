from enums.token import TokenType
from schemas.base import ResponseModel


class TokenResponseSchema(ResponseModel):
    access_token: str
    token_type: TokenType
    expires_at: int
