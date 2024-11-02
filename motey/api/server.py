import logging

from aiohttp import web
import aiohttp_session
import aiohttp_csrf
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from motey.config import Config
from motey.database.engine import get_db
from motey.api.middleware import setup_middlewares
from motey.api.routing import setup_routes


async def _attach_database_context(app: web.Application):
    engine = get_db()
    app["db"] = engine
    yield


def prepare_app(config: Config = Config()) -> web.Application:
    app = web.Application()

    csrf_policy = aiohttp_csrf.policy.FormPolicy(config.form_field_name)
    csrf_storage = aiohttp_csrf.storage.CookieStorage(
        config.cookie_name, secret_phrase=config.secret_phrase
    )
    aiohttp_csrf.setup(app, policy=csrf_policy, storage=csrf_storage)

    setup_routes(app)

    aiohttp_session.setup(app, EncryptedCookieStorage(config.cookie_encryption_key))

    setup_middlewares(app)

    app.cleanup_ctx.append(_attach_database_context)

    logging.basicConfig(level=logging.DEBUG)

    return app


def run_app(config: Config = Config()):
    app = prepare_app()
    web.run_app(app, host=config.http_host, port=config.http_port)
