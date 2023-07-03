from aiohttp import web
import aiohttp_jinja2
from sqlalchemy import insert
from sqlalchemy import select
import hashlib

from motey.infrastructure.database import tables
from motey.infrastructure.config import Config
from motey.infrastructure.database.tables import users


@aiohttp_jinja2.template('list.html')
async def list_emotes(request: web.Request):
    with request.app['db'].connect() as connection:
        cursor = connection.execute(tables.emotes.select())
        records = cursor.fetchall()
        emotes = [emote for emote in records]
        return {"emotes": emotes}


@aiohttp_jinja2.template('index.html')
async def index(request: web.Request):
    return None


@aiohttp_jinja2.template('index.html')
async def upload(request: web.Request, config: Config = Config()):
    # TODO
    # Check if the user has proper session cookie
    data = await request.post()
    emote_name = data['emotename']
    if not emote_name:
        return {'error_message': 'Please enter emote name'}
    emote = data['emote']
    filename = emote.filename
    extension = filename.split('.')[-1]
    emote_image = emote.file.read()
    location = str(config.emotes_dir / emote_name) + "." + extension
    with open(location, 'wb') as f:
        f.write(emote_image)
    with request.app['db'].connect() as connection:
        statement = insert(tables.emotes)\
            .values(name=emote_name, location=location)
        connection.execute(statement)
        connection.commit()
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
        statement = insert(tables.emotes)\
            .values(login=login, password=password)
        connection.execute(statement)
        connection.commit()
    raise web.HTTPFound(location='/')


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
        statement = select(users.id)\
            .where(login=login, password=password)
        userId = connection.scalars(statement).one()
        # TODO
        # if userId:
            # Successful login
            # Set session cookie
    raise web.HTTPFound(location='/')
