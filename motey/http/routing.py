from aiohttp.web import Application
from aiohttp import web
from motey.config import Config

from motey.http.views import list_emotes, index, process_oauth, process_upload, upload


def setup_routes(app: Application, config: Config = Config()) -> None:
    app.router.add_static(str(config.emotes_dir), config.emotes_dir)
    app.router.add_get('/list', list_emotes)
    app.router.add_get('/', index)
    app.router.add_post('/upload', process_upload)
    app.router.add_get('/upload', upload)
    app.router.add_get('/process_oauth', process_oauth)
    app.router.add_static('/static/', path=(config.static_files_dir), name='static')
    app.router.add_get('/login', lambda _: web.HTTPFound(location=config.auth_start_url))
