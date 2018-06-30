import discord
from discord.ext import commands


class Economy:

    def __init__(self, bot):
        self.bot = bot

    async def balance(self, ctx):
        await ctx.send("This feature has not been implemented yet.")

    async def pay(self, ctx):
        await ctx.send("This feature has not been implemented yet.")

    async def gamble(self, ctx):
        await ctx.send("This feature has not been implemented yet.")

    async def daily(self, ctx):
        await ctx.send("This feature has not been implemented yet.")

    async def weekly(self, ctx):
        await ctx.send("This feature has not been implemented yet.")


def setup(bot):
    bot.add_cog(Economy(bot))