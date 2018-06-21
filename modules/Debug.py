import discord
from discord.ext import commands


class Debug:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reload(self, ctx, *, module):
        """Reloads a module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send(':ok_hand:')

    @commands.command()
    async def load(self, ctx, *, module):
        """Loads a module. Useful if new modules were added."""
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send(':ok_hand:')


def setup(bot):
    bot.add_cog(Debug(bot))
