from discord import Client, Message
from discord.ext.commands import Bot, Cog
from typing import Union

from .utils import parse_message

class SDK(Cog):

    def __init__(self, client: Union[Client, Bot]) -> None:
        self.client = client

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        parsed = parse_message(self.client, message)
        if parsed and await self.client.is_owner(message.author):
            command, args = parsed
            await command(self.client, message, *args)

async def setup(client: Union[Client, Bot]) -> None:
    await client.add_cog(SDK(client))