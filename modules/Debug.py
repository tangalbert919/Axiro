import discord
from discord.ext import commands
import io
from contextlib import redirect_stdout


class Debug:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reload(self, ctx, *, module):
        """Reloads a module."""
        if ctx.message.author.id != 310496481435975693:
            await ctx.send("Only my creator can run this command.")
            return
        try:
            self.bot.unload_extension("modules." + module)
            self.bot.load_extension("modules." + module)
        except Exception as e:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send(':ok_hand:')

    @commands.command()
    async def load(self, ctx, *, module):
        """Loads a new module."""
        if ctx.message.author.id != 310496481435975693:
            await ctx.send("Only my creator can run this command.")
            return
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send(':ok_hand:')

    @commands.command()
    async def say(self, ctx, *, message: str):
        if ctx.message.author.id != 310496481435975693:
            await ctx.send("Only my creator can run this command.")
            return
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
    async def eval(self, ctx, *, message: str):
        if ctx.message.author.id != 310496481435975693:
            await ctx.send("Only my creator can run this command.")
            return
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
        except Exception as e:
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


def setup(bot):
    bot.add_cog(Debug(bot))
