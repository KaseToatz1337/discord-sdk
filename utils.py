from typing import Tuple, List, Optional, Coroutine, Union
from discord import Client, Message
from discord.ext.commands import Bot

from .eval import eval
from .loading import load, unload, reload, cogs, sync

CommandTypes = {
    "python": eval,
    "py": eval,
    "load": load,
    "ld": load,
    "unload": unload,
    "ul": unload,
    "reload": reload,
    "rl": reload,
    "cogs": cogs,
    "sync": sync
}

def parse_message(client: Union[Client, Bot], message: Message) -> Optional[Tuple[Coroutine, List[str]]]:
    if hasattr(client, "command_prefix"):
        prefix = client.command_prefix
    else:
        prefix = "sdk"
    if message.content.startswith(prefix):
        msg = message.content.replace(prefix, "", 1)
        while msg.startswith(" "):
            msg = msg[1:]
    else:
        return
    command = CommandTypes.get(msg.splitlines()[0].split(" ")[0].lower(), None)
    args = [arg for arg in msg[len(msg.splitlines()[0].split(" ")[0]):].split(" ")]
    if len(args[0]) == 0: args = args[1:]
    if command:
        return (command, args)