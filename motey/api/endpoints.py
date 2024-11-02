import aiohttp
from aiohttp import web
import aiohttp_session
import aiohttp_csrf

from sqlalchemy import select, exists
from sqlalchemy.orm import Session

from motey.database.storage import EmoteStorage, UserStorage
from motey.filesystem import EmoteFileWriter
from motey.database.tables import User, Server

from motey.config import Config

routes = web.RouteTableDef()


async def get_emote_list(request: web.Request):
    emotes = EmoteStorage(request.app["db"]).fetch_all_emotes()

    names = []
    paths = []

    for emote in emotes:
        names.append(emote.name)
        paths.append(emote.path)

    return web.json_response((names, paths))


async def get_server_list(request: web.Request):
    session = await aiohttp_session.get_session(request)
    user_servers = UserStorage(request.app["db"]).get_user_servers(discord_id=session["discord_id"])

    guilds = []
    names = []

    for server in user_servers:
        guilds.append(server.guild)
        names.append(server.name)

    return web.json_response((guilds, names))


async def get_csrf_token(request: web.Request):
    token = await aiohttp_csrf.generate_token(request)

    return web.json_response({"field_name": Config.form_field_name, "token": token})


async def process_upload(request: web.Request):
    data = await request.post()
    emote = data["emote"]
    emote_name = data["emotename"]
    session = await aiohttp_session.get_session(request)

    if not emote_name or not emote:
        return web.json_response({"error_message": "Emote file or emote name empty"})

    with Session(request.app["db"]) as db_session:
        stmt = select(User).where(User.discord_id == session["discord_id"])
        author = db_session.scalars(stmt).one()

    if author.banned:
        return web.json_response({"error_message": "User banned from uploading emotes"})

    emote_storage = EmoteStorage(request.app["db"])

    if emote_storage.emote_exists(emote_name):
        return web.json_response(
            {"error_message": "Emote with this name already exists"}
        )

    file_writer = EmoteFileWriter(emote_name, emote.filename, emote.file)

    if file_writer.extension_valid:
        file_writer.save_to_filesystem()
    else:
        return web.json_response({"error_message": "File extension invalid"})

    emote_storage.add_emote(emote_name, str(file_writer.path), author)


async def process_oauth(request: web.Request):
    code = request.rel_url.query.get("code", "")
    session = await aiohttp_session.get_session(request)

    if not code:
        return web.json_response({"error_message": "There is no OAuth code"})

    payload = {
        "code": str(code),
        "client_id": str(Config.client_id),
        "client_secret": Config.client_secret,
        "grant_type": "authorization_code",
        "redirect_uri": Config.redirect_url,
        "scope": r"identify%20guilds",
    }

    async with aiohttp.ClientSession() as client_session:

        async with client_session.post(
            "https://discord.com/api/oauth2/token", data=payload
        ) as response:

            auth_token_data = await response.json()

    access_token = auth_token_data["access_token"]

    header = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    async with aiohttp.ClientSession(headers=header) as client_session:

        async with client_session.get("https://discord.com/api/users/@me") as response:

            user_data = await response.json()

            session["discord_id"] = int(user_data["id"])

        async with client_session.get(
            "https://discord.com/api/users/@me/guilds"
        ) as response:

            guilds = await response.json()

    with Session(request.app["db"]) as db_session:

        if not db_session.query(
            exists().where(User.discord_id == session["discord_id"])
        ).scalar():

            user = User(discord_id=session["discord_id"], name=user_data["global_name"])
            db_session.add(user)
            db_session.commit()

        for guild in guilds:
            guild_id = int(guild["id"])
            guild_name = guild["name"]

            stmt = select(Server).where(Server.guild == guild_id)
            server = db_session.scalars(stmt).one()

            if server is None:
                server = Server(guild=guild_id, name=guild_name)
                server.server_users.append(user)
                db_session.add(server)
                db_session.commit()
            else:
                if not db_session.query(
                    exists().where(
                        Server.guild == guild_id,
                        Server.server_users.any(discord_id=session["discord_id"]),
                        )
                    ).scalar():
                        server.server_users.append(user)
                        db_session.commit()

                if server.name != guild_name:
                    server.name = guild_name
                    db_session.commit()

    raise web.HTTPFound(location="/")
