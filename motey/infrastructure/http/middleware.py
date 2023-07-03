import aiohttp_jinja2
from aiohttp import web

from motey.infrastructure.database import tables
from motey.infrastructure.database.tables import users

from sqlalchemy import select


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
async def session_is_valid(request):
    session_id = request.cookies.get('session_id')
    if session_id:
        statement = select(users)\
            .where(session_id==session_id)
        if not connection.scalars(statement).all():
            return {'error_message': 'Invalid session id.'}



def setup_middlewares(app: web.Application) -> None:
    error_middleware = _create_error_middleware({
        404: handle_404,
        500: handle_500
    })
    app.middlewares.append(error_middleware)
    app.middlewares.append(session_is_valid)
