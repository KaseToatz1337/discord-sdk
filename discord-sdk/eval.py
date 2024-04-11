from traceback import format_exc
from io import StringIO
from discord import Client, Message, File
from discord.ext.commands import Bot
from typing import Union

from .views import CodeView

async def eval(client: Union[Client, Bot], message: Message, *args) -> None:
    code = ' '.join(args).strip()
    if code.startswith('```py\n'): code = code.replace('```py\n', '', 1)
    elif code.startswith('```python\n'): code = code.replace('```python\n', '', 1)
    elif code.startswith('```\n'): code = code.replace('```\n', '', 1)
    if code[::-1].startswith('```\n'): code = code[::-1].replace('```\n', '', 1)[::-1]
    _code = "\n".join([f"    {line}" for line in code.splitlines()])
    try:
        exec(f'async def eval(client, message):\n{_code}')
        output = str(await locals()['eval'](client, message))
        await message.add_reaction('✅')
    except:
        output = format_exc()
        await message.add_reaction('❌')
    buffer = StringIO()
    buffer.write(output)
    buffer.seek(0)
    await message.reply(file=File(buffer, 'output.log'), mention_author=False, view=CodeView(client, message, 'eval', *args))