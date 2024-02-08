from aiohttp import web
import aiohttp_jinja2
import jinja2
import aiohttp_session
import aiohttp_csrf
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import logging


from motey.config import Config
from motey.database.engine import get_db
from motey.http.middleware import setup_middlewares
from motey.http.routing import setup_routes


async def _attach_database_context(app: web.Application):
    engine = get_db()
    app["db"] = engine
    yield


def _build_jinja_loader(config: Config = Config()) -> jinja2.FileSystemLoader:
    return jinja2.FileSystemLoader(str(config.templates_dir))


def prepare_app(config: Config = Config()) -> web.Application:
    app = web.Application()
    csrf_policy = aiohttp_csrf.policy.FormPolicy(config.form_field_name)
    csrf_storage = aiohttp_csrf.storage.CookieStorage(
        config.cookie_name, secret_phrase=config.secret_phrase
    )
    aiohttp_csrf.setup(app, policy=csrf_policy, storage=csrf_storage)
    aiohttp_jinja2.setup(app, loader=_build_jinja_loader())
    setup_routes(app)
    aiohttp_session.setup(app, EncryptedCookieStorage(config.cookie_encryption_key))
    setup_middlewares(app)
    app.cleanup_ctx.append(_attach_database_context)
    logging.basicConfig(level=logging.DEBUG)
    return app


def run_app(config: Config = Config()):
    app = prepare_app()
    web.run_app(app, host=config.http_host, port=config.http_port)
