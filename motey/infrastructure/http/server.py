from aiohttp import web
import aiohttp_jinja2
import jinja2
import aiohttp_session

from motey.infrastructure.config import Config
from motey.infrastructure.database.engine import get_db
from motey.infrastructure.http.middleware import setup_middlewares
from motey.infrastructure.http.routing import setup_routes


async def _attach_database_context(app: web.Application):
    engine = get_db()
    app['db'] = engine
    yield


def _build_jinja_loader(config: Config = Config()) -> jinja2.FileSystemLoader:
    return jinja2.FileSystemLoader(str(config.templates_dir))


def run_app(config: Config = Config()) -> None:
    app = web.Application(client_max_size=16780000)
    aiohttp_jinja2.setup(app, loader=_build_jinja_loader())
    setup_routes(app)
    setup_middlewares(app)
    aiohttp_session.setup(app, aiohttp_session.SimpleCookieStorage())
    app.cleanup_ctx.append(_attach_database_context)
    web.run_app(app, host=config.http_host, port=config.http_port)
