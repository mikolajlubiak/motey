from aiohttp.web import Application
from motey.config import Config

from motey.api.endpoints import (
    get_emote_list,
    get_server_list,
    get_csrf_token,
    process_oauth,
    process_upload,
)


def setup_routes(app: Application, config: Config = Config()) -> None:
    app.router.add_get("/api/v1/get_emote_list", get_emote_list)
    app.router.add_get("/api/v1/get_server_list", get_server_list)
    app.router.add_get("/api/v1/get_csrf_token", get_csrf_token)

    app.router.add_post("/api/v1/process_upload", process_upload)
    app.router.add_get("/api/v1/process_oauth", process_oauth)
