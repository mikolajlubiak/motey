from aiohttp import web
import aiohttp_session
import aiohttp_csrf
from motey.config import Config


def _create_error_middleware(overrides):
    @web.middleware
    async def error_middleware(request, handler):
        try:
            return await handler(request)
        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request)

            raise
        except Exception:
            request.protocol.logger.exception("Error handling request")
            return await overrides[500](request)

    return error_middleware


@web.middleware
async def check_login(request, handler):
    session = await aiohttp_session.get_session(request)
    discord_id = session.get("discord_id")

    if not discord_id:
        url = Config.auth_start_url
        raise web.HTTPFound(location=url)

    return await handler(request)


def setup_middlewares(app: web.Application) -> None:
    app.middlewares.append(aiohttp_csrf.csrf_middleware)
    app.middlewares.append(check_login)
