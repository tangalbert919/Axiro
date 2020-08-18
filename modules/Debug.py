from discord.ext import commands
import io
from contextlib import redirect_stdout
import subprocess
import textwrap
import traceback
import requests
from os import listdir
from os.path import isfile, join
from discord.ext.commands import Bot, Greedy
from discord import User

class Debug(commands.Cog, command_attrs=dict(hidden=True), name='Debug'):

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, module):
        """Reloads a module."""
        try:
            self.bot.unload_extension('modules.' + module)
            self.bot.load_extension('modules.' + module)
        except Exception:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send(':ok_hand:')

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, module):
        """Loads a new module."""
        try:
            self.bot.load_extension('modules.' + module)
        except Exception:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send(':ok_hand:')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, module):
        """Unloads a module."""
        try:
            self.bot.unload_extension('modules.' + module)
        except Exception:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send(':ok_hand:')

    @commands.command()
    @commands.is_owner()
    async def say(self, ctx, *, message: str):
        await ctx.message.delete()
        await ctx.send(message)

    """The following two definitions come from the Monika bot (dev.py module)."""
    """It has been modified so only the creator can run this command."""
    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *, message: str):
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(message)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('👌')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.command()
    @commands.is_owner()
    async def pull(self, ctx):
        c = subprocess.call(('git', 'pull'))
        if c != 0:
            await ctx.send('Updating from Git failed.')
            return
        await ctx.send('Successfully updated from Git.')

    @commands.command()
    @commands.is_owner()
    async def download(self, ctx, link):
        file = [f for f in listdir('./modules/') if isfile(join('./modules/', f))]
        r = requests.get(link)
        newmod = open(f'./modules/module-{len(file)}.py', 'wb+')
        try:
            newmod.write(r.content)
        except:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        await ctx.send('Downloaded new module ending in {len(file)}')

    @commands.command()
    @commands.is_owner()
    async def dl(self, ctx, url: str, path: str):
        '''Downloads File to Hard Drive'''
            ``````
                r = requests.get(url, stream=True)
                with open(path, 'wb') as f:
                        total_length = int(r.headers.get('content-length'))
                        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                                if chunk:
                                    f.write(chunk)
                                    f.flush()
        await ctx.send(':white_check_mark: downloaded file from **`{}`** saved to **`{}`**'.format(url, path))
    
    @commands.command()
    @commands.is_owner()
	async def pm(self, ctx, users: Greedy[User], *, message: str):
		for user in users:
			await user.send(message)
			await ctx.message.add_reaction('👌')

    @commands.command(aliases=['quit'], hidden=True)
    @commands.is_owner()    
    async def shutdown(self, ctx):
        '''Turn me off :( (BOT OWNER ONLY)'''
        await ctx.send('**👌🏼** Bye!')
        #self.bot.gamesLoop.cancel()
        await self.bot.logout()
        sys.exit(0)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def restart(self, ctx):
        ''''Restart me (BOT OWNER ONLY)'''
        await ctx.send('**👌🏼** See you soon!')
        try:
                await self.bot.logout()
        except:
            pass
        finally:
            os.system("python3 GoddessBlackHeartBot.py")
        await ctx.send('**👌🏼** Restart Successful!')

    @commands.command()
    @commands.is_owner()
    async def ls(self, ctx, path: str):
        ``````
            '''Lists Files from path on Hard Drive'''
            await ctx.send(os.listdir(path))
        await ctx.send('✅ list of files in **`{}`**'.format(path))

    @commands.command()
    @commands.is_owner()
    async def cat(self, ctx, file: str):
        ``````
            '''Lists Files from path on Hard Drive'''
            with open(file, 'rb') as f:
                f_contents = f.read()
                await ctx.send(f_contents)
        await ctx.send('✅ listed contents in **`{}`**'.format(file))

    @commands.command()
    @commands.is_owner()
    async def touch(self, ctx, text: str, file: str):
        ``````
            '''Writes Text to Files from path on Hard Drive'''
            with open(file, 'a+') as f:
                f_contents = f.write((text) + "\r\n")
        await ctx.send('✅ wrote test to file in **`{}`**'.format(file))

    @commands.command()
    @commands.is_owner()
    async def rm(self, ctx, file: str):
        ``````
            '''Removes Files from path on Hard Drive'''
            os.remove(file)
        await ctx.send('✅ removed **`{}`**'.format(file))

    @commands.command()
    @commands.is_owner()
    async def cmd(self, ctx, cmd: str):
        ``````
            '''Runs command from the computers command and directs the output to Discord'''
        # returns output as byte string
        returned_output = subprocess.check_output(cmd, shell=True)

        # using decode() function to convert byte string to string
        await ctx.send(f'```py\n{returned_output}\b```')
        await ctx.send('✅ command **`{}`** ran'.format(cmd))

    @commands.command()
    @commands.is_owner()
    async def sfuser(self, ctx, userid: str, path: str):
        ``````
            '''Sends Files in path to user from Hard Drive'''
            user = self.bot.get_user(int(userid))
        await user.send(file=discord.File(path))
        await ctx.send('✅ sent **`{}`** to **`<#{}>`**'.format(path, userid))

    @commands.command()
    @commands.is_owner()
    async def sfch(self, ctx, channelid: str, path: str):
        ``````
            '''Sends Files in path to channel from Hard Drive'''
            ch = self.bot.get_channel(int(channelid))
        await ch.send(file=discord.File(path))
        await ctx.send('✅ sent **`{}`** to **`<#{}>`**'.format(path, channelid))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def botavatar(self, ctx, url: str):
        '''Set a new avatar (BOT OWNER ONLY)'''
        tempBHFile = 'tempBH.png'
        r = requests.get(url)
        with open(tempBHFile, 'wb') as f:
                total_length = int(r.headers.get('content-length'))
                for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                    if chunk:
                        f.write(chunk)
                        f.flush()
        with open('tempBH.png', 'rb') as f:
                await self.bot.user.edit(avatar=f.read())
        os.remove(tempBHFile)
        asyncio.sleep(2)
        await ctx.send('**👌🏼** My new avatar!\n %s' % self.bot.user.avatar_url)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def servericon(self, ctx, url: str):
        '''Set a new avatar (BOT OWNER ONLY)'''
        tempsvicon = 'tempsvicon.png'
        r = requests.get(url)
        with open('tempsvicon.png', 'wb') as f:
                total_length = int(r.headers.get('content-length'))
                for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                    if chunk:
                        f.write(chunk)
                        f.flush()
        with open('tempsvicon.png', 'rb') as f:
                await ctx.guild.edit(icon=f.read())
        os.remove(tempsvicon)
        asyncio.sleep(2)
        await ctx.send('**👌🏼** New Server Icon set!') #\n %s' % self.bot.user.avatar_url)

    @commands.command(hidden=True, aliases=['game'])
    @commands.is_owner()
    async def changegame(self, ctx, status: str, gameType: str, *, gameName: str):
        ``````
            '''Changes the game currently playing (BOT OWNER ONLY)'''
        gameType = gameType.lower()
        if gameType == 'playing':
            type2 = discord.ActivityType.playing
        elif gameType == 'watching':
            type2 = discord.ActivityType.watching
        elif gameType == 'listening':
            type2 = discord.ActivityType.listening
        elif gameType == 'streaming':
            type2 = discord.ActivityType.streaming
        status = status.lower()
        if status == 'offline' or status == 'off' or status == 'invisible':
            discordStatus = discord.Status.invisible
        elif status == 'idle':
            discordStatus = discord.Status.idle
        elif status == 'dnd' or status == 'disturb':
            discordStatus = discord.Status.dnd
        else:
            discordStatus = discord.Status.online
        guildsCount = len(self.bot.guilds)
        memberCount = len(list(self.bot.get_all_members()))
        gameName = gameName.format(guilds = guildsCount, members = memberCount)
        await self.bot.change_presence(status=discordStatus, activity=discord.Activity(type=type2, name=gameName))
        await ctx.send(f'**👌🏼** Changed the status & game to: **{discordStatus}** {gameType} **{gameName}**')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def changestatus(self, ctx, status: str):
        ``````
            '''Changes bot online status (BOT OWNER ONLY)'''
        status = status.lower()
        if status == 'offline' or status == 'off' or status == 'invisible':
            discordStatus = discord.Status.invisible
        elif status == 'idle':
            discordStatus = discord.Status.idle
        elif status == 'dnd' or status == 'disturb':
            discordStatus = discord.Status.dnd
        else:
            discordStatus = discord.Status.online
        await self.bot.change_presence(status=discordStatus)
        await ctx.send(f'**👌🏼** to another status: **{discordStatus}**')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def name(self, ctx, name):
        ``````
            '''changes bot global name (BOT OWNER ONLY)'''
        await self.bot.user.edit(username=name)
        msg = f'👌🏼 change my name: **{name}**'
        await ctx.send(msg)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def servername(self, ctx, name):
        ``````
            '''changes server global name (BOT OWNER ONLY)'''
        await ctx.guild.edit(name=name)
        msg = f'👌🏼 change server name: **{name}**'
        await ctx.send(msg)

    @commands.command(hidden=True, aliases=['guilds'])
    @commands.is_owner()
    async def servers(self, ctx):
        '''Lists the current connected guilds (BOT OWNER ONLY)'''
        msg = '```js\n'
        msg += '{!s:19s} | {!s:>5s} | {} | {}\n'.format('ID', 'Member', 'Name', 'Owner')
        for guild in self.bot.guilds:
            msg += '{!s:19s} | {!s:>5s}| {} | {}\n'.format(guild.id, guild.member_count, guild.name, guild.owner)
        msg += '```'
        await ctx.send(msg)


    @commands.command(hidden=True)
    @commands.is_owner()
    async def leaveserver(self, ctx, guildid: str):
        ``````
            '''Leaves a server (BOT OWNER ONLY)
        Example:
        -----------
        : leaveserver 102817255661772800
        '''
        if guildid == 'this':
            await ctx.guild.leave()
            return
        else:
            guild = self.bot.get_guild(int(guildid))
            if guild:
                await guild.leave()
                msg = "👌🏼 Exit from: **{}** **{}** successful!".format(guild.name, guild.id)
            else:
                msg = f":x: Couldn't find a matching guild for this ID!"
        await ctx.send(msg)


    @commands.command(hidden=True)
    @commands.is_owner()
    async def echo(self, ctx, channel: str, *message: str):
        '''Outputs a message as a bot on a specific channel (BOT OWNER ONLY)'''
        ch = self.bot.get_channel(int(channel))
        msg = ' '.join(message)
        await ch.send(msg)
        await ctx.message.delete()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def discriminator(self, ctx, disc: str):
        '''Returns users with the respective discriminator'''

        discriminator = disc
        memberList = ''

        for guild in self.bot.guilds:
            for member in guild.members:
                if member.discriminator == discriminator and member.discriminator not in memberList:
                    memberList += f'{member}\n'

        if memberList:
            await ctx.send(memberList)
        else:
            await ctx.send(":x: Couldn't find anyone")

    @commands.command(hidden=True)
    @commands.is_owner()
    @commands.bot_has_permissions(manage_nicknames = True)
    async def nickname(self, ctx, *name):
        '''Changes the server nickname from the bot (BOT OWNER ONLY)'''
        nickname = ' '.join(name)
        await ctx.me.edit(nick=nickname)
        if nickname:
            msg = f'👌🏼 Change my server nickname: **{nickname}**'
        else:
            msg = f'👌🏼 Reset from my server nickname: **{ctx.me.name}**'
        await ctx.send(msg)

    @commands.command(hidden=True)
    @commands.is_owner()
    @commands.bot_has_permissions(manage_nicknames = True)
    async def setnickname(self, ctx, member: discord.Member=None, *name):
        '''Changes a user's nickname (BOT OWNER ONLY)'''
        if member == None:
            member = ctx.author
        nickname = ' '.join(name)
        await member.edit(nick=nickname)
        if nickname:
            msg = f'👌🏼 Change nickname of {member} to: **{nickname}**'
        else:
            msg = f'👌🏼 Reset nickname for {member} on: **{member.name}**'
        await ctx.send(msg)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def serverimage(self, ctx, guildid: str):
        '''Grabs icon from a guild if possible (BOT OWNER ONLY)'''
        server = self.bot.get_guild(int(guildid))
        await ctx.send(server.icon_url)
        await ctx.send('✅ Server icon from **`{}`**'.format(guildid))

    @commands.command()
    @commands.is_owner()
    async def lschannels(self, ctx, guildid: str):
        logfile = 'channel.ids.txt'
        server = self.bot.get_guild(int(guildid))
        log = open(logfile,"w+")
        ids = server.channels
        log.write("" + str(ids)  + "\r\n")
        log.close()
        await ctx.send(file=discord.File(logfile))
        await ctx.send('✅ sent **`{}`** from **`{}`**'.format(logfile, server))

    @commands.command()
    @commands.is_owner()
    async def lsusers(self, ctx, guildid: str):
        logfile = 'user.ids.txt'
        server = self.bot.get_guild(int(guildid))
        log = open(logfile,"w+")
        ids = server.members
        log.write("" + str(ids)  + "\r\n")
        log.close()
        await ctx.send(file=discord.File(logfile))
        await ctx.send('✅ sent **`{}`** from **`{}`**'.format(logfile, server))

    @commands.command(hidden=True)
    @commands.is_owner()
    @commands.bot_has_permissions(create_instant_invite = True)
    async def geninvite(self, ctx, channelid: str, userid: str):
        '''Generates an invite for a guild if possible (BOT OWNER ONLY)'''
        guild = self.bot.get_channel(int(channelid))
        user = self.bot.get_user(int(userid))
        invite = await guild.create_invite(unique=False)
        msg = f'Invite for **{guild.name}** ({guild.id})\n{invite.url}'
        await user.send(msg)

    @commands.command()
    @commands.is_owner()
    async def blacklist(self, ctx, id=None):
        if not self.bot.usedatabase:
            await ctx.send('This command requires a running database to work.')
            return
        elif id is None:
            await ctx.send('You need a user ID.')
            return
        check_blacklist = 'SELECT blacklist FROM users WHERE id = $1'
        temp = await self.bot.db.fetchval(check_blacklist, int(id))
        if not temp:
            await ctx.send('This user is not in the database.')
            return
        blacklist_value = int(temp)
        new_value = 0 if blacklist_value != 0 else 1
        sql = 'UPDATE users SET blacklist = $1 where id = $2'
        await self.bot.db.execute(sql, str(new_value), int(id))
        if new_value == 0:
            await ctx.send('User has been removed from the blacklist.')
        else:
            await ctx.send('User has been added to the blacklist.')


def setup(bot):
    bot.add_cog(Debug(bot))
