from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
from Tools import AutoCogs
load_dotenv(verbose=True)
TOKEN = os.getenv('TOKEN')
intents = discord.Intents.all()

class Haziel(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/', intents=intents)
        self.remove_command('help')
        AutoCogs(self)

    async def on_ready(self):
        print(f'봇 작동 준비가 완료되었습니다. 명령어 주세요!\n{str(self.user)}\n============================')

    async def on_guild_join(self, server):
        print(f'{server} 서버에 들어왔어요! 헤이즐 서버 하나 늘었다')

    async def on_guild_remove(self, server):
        print(f"{server} 서버에서 헤이즐이 나갔어요,,,ㅠㅠ")

    async def on_message(self, message):
        if message.author.bot:
            return
        else:
            await self.process_commands(message)

bot = Haziel()
bot.run(TOKEN, bot=True)