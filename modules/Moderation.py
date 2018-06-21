import discord
from discord.ext import commands


class Moderation:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, user: discord.User, *, reason):
        await ctx.send("This feature has not been built yet.")

    @commands.command()
    async def ban(self, ctx, user: discord.User, *, reason):
        await ctx.send("This feature has not been built yet.")

    @commands.command()
    async def mute(self, ctx, user: discord.User, *, reason):
        await ctx.send("This feature has not been built yet.")


def setup(bot):
    bot.add_cog(Moderation(bot))