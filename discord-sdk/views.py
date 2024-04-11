import traceback
from discord import Client, ui, ButtonStyle, Interaction, File, Message
from discord.ext.commands import Bot
from typing import Union
from io import StringIO
from subprocess import run, PIPE, STDOUT

class CodeView(ui.View):

    def __init__(self, client: Union[Client, Bot], message: Message, command_type: str, *args) -> None:
        super().__init__(timeout=None)
        self.command_type = command_type
        self.args = args
        self.client = client
        self.message = message

    @ui.button(style=ButtonStyle.green, emoji='🔁')
    async def re_run(self, interaction: Interaction, button: ui.Button) -> None:
        if not await self.client.is_owner(interaction.user):
            await interaction.response.send_message('This button is only available to the owner of the bot.', ephemeral=True)
        else:
            await interaction.response.defer(ephemeral=True)
            if self.command_type == 'eval':
                code = ' '.join(self.args).strip()
                if code.startswith('```py\n'): code = code.replace('```py\n', '', 1)
                elif code.startswith('```\n'): code = code.replace('```\n', '', 1)
                if code[::-1].startswith('```\n'): code = code[::-1].replace('```\n', '', 1)[::-1]
                _code = "\n".join([f"    {line}" for line in code.splitlines()])
                try:
                    exec(f'async def eval(client, message):\n{_code}')
                    output = str(await locals()['eval'](self.client, self.message))
                except:
                    output = traceback.format_exc()
            elif self.command_type == 'shell':
                process = run(list(self.args), stdout=PIPE, stderr=STDOUT, shell=True)
                output = process.stdout.decode('utf-8')
            buffer = StringIO()
            buffer.write(output)
            buffer.seek(0)
            await interaction.followup.send(file=File(buffer, 'output.log'), ephemeral=True)

    @ui.button(style=ButtonStyle.green, emoji='📝')
    async def show_code(self, interaction: Interaction, button: ui.Button) -> None:
        if self.command_type == 'eval':
            code = ' '.join(self.args).strip()
            if code.startswith('```py\n'): code = code.replace('```py\n', '', 1)
            elif code.startswith('```\n'): code = code.replace('```\n', '', 1)
            if code[::-1].startswith('```\n'): code = code[::-1].replace('```\n', '', 1)[::-1]
            filename = 'code.py'
        elif self.command_type == 'shell':
            code = ' '.join(arg for arg in self.args if len(arg) > 0)
            filename = 'code.bat'
        buffer = StringIO()
        buffer.write(code)
        buffer.seek(0)
        await interaction.response.send_message(file=File(buffer, filename), ephemeral=True)