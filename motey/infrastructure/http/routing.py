from aiohttp.web import Application

from motey.infrastructure.http.views import list_emotes, index, upload, login, show_login_page, register
from motey.infrastructure.config import Config


def setup_routes(app: Application, config: Config = Config()) -> None:
    app.router.add_static(str(config.emotes_dir), config.emotes_dir)
    app.router.add_get('/list', list_emotes)
    app.router.add_get('/', index)
    app.router.add_post('/upload', upload)
    app.router.add_post('/login', login)
    app.router.add_get('/login', show_login_page)
    app.router.add_post('/register', register)
