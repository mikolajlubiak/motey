import discord
from discord import app_commands

from sqlalchemy import select, update, exists
from sqlalchemy.orm import Session

from motey.database.storage import EmoteStorage
from motey.database.tables import User
from motey.database.engine import get_db
from motey.filesystem import AsyncEmoteWriter
from motey.config import Config

def main():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents = intents)
    tree = app_commands.CommandTree(client)
    emotes = EmoteStorage(get_db())

    async def is_admin(interaction: discord.Interaction) -> bool:
        with Session(get_db()) as db_session:
            stmt = select(User).where(User.discord_id == interaction.user.id)
            author = db_session.scalars(stmt).one()
            result = interaction.guild.id in author.admin_servers
            if not result: await interaction.response.send_message("You are not an administrator.")
            return result

    async def is_not_banned(interaction: discord.Interaction) -> bool:
        with Session(get_db()) as db_session:
            stmt = select(User).where(User.discord_id == interaction.user.id)
            author = db_session.scalars(stmt).one()
            if author.banned: await interaction.response.send_message("Failed to add the emote, you were banned from uploading new emotes.")
            return not author.banned

    @client.event
    async def on_ready():
        print(f"loged in as {client.user}")

    @client.event
    async def on_message(message: discord.Message):
        if message.author.bot:
                return

        if message.content == "whoami" and message.author.id in [977864831568850955, 633222053050318855, 267631595425366018, 278934243516874752, 776867547404173362]: await message.reply("root")

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
    async def toggle_replacing(interaction: discord.Interaction):
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

    @tree.command(name="add_emote", description="Add a new emote.")
    @app_commands.check(is_not_banned)
    async def add_emote(interaction: discord.Interaction, emote_name: str, image: discord.Attachment):
        if not emote_name or not image:
            await interaction.response.send_message("Failed to add the emote, missing name or file.")
            return

        with Session(get_db()) as db_session:
            stmt = select(User).where(User.discord_id == interaction.user.id)
            author = db_session.scalars(stmt).one()

        if emotes.emote_exists(emote_name):
            await interaction.response.send_message("Failed to add the emote, an emote with this name already exists.")
            return
        
        file_writer = AsyncEmoteWriter(emote_name, image.filename, image)

        if file_writer.extension_valid:
            await file_writer.save_to_filesystem()
        else:
            await interaction.response.send_message("Failed to add the emote, invalid file type.")
            return

        emotes.add_emote(emote_name, str(file_writer.path), author)
        await interaction.response.send_message(f"Emote **{emote_name}** added successfuly!")

    @tree.command(name="sync_slash_commands", description="Synchronize the bots slash commands.")
    @app_commands.check(is_admin)
    async def sync(interaction: discord.Interaction):
        await tree.sync()
        await interaction.response.send_message("Slash commands synchronized.")

    client.run(Config.token)

if __name__ == "__main__": main()
