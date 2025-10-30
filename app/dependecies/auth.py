from typing import Annotated

from fastapi import Depends, Security

from core.security.token import get_token
from schemas.token import TokenSchema
from services.auth import AuthService

AuthServiceDependency = Annotated[
    AuthService,
    Depends(AuthService.get_service),
]

CurrentTokenDependency = Annotated[
    TokenSchema,
    Security(get_token),
]

TokenSecurityDependency = Security(get_token)
