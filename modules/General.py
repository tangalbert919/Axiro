import discord, json, random, time, sys
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType


class General(commands.Cog, name='General'):

    def __init__(self, bot):
        self.bot = bot
        self.information = json.loads(open('help.json', 'r').read())

    @commands.command(name='help')
    @commands.cooldown(1, 2, BucketType.user)
    @commands.guild_only()
    async def _help(self, ctx, commands=None):
        if commands is None:
            embed = discord.Embed(title='I\'m Axiro! This is my list of commands!',
                              description='If you need help on a specific command, use ``x!help <command>``')
            for module in self.bot.cogs:
                cog = self.bot.get_cog(module)
                cogcmds = cog.get_commands()
                list = ''
                for c in cogcmds:
                    list += f'``{c}`` '
                embed.add_field(name=module, value=list, inline=False)
            embed.set_footer(icon_url=ctx.message.author.avatar_url,
                             text=f'Requested by {ctx.message.author.name}')
        else:
            embed = self.commandhelp(commands)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def ping(self, ctx):
        t_1 = time.perf_counter()
        await ctx.trigger_typing()
        t_2 = time.perf_counter()
        time_delta = round((t_2 - t_1) * 1000)
        responses = ['Pong!', 'Ack!', 'Whoa!', 'Pang!', 'How am I doing?']
        await ctx.send(f'{random.choice(responses)} ``Time: {time_delta}ms``')

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def time(self, ctx):
        now = datetime.datetime.now()
        msg = ('Current date and time : ')
        timeline = (now.strftime("%Y.%m.%d %H:%M:%S"))
        await ctx.send('**`{}`**'.format(msg))
        await ctx.send('**`{}`**'.format(timeline))

    @commands.command(aliases=['info'])
    @commands.cooldown(1, 2, BucketType.user)
    @commands.guild_only()
    async def about(self, ctx):
        embed = discord.Embed(title='About Axiro:', description='This bot was created to do what most '
                                    'bots should do, and then some really weird things.')
        embed.add_field(name='Author: ', value='tangalbert919 (The Freaking iDroid)', inline=False)
        embed.add_field(name='Stats: ', value=f'Guilds: **{len(self.bot.guilds)}**\n'
                                              f'Unique Players: **{sum(1 for _ in self.bot.get_all_members())}**\n')
        embed.add_field(name='Version: ', value=f'Axiro: **{self.bot.version_code}**\nPython: **{sys.version}**\n'
                                                f'Discord.py: **{discord.__version__}**')
        embed.set_footer(icon_url=ctx.message.author.avatar_url,
                         text=f'Requested by {ctx.message.author.name}')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def user(self, ctx, user: discord.Member=None):
        if user is None:
            await ctx.send('User not found or specified. Collecting information about sender...')
            user = ctx.message.author
        roles = []
        for x in user.roles:
            roles.append(x.name)
        knownroles = '\n'.join(roles)
        embed = discord.Embed(title='Information successfully collected!', 
                              description=f'Here\'s what we know about {user.name} (also known as {user.display_name})')
        embed.add_field(name='User ID: ', value=str(user.id), inline=False)
        embed.add_field(name='Current Roles: ', value=knownroles, inline=False)
        embed.add_field(name='Joined Discord on: ', value=target.created_at, inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {ctx.message.author.name}')
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def avatar(self, ctx, user : discord.User=None):
        if user is None:
            user = ctx.message.author
        embed = discord.Embed(title='{users}\'s avatar:')
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def invite(self, ctx):
        embed = discord.Embed(color=discord.Colour.dark_orange(), title='Are you going to invite me to your server?',
                              description='Invite me by clicking [here](https://discordapp.com/api/oauth2/authorize?client_id=458834071796187149&permissions=8&scope=bot).')
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {ctx.message.author.name}')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def server(self, ctx):
        embed = discord.Embed(color=discord.Colour.dark_gold(), title='So you want to join my creator\'s server?',
                              description='Come join the support server by clicking [here](https://discord.gg/NEpsy8h)')
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {ctx.message.author.name}')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def suggest(self, ctx, *, report: str):
        channel = self.bot.get_channel(460669314933063680)
        embed = discord.Embed(color=discord.Colour.blue(), title='Suggestion!', description=f'We got a suggestion from {ctx.message.author}!')
        embed.add_field(name='Suggestion: ', value=report)
        await channel.send(embed=embed)
        await ctx.send('Your suggestion has been sent.')

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def report(self, ctx, *, report: str):
        channel = self.bot.get_channel(460666448352641026)
        embed = discord.Embed(color=discord.Colour.red(), title='Bug report!', description=f'We got a bug report from {ctx.message.author}!')
        embed.add_field(name='Full report: ', value=report)
        await channel.send(embed=embed)
        await ctx.send('Your report has been sent.')

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def github(self, ctx):
        embed = discord.Embed(color=discord.Colour.light_grey(), title='Are you a programmer and want to help?',
                              description='You should click [here](https://github.com/tangalbert919/Axiro) to see my repository. I am an open-source bot.')
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {ctx.message.author.name}')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def upvote(self, ctx):
        embed = discord.Embed(color=discord.Colour.blue(), title='Come vote for Axiro!',
                              description='Do you really like using Axiro? You can upvote it by clicking [here](https://discordbots.org/bot/458834071796187149/vote)!')
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {ctx.message.author.name}')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def avatar(self, ctx, user: discord.Member=None):
        if user is None:
            user = ctx.message.author
        embed = discord.Embed(color=discord.Colour.gold(), title=f'{user.name}\'s avatar:')
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    def commandhelp(self, command):
        embed = discord.Embed(title=f'Help on {command}', description='What we know about this command...')
        try:
            embed.add_field(name='Usage: ', value=self.information[command], inline=False)
        except Exception:
            embed.add_field(name='Error: ', value="This command does not exist.", inline=False)
        return embed


def setup(bot):
    bot.add_cog(General(bot))
