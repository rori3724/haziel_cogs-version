from discord.ext import commands
from discord.ext import tasks
import discord
import asyncio

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user = len(self.bot.users)
        self.server = len(self.bot.guilds)
        self.message = ["/도움말 과 명령어 듣기", f"{self.user}명과 {self.server}개의 서버에서 안전하게 보호되고 있어요!", "로라님이 만들어주셔서 열심히 일하는중", "가입된 서버분들을 위해 열심히 일하는중"]
        asyncio.get_event_loop().create_task(self.on_load())


    @tasks.loop(seconds=5)
    async def StatusLoop(self):
        for i in self.message:
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=str(i), type=discord.ActivityType.playing))
            await asyncio.sleep(5)

    async def on_load(self):
        await self.bot.wait_until_ready()
        self.StatusLoop.start()

def setup(bot):
    bot.add_cog(Status(bot))