from traceback import format_exc
from discord import Client, Message, Object
from discord.ext.commands import Bot
from typing import Union

async def load(client: Union[Client, Bot], message: Message, *args) -> None:
    successful = []
    failed = []
    for arg in [arg.replace('/', '.').replace('\\', '.') for arg in args]:
        try:
            await client.load_extension(arg)
            successful.append(arg)
        except:
            failed.append(format_exc().splitlines()[-1].split(": ", 1)[1])
    if len(failed) == 0:
        await message.add_reaction('✅')
    else:
        await message.add_reaction('⚠️')
        successful = f'\n\n{", ".join(successful)} loaded succesfully.' if len(successful) > 0 else ''
        failed = "\n".join(failed)
        await message.reply(f'```\n{failed}{successful}\n```', mention_author=False)

async def unload(client: Union[Client, Bot], message: Message, *args) -> None:
    successful = []
    failed = []
    for arg in [arg.replace('/', '.').replace('\\', '.') for arg in args]:
        try:
            if arg == 'discord-sdk':
                failed.append('Extension \'discord-sdk\' cannot be unloaded.')
            else:
                await client.unload_extension(arg)
                successful.append(arg)
        except:
            failed.append(format_exc().splitlines()[-1].split(": ", 1)[1])
    if len(failed) == 0:
        await message.add_reaction('✅')
    else:
        await message.add_reaction('⚠️')
        successful = f'\n\n{", ".join(successful)} unloaded succesfully.' if len(successful) > 0 else ''
        failed = "\n".join(failed)
        await message.reply(f'```\n{failed}{successful}\n```', mention_author=False)

async def reload(client: Union[Client, Bot], message: Message, *args) -> None:
    successful = []
    failed = []
    for arg in [arg.replace('/', '.').replace('\\', '.') for arg in args]:
        try:
            if arg == 'discord-sdk':
                failed.append('Extension \'discord-sdk\' cannot be reloaded.')
            else:
                await client.reload_extension(arg)
                successful.append(arg)
        except:
            failed.append(format_exc().splitlines()[-1].split(": ", 1)[1])
    if len(failed) == 0:
        await message.add_reaction('✅')
    else:
        await message.add_reaction('⚠️')
        successful = f'\n\n{", ".join(successful)} reloaded succesfully.' if len(successful) > 0 else ''
        failed = "\n".join(failed)
        await message.reply(f'```\n{failed}{successful}\n```', mention_author=False)

async def sync(client: Union[Client, Bot], message: Message, *args) -> None:
    guilds = [Object(id=int(guild)) for guild in args if guild.isdigit() and guild in [clientguild.id for clientguild in client.guilds]]
    if len(guilds) > 0:
        for guild in guilds:
            client.tree.copy_global_to(guild=Object(id=int(guild)))
            await client.tree.sync(guild=Object(id=int(guild)))
    else:
        await client.tree.sync()
    await message.reply('Registered commands.', mention_author=False)

async def cogs(client: Union[Client, Bot], message: Message, *args) -> None:
    cogs = '\n'.join(client.extensions.keys())
    await message.reply(f'```\n{cogs}\n```', mention_author=False)