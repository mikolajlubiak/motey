from aiohttp import web
from aiomysql.sa import create_engine
import aiohttp_jinja2
import jinja2

from motey.infrastructure.config import Config
from motey.infrastructure.http.middleware import (
    create_error_middleware,
    handle_404,
    handle_500)


async def _attach_database_context(app: web.Application,
                                   config: Config = Config()):
    engine = await create_engine(
        user=config.database_user, db=config.database,
        host=config.database_host, port=config.database_port,
        password=config.database_password)
    app['db'] = engine

    yield

    app['db'].close()
    await app['db'].wait_closed()


def _build_jinja_loader(config: Config = Config()) -> jinja2.FileSystemLoader:
    return jinja2.FileSystemLoader(str(config.templates_dir))


def _setup_middlewares(app: web.Application) -> None:
    error_middleware = create_error_middleware({
        404: handle_404,
        500: handle_500
    })
    app.middlewares.append(error_middleware)


def run_app(config: Config = Config()) -> None:
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=_build_jinja_loader())
    _setup_middlewares(app)
    app.cleanup_ctx.append(_attach_database_context)
    web.run_app(app, host=config.http_host, port=config.http_port)
