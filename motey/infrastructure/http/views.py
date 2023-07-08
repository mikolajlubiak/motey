import aiohttp
from aiohttp import web
import aiohttp_jinja2
import aiohttp_session

from sqlalchemy import insert, select, update

from motey.infrastructure.database.storage import EmoteStorage
from motey.infrastructure.filesystem import EmoteFileWriter

from motey.infrastructure.config import Config

routes = web.RouteTableDef()

@aiohttp_jinja2.template('list.html')
async def list_emotes(request: web.Request):
    with Session(request.app['db']) as session:
        return EmoteStorage(session).fetch_all_emotes()


@aiohttp_jinja2.template('index.html')
async def index(request: web.Request):
    return None


@aiohttp_jinja2.template('index.html')
async def upload(request: web.Request):
    data = await request.post()
    emote = data['emote']
    emote_name = data['emotename']
    if not emote_name:
        return {'error_message': 'Please enter emote name'}

    file_writer = EmoteFileWriter(emote_name, emote.filename, emote.file)
    if file_writer.extension_valid:
        file_writer.save_to_filesystem()
    else:
        return {'error_message': 'File extension invalid'}

    with Session(request.app['db']) as session:
        emote_storage = EmoteStorage(session)
        if emote_storage.emote_exists(emote_name):
            return {'error_message': 'Emote with this name already exists'}
        emote_storage.add_emote(emote_name, str(file_writer.path), author) # `author` needs to be object of User class that is the author of this Emote

    raise web.HTTPFound(location='/')


@routes.get('/process_oauth')
async def process_oauth(request: web.Request):
    code = request.rel_url.query.get("code", "")
    if not code:
        return {'error_message': 'There is no oauth code'}
    payload = {
            "code": str(code),
            "client_id": str(Config.client_id),
            "client_secret": Config.client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": Config.redirect_url,
            "scope": "identify%20guilds"
        }
    async with aiohttp.ClientSession() as session:
        async with session.post("https://discord.com/api/oauth2/token", data=payload) as response:
            auth_token_data = await response.json()
    access_token = auth_token_data["access_token"]
    header = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }  
    async with aiohttp.ClientSession(headers=header) as session:
        async with session.get("https://discord.com/api/users/@me") as response:
            user_data = await response.json()
            session = await aiohttp_session.get_session(request)
            session['discord_id'] = user_data['id']
    async with aiohttp.ClientSession(headers=header) as session:
        async with session.get("https://discord.com/api/users/@me/guilds") as response:
            guilds = await response.json()
    raise web.HTTPFound(location='/')
