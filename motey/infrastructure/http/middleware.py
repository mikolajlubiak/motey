import aiohttp_jinja2
from aiohttp import web
import aiohttp_session
from motey.infrastructure.config import Config


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


async def handle_404(request):
    return aiohttp_jinja2.render_template('404.html', request, {}, status=404)


async def handle_500(request):
    return aiohttp_jinja2.render_template('500.html', request, {}, status=500)


@web.middleware
async def check_login(request, handler):
    if request.path == '/upload':
        session = await aiohttp_session.get_session(request)
        discord_id = session.get("discord_id")
        if not discord_id:
            url = Config.auth_start_url
            raise web.HTTPFound(location=url)
    return await handler(request)


def setup_middlewares(app: web.Application) -> None:
    error_middleware = _create_error_middleware({
        404: handle_404,
        500: handle_500
    })
    app.middlewares.append(error_middleware)
    app.middlewares.append(check_login)
