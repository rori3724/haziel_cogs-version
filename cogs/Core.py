from discord.ext import commands
import datetime
import asyncio
import random
import discord

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, e):
        if str(e) == 'You are missing Manage Messages permission(s) to run this command.':
            await ctx.reply(f'{str(ctx.author)} 님은 해당 커맨드를 사용할 권한이 없습니다.')

    @commands.command(name='킥')
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason: str):
        embed = discord.Embed(title="킥문구 작동", color=0xAAFFFF)
        embed.add_field(name="킥된 유저", value=f"{user.mention}", inline=False)
        embed.add_field(name="킥 시킨 관리자", value=f"{ctx.author.mention}", inline=False)
        embed.add_field(name="사유", value=f"{reason}", inline=False)
        await ctx.reply(embed=embed)
        await user.kick(reason=reason)

    @commands.command(name='밴')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason: str):
        embed = discord.Embed(title="밴문구 작동", color=0xAAFFFF)
        embed.add_field(name="밴된 유저", value=f"{user.mention}", inline=False)
        embed.add_field(name="밴 시킨 관리자", value=f"{ctx.author.mention}", inline=False)
        embed.add_field(name="사유", value=f"{reason}", inline=False)
        await ctx.reply(embed=embed)

    @commands.command(name='청소')
    @commands.has_permissions(manage_messages=True)
    async def Clean(self, ctx, number: int):
        embed = discord.Embed(title="청소기능 발동", description =f"{number}개의 메세지가 {ctx.author.mention}님의 의하여 삭제 되었습니다")
        await ctx.send(embed=embed)

    @commands.command(name='핑')
    async def Ping(self, ctx):
        latency = self.bot.latency
        await ctx.reply(f'{str(round(latency * 1000))} ms 입니다!')

    @commands.command(name='타이머')
    async def Timer(self, ctx, timer: int = None):
        if timer == None:
            return await ctx.reply(f'{ctx.author.mention}\n그래서 몇 초를 맞추라고요?\n올바른 명령어는 `/타이머 (숫자)` 에요!"')
        await asyncio.sleep(timer)
        await ctx.send(f"{ctx.author.mention} ,\n타이머가 끝났어요!")

    @commands.command(name='주사위')
    async def Dice(self, ctx):
        await ctx.reply(random.randint(1, 6))

    @commands.command(name='서버정보')
    async def ServerInfo(self, ctx):
        embed = discord.Embed(title=str(f"{ctx.guild.name}의 서버정보"), colour=discord.Colour.green(),description="선택하신 서버의 정보예요.")
        embed.add_field(name="서버 이름", value=ctx.guild.name)
        embed.add_field(name="서버 아이디", value=f"{ctx.guild.id}")
        embed.add_field(name="서버 생성일", value=ctx.guild.created_at)
        embed.add_field(name="서버인원", value=str(ctx.guild.member_count)+"명")
        await ctx.reply(embed=embed)

    @commands.command(name='투표')
    async def Vote(self, ctx, *, vote: str = None):
        if vote == None:
            return await ctx.reply(embed=discord.Embed(title="명령어 오류", description="올바른 명령어는 '/투표 [제목]/항목1/항목2 ... 이에요", color=0xff0000))
        vote = vote.split('/')
        await ctx.reply(f'투표 - {vote[0]}')
        for i in range(1, len(vote)):
            a = await ctx.send(f'```{vote[i]}```')
            await a.add_reaction('👍')

    @commands.command(name='내정보')
    async def MyInfo(self, ctx):
        date = datetime.datetime.utcfromtimestamp(((ctx.author.id >> 22) + 1420070400000) / 1000)
        embed = discord.Embed(title=f'{ctx.author.name}의 정보', color=0xAAFFFF)
        embed.add_field(name="이름", value=ctx.author.name, inline=False)
        embed.add_field(name="별명", value=ctx.author.display_name)
        embed.add_field(name="가입일", value=str(date.year) + "년" + str(date.month) + "월" + str(date.day) + "일", inline=False)
        embed.add_field(name="아이디", value=ctx.author.id)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(name='말해')
    async def Talk(self, ctx, tada: str):
        embed = discord.Embed(title=f"{ctx.author.name}님에 의해서 발생한 message", description=tada, color=0xAAFFFF)
        embed.set_footer(text="출처(및 도와주신분):Dev. Hestia#5444")
        await ctx.reply(embed=embed)

    @commands.command(name='도움말')
    async def Help(self, ctx):
        if ctx.author.id == 704535152763601007:
            embed = discord.Embed(title="Haizel의 명령어 도움말", description="Haizel은 관리기능 편의기능 재미기능 등이 있어요!", color=0xAAFFFF)
            embed.add_field(name="관리기능", value="ㅤ", inline=False)
            embed.add_field(name="/킥 [사용자 ID] [사유]", value="특정사용자를 서버에서 킥시켜요", inline=True)
            embed.add_field(name="/밴 [사용자 ID] [사유]", value="특정사용자를 서버에서 밴시켜요", inline=True)
            embed.add_field(name="/청소 [개수]", value="매세지를 청소해요(요구 권한=관리자)", inline=True)
            embed.add_field(name="/핑", value="현재 핑을 측정해서 알려줘요", inline=True)
            embed.add_field(name="편의기능", value="ㅤ", inline=False)
            embed.add_field(name="/타이머 [시간(초기준)]", value="몇초의 타이머를 설정하고 끝나면 맨션해 드려요", inline=True)
            embed.add_field(name="/주사위", value="1부터 6까지 중에서 랜덤 숫자를 불러주어요", inline=True)
            embed.add_field(name="/서버정보", value="현재 서버의 정보를 알려줘요", inline=True)
            embed.add_field(name="/투표 [제목]/[항목 1]/[항목 2]....", value="투표를 할수있어요!예:'/투표 헤이즐은 유용하다/yes/no'같이 사용할수 있어요!", inline=True)
            embed.add_field(name="/내정보", value="디엠으로 내 정보를 알려줘요", inline=True)
            embed.add_field(name="/말해 [말할 내용]", value="봇으로 말을 할 수 있어요", inline=True)
            embed.add_field(name="재미기능", value="ㅤ", inline=False)
            embed.add_field(name="/금붕어 키우기[현재 오류남]", value="금붕어 키우기 미니게임을 해요", inline=True)
            embed.add_field(name="/가위(또는 /바위 또는 /보)", value="가위바위보 게임을 해요", inline=True)
            embed.add_field(name="봇 정보", value="ㅤ", inline=False)
            embed.add_field(name="/링크", value="한국 봇 리스트 링크를 줘요", inline=True)
            embed.add_field(name="/초대링크", value="저의 초대링크를 드려요", inline=True)
            embed.add_field(name="/패치노트", value="최근 패치노트를 불러주어요", inline=True)
            embed.add_field(name="/개발자", value="저를 만들어주신분을 알려드려요!", inline=True)
            embed.add_field(name="/도움말 페이지2", value="나머지 기능의 도움말이에요", inline=False)
            await ctx.reply(embed=embed)
        else:
            await ctx.reply(f"{ctx.author.mention}, 아래의 링크를 클릭하여 서포트서버에서 **#도움말**에 가보시면 되요!")
            embed = discord.Embed(title="Haizel의 서포트 서버", description="[여기](https://discord.gg/xEBEpw7uQs)를 클릭하여 바로 갈수 있어요!", color=0xAAFFFF)
            await ctx.send(embed=embed)

    @commands.command(name='패치노트')
    async def PatchNote(self, ctx):
        embed = discord.Embed(timestamp=ctx.created_at, colour=discord.Colour.red(), title="패치노트\n 베타Ver. 0.1.4", description="1.가위바위보 미니게임 추가!\n2.욕 검열 시스템 수정\n3.패치노트 추가\n4.킥문구 수정\n5.밴문구 수정\n6.타이머 기능 추가\n7.서버정보 기능 추가\n8.계산문구 제거")
        await ctx.reply(embed=embed)

    @commands.command(name='초대링크')
    async def InviteLink(self, ctx):
        embed = discord.Embed(title="haziel 초대링크",
                              description="[여기](https://discord.com/oauth2/authorize?client_id=800193013292335145&scope=bot&permissions=1610607742) 를 눌러 바로 초대 하실수 있어요!",
                              color=0x00ff00)
        await ctx.reply(embed=embed)

    @commands.command(name='링크')
    async def Link(self, ctx):
        await ctx.reply(embed=discord.Embed(title="한국 봇 리스트 링크",
                                                       description="[여기](https://koreanbots.dev/bots/800193013292335145)를 눌러 바로 접속하실수 있어요!\n하트 부탁드려요!",
                                                       color=0x00ff00))

    @commands.command(name='봇정보')
    async def BotInfo(self, ctx):
        users = len(self.bot.users)
        servers = len(self.bot.guilds)
        await ctx.reply(f"봇이 있는 서버 수: {servers}, 봇이 있는 서버에 있는 유저 수의 합: {users}")

    @commands.command(name='개발자')
    async def Developer(self, ctx):
        embed = discord.Embed(title="Haizel의 개발자 정보", description="저를 만들어주신분 정보에요!", color=0xAAFFFF)
        embed.add_field(name="닉네임", value="Lora로라#3561", inline=False)
        embed.add_field(name="아이디", value="704535152763601007", inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/800255202535014420/800922645733310505/KakaoTalk_20201001_105019614.jpg")
        await ctx.reply(embed=embed)

    @commands.command(name='서포트')
    async def Support(self, ctx, query: str = None):
        if query == '서버':
            embed = discord.Embed(title="Haizel의 서포트 서버",
                                  description="[여기](https://discord.gg/xEBEpw7uQs)를 클릭하여 바로 갈수 있어요!", color=0xAAFFFF)
            await ctx.reply(embed=embed)
        if query == None:
            pass
        else:
            pass

    @commands.command(name='가위')
    async def Scissors(self, ctx):
        r = random.randint(1, 3)
        if r == 1:
            await ctx.reply(f"{ctx.author.mention}님은 가위, 저는 가위!")
            await ctx.send(f"{ctx.author.mention}님 비겼습니다.")
        if r == 2:
            await ctx.reply(f"{ctx.author.mention}님은 가위, 저는 바위!")
            await ctx.send(f"{ctx.author.mention}님 제가 이겼습니다.")
        if r == 3:
            await ctx.reply(f"{ctx.author.mention}님은 가위, 저는 보!")
            await ctx.send(f"{ctx.author.mention}님 제가 졌습니다.")

    @commands.command(name='바위')
    async def Rock(self, ctx):
        r = random.randint(1, 3)
        if r == 1:
            await ctx.reply(f"{ctx.author.mention}님은 바위, 저는 가위!")
            await ctx.send(f"{ctx.author.mention}님 제가 졌습니다.")
        if r == 2:
            await ctx.reply(f"{ctx.author.mention}님은 바위, 저는 바위!")
            await ctx.send(f"{ctx.author.mention}님 비겼습니다.")
        if r == 3:
            await ctx.reply(f"{ctx.author.mention}님은 바위, 저는 보!")
            await ctx.send(f"{ctx.author.mention}님 제가 이겼습니다.")

    @commands.command(name='보')
    async def Paper(self, ctx):
        r = random.randint(1, 3)
        if r == 1:
            await ctx.reply(f"{ctx.author.mention}님은 보, 저는 가위!")
            await ctx.send(f"{ctx.author.mention}님 제가 이겼습니다.")
        if r == 2:
            await ctx.reply(f"{ctx.author.mention}님은 보, 저는 바위!")
            await ctx.send(f"{ctx.author.mention}님 제가 졌습니다.")
        if r == 3:
            await ctx.reply(f"{ctx.author.mention}님은 보, 저는 보!")
            await ctx.send(f"{ctx.author.mention}님 비겼습니다.")


def setup(bot):
    bot.add_cog(Core(bot))