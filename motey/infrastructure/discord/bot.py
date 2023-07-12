import nextcord

from sqlalchemy import insert, select, update, exists
from sqlalchemy.orm import Session

from motey.infrastructure.database.storage import EmoteStorage
from motey.infrastructure.database.tables import User, Server, Emote
from motey.infrastructure.database.engine import get_db
from motey.infrastructure.config import Config

class MoteyClient(nextcord.Client):
    def __init__(self, emote_storage: EmoteStorage = EmoteStorage(Session(get_db()))):
        intents = nextcord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self._emotes = emote_storage

    async def on_message(self, message):
        if message.author.bot:
            return
        with Session(get_db()) as db_session:
            stmt = select(User).where(User.discord_id==message.author.id)
            author = db_session.scalars(stmt).one()
        try:
            if author.replace==False:
                return
        except:
            pass
        emote = self._emotes.get_emote_by_name(message.content)
        if emote is not None:
            await message.delete()
            with open(emote.path, 'rb') as f:
                picture = nextcord.File(f)
                webhook = await message.channel.create_webhook(name=message.author.name)
                await webhook.send(file=picture, username=message.author.name, avatar_url=message.author.avatar)
                await webhook.delete()

client = MoteyClient()
@client.slash_command()
async def toggle_replacing(interaction: nextcord.Interaction):
    with Session(get_db()) as db_session:
        if not db_session.query(exists().where(User.discord_id == interaction.user.id)).scalar():
            user = User(discord_id=interaction.user.id)
            db_session.add(user)
            db_session.commit()
    with Session(get_db()) as db_session:
        stmt = select(User).where(User.discord_id==interaction.user.id)
        author = db_session.scalars(stmt).one()
    with Session(get_db()) as db_session:
        stmt = (
        update(User)
        .where(User.discord_id == interaction.user.id)
        .values(replace=not author.replace))
        author.replace = not author.replace
        db_session.execute(stmt)
        db_session.commit()
    await interaction.response.send_message(f"Replacing messages with emotes is now set to: {author.replace}")

if __name__ == '__main__':
    client.run(Config.token)
