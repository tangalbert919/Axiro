from discord.ext import commands
import io
from contextlib import redirect_stdout
import subprocess
import textwrap
import traceback
import requests
from os import listdir
from os.path import isfile, join


class Debug(commands.Cog, command_attrs=dict(hidden=True), name="Debug"):

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, module):
        """Reloads a module."""
        try:
            self.bot.unload_extension("modules." + module)
            self.bot.load_extension("modules." + module)
        except Exception:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send(':ok_hand:')

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, module):
        """Loads a new module."""
        try:
            self.bot.load_extension("modules." + module)
        except Exception:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send(':ok_hand:')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, module):
        """Unloads a module."""
        try:
            self.bot.unload_extension("modules." + module)
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
            await ctx.send("Updating from Git failed.")
            return
        await ctx.send("Successfully updated from Git.")

    @commands.command()
    @commands.is_owner()
    async def download(self, ctx, link):
        file = [f for f in listdir('./modules/') if isfile(join('./modules/', f))]
        r = requests.get(link)
        newmod = open('./modules/{}.py'.format('module-{}'.format(len(file))), 'wb+')
        try:
            newmod.write(r.content)
        except:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        await ctx.send('Downloaded new module ending in {}'.format(len(file)))


def setup(bot):
    bot.add_cog(Debug(bot))
