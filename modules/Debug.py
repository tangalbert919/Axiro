import discord
from discord.ext import commands


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
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
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


def setup(bot):
    bot.add_cog(Debug(bot))
