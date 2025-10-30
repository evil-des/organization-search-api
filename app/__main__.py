import asyncio

import uvicorn

from core.config import core_settings


async def main():
    config = uvicorn.Config(
        "asgi.app:create_app",
        host="0.0.0.0",
        port=core_settings.BACKEND_PORT,
        factory=True,
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
