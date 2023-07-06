from aiohttp import web
import aiohttp_jinja2
import aiohttp_session

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update

import hashlib
import secrets

from motey.infrastructure.database import tables
from motey.infrastructure.database.tables import users
from motey.infrastructure.database.storage import EmoteStorage, StorageException
from motey.infrastructure.filesystem import EmoteFileWriter

from motey.infrastructure.config import Config

routes = web.RouteTableDef()

@aiohttp_jinja2.template('list.html')
async def list_emotes(request: web.Request):
    with request.app['db'].connect() as connection:
        return {"emotes": EmoteStorage(connection).fetch_all_emotes()}


@aiohttp_jinja2.template('index.html')
async def index(request: web.Request):
    return None


@aiohttp_jinja2.template('index.html')
async def upload(request: web.Request):
    session_id = request.cookies.get('session_id')
    if not session_id:
        return {'error_message': 'Please login'}
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

    with request.app['db'].connect() as connection:
        statement = select(users.c.id)\
            .where(users.c.session_id == session_id)
        user_id = connection.execute(statement).one_or_none()[0]
        if not user_id:
            return {'error_message': 'Invalid session cookie'}

        emote_storage = EmoteStorage(connection)
        if emote_storage.emote_exists(emote_name):
            return {'error_message': 'Emote with this name already exists'}
        try:
            emote_storage.add_emote(emote_name, str(file_writer.location), user_id)
        except StorageException as e:
            file_writer.rollback()
            raise web.HTTPInternalServerError from e

    raise web.HTTPFound(location='/')

@routes.get('/login')
async def login(request: web.Request):
    session = await aiohttp_session.get_session(request)
    session["id"] = "discord id"
    raise web.HTTPFound(location='/')

@routes.get('/init_oauth')
async def init_oauth(request: web.Request):
    raise web.HTTPFound(location=config.auth_start_url)

@routes.get('/process_oauth')
async def process_oauth(request: web.Request):
    code = request.match_info.get("code", "")
    if not code:
        return {'error_message': 'There is no oauth code'}
    else:
        payload = {
                "code":code,
                "client_id":Config.client_id,
                "client_secret":Config.client_secret,
                "grant_type":"authorization_code",
                "redirect_url":Config.redirect_url,
                "scope":"identify%20guilds"
            }
        #response = await request("url", payload)
        #print(response)
        

async def request(url, data):
    out = []
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as resp:
            out.append(resp.text())
    return out