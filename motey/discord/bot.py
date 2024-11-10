import discord
from discord import app_commands

from sqlalchemy import select, update, exists
from sqlalchemy.orm import Session

from motey.database.storage import EmoteStorage
from motey.database.tables import User
from motey.database.engine import get_db
from motey.config import Config

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents = intents)

tree = app_commands.CommandTree(client)

emotes = None

@client.event
async def on_ready():
    await tree.sync()
    print(f"loged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
            return

    with Session(get_db()) as db_session:
        if not db_session.query(
            exists().where(User.discord_id == message.author.id)
        ).scalar():
            user = User(discord_id=message.author.id, name=message.author.name)
            db_session.add(user)
            db_session.commit()

    with Session(get_db()) as db_session:
        stmt = select(User).where(User.discord_id == message.author.id)
        author = db_session.scalars(stmt).one()

        if author.replace is False:
            return

    emote = emotes.get_emote_by_name(message.content)

    if emote is not None:
        await message.delete()
        with open(emote.path, "rb") as f:
            picture = discord.File(f)
            webhook = await message.channel.create_webhook(name=message.author.name)
            await webhook.send(
                file=picture,
                username=message.author.name,
                avatar_url=message.author.avatar,
            )
            await webhook.delete()


@tree.command(name="toggle_replacing", description="Tells the bot if you want to have your messages replaced with images.")
async def toggle_replacing(interaction):
    with Session(get_db()) as db_session:
        if not db_session.query(
            exists().where(User.discord_id == interaction.user.id)
        ).scalar():
            user = User(discord_id=interaction.user.id, name=interaction.user.name)
            db_session.add(user)
            db_session.commit()

    with Session(get_db()) as db_session:
        stmt = select(User).where(User.discord_id == interaction.user.id)
        author = db_session.scalars(stmt).one()

    with Session(get_db()) as db_session:
        stmt = (
            update(User)
            .where(User.discord_id == interaction.user.id)
            .values(replace=not author.replace)
        )
        author.replace = not author.replace
        db_session.execute(stmt)
        db_session.commit()

    await interaction.response.send_message(
        f"Replacing messages with emotes is now set to: {author.replace}"
    )

if __name__ == "__main__":
    emotes = EmoteStorage(get_db())
    client.run(Config.token)