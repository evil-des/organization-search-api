from fastapi import APIRouter

from dependecies.auth import AuthServiceDependency
from schemas.auth import TokenResponseSchema

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenResponseSchema)
async def issue_token(
    auth_service: AuthServiceDependency,
) -> TokenResponseSchema:
    return await auth_service.issue_token()
