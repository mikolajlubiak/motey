import nextcord

from motey.infrastructure.database.storage import EmoteStorage
from motey.infrastructure.database.engine import get_db


class MoteyClient(nextcord.Client):
    def __init__(self, emote_storage: EmoteStorage = EmoteStorage(get_db().connect())):
        intents = nextcord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self._emotes = emote_storage

    async def on_message(self, message):
        if message.author.bot:
            return

        emote = self._emotes.get_emote_by_name(message.content)
        if emote is not None:
            self._emotes.increase_emote_usage_count(emote.id)
            await message.delete()
            with open(emote.location, 'rb') as f:
                picture = nextcord.File(f)
                webhook = await message.channel.create_webhook(name=message.author.name)
                await webhook.send(file=picture, username=message.author.name, avatar_url=message.author.avatar)
                await webhook.delete()


if __name__ == '__main__':
    MoteyClient().run('token')
