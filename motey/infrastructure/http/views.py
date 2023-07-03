from aiohttp import web
import aiohttp_jinja2
from sqlalchemy import insert
from sqlalchemy import select
import hashlib

from motey.infrastructure.database import tables
from motey.infrastructure.database.tables import users
from motey.infrastructure.database.storage import EmoteStorage, StorageException
from motey.infrastructure.filesystem import EmoteFileWriter


@aiohttp_jinja2.template('list.html')
async def list_emotes(request: web.Request):
    with request.app['db'].connect() as connection:
        return {"emotes": EmoteStorage(connection).fetch_all_emotes()}


@aiohttp_jinja2.template('index.html')
async def index(request: web.Request):
    return None


@aiohttp_jinja2.template('index.html')
async def upload(request: web.Request):
    # TODO
    # Check if the user has proper session cookie
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
        emote_storage = EmoteStorage(connection)
        if emote_storage.emote_exists(emote_name):
            return {'error_message': 'Emote with this name already exists'}
        try:
            emote_storage.add_emote(emote_name, str(file_writer.location))
        except StorageException as e:
            file_writer.rollback()
            raise web.HTTPInternalServerError from e

    raise web.HTTPFound(location='/')


@aiohttp_jinja2.template('login.html')
async def register(request: web.Request):
    data = await request.post()
    login = data['login']
    password = data['password']
    password = hashlib.sha512(password.encode()).hexdigest()
    if not login:
        return {'error_message': 'Please enter login'}
    if not password:
        return {'error_message': 'Please enter password'}
    with request.app['db'].connect() as connection:
        statement = insert(tables.users)\
            .values(login=login, password=password)
        connection.execute(statement)
        connection.commit()
    raise web.HTTPFound(location='/')


@aiohttp_jinja2.template('login.html')
async def show_login_page(request: web.Request):
    pass


@aiohttp_jinja2.template('login.html')
async def login(request: web.Request):
    data = await request.post()
    login = data['login']
    password = data['password']
    password = hashlib.sha512(password.encode()).hexdigest()
    if not login:
        return {'error_message': 'Please enter login'}
    if not password:
        return {'error_message': 'Please enter password'}
    with request.app['db'].connect() as connection:
        statement = select(users)\
            .where(login==login, password==password)
        userId = connection.scalars(statement).one_or_none()
        # TODO
        # if userId:
            # Successful login
            # Set session cookie
    raise web.HTTPFound(location='/')
