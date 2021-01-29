import discord
from discord.ext import commands
from config import OWNERS
import ast
from Tools import AutoCogsReload

def CheckOwner():
    def predicate(ctx):
        return ctx.author.id in OWNERS
    return commands.check(predicate)

def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, e):
        if str(e) == 'The check functions for command eval failed.':
            await ctx.reply("이 명령어는 저의 개발자만 사용할수 있어요!")
            embed = discord.Embed(title="Haizel의 개발자 정보", description="저를 만들어주신분 정보에요!", color=0xAAFFFF)
            embed.add_field(name="닉네임", value="Lora로라#3561", inline=False)
            embed.add_field(name="아이디", value="704535152763601007", inline=False)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/800255202535014420/800922645733310505/KakaoTalk_20201001_105019614.jpg")
            await ctx.send(embed=embed)

    @commands.command()
    @CheckOwner()
    async def eval(self, ctx, *, cmd: str):
        try:
            fn_name = "_eval_expr"
            cmd = cmd.strip("` ")
            cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
            body = f"async def {fn_name}():\n{cmd}"
            parsed = ast.parse(body)
            body = parsed.body[0].body
            insert_returns(body)
            env = {
                'bot': self.bot,
                'discord': discord,
                'commands': commands,
                'ctx': ctx,
                '__import__': __import__
                }
            exec(compile(parsed, filename="<ast>", mode="exec"), env)

            result = (await eval(f"{fn_name}()", env))
            embed = discord.Embed(title='실행 성공', colour=discord.Colour.green())
            embed.add_field(name="`📥 Input (들어가는 내용) 📥`", value=f"```py\n{cmd}```", inline=False)
            embed.add_field(name="`📤 Output (나오는 내용) 📤`", value=f"```py\n{result}```", inline=False)
            embed.add_field(name="`🔧 Type (타입) 🔧`", value=f"```py\n{type(result)}```", inline=False)
            await ctx.reply(embed=embed)
        except Exception as a:
            await ctx.send(a)

    @commands.command(name='리로드', aliases=['r'])
    @CheckOwner()
    async def Reload(self, ctx, extension = None):
        try:
            if extension == None:
                AutoCogsReload(self.bot)
                await ctx.reply('정상적으로 리로드가 되었습니다.')
            else:
                self.bot.reload_extension(extension)
                await ctx.reply(f'정상적으로 {extension}.py 리로드가 되었습니다.')
        except Exception as e:
            await ctx.reply(f'리로드 진행 도중 오류가 발생하였습니다. {e}')


def setup(bot):
    bot.add_cog(Owner(bot))