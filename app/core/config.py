from pydantic import SecretStr
from pydantic_settings import BaseSettings


class CoreSettings(BaseSettings):
    DEBUG: bool = False
    BACKEND_PORT: int = 5000

    JWT_KEY: SecretStr


core_settings = CoreSettings()
