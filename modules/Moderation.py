import discord
from discord.ext import commands


class Moderation:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.User, *, reason: str):
        try:
            await ctx.message.guild.kick(user, reason=reason)
        except Exception:
            await ctx.send("Player kick failed.")
            return
        await ctx.send("Player {} has been kicked from the server.".format(user.name))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.User, *, reason: str):
        try:
            await ctx.message.guild.ban(user, reason=reason)
        except Exception:
            await ctx.send("I completely failed to ban that player.")
            return
        await ctx.send("Player {} has been banned from the server.".format(user.name))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user, *, reason: str):
        try:
            await ctx.message.guild.unban(user, reason=reason)
        except Exception:
            await ctx.send("I completely failed to unban that player.")
            return
        await ctx.send("Player {} has been unbanned from the server.".format(user))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: discord.User, *, reason: str):
        await ctx.send("This feature has not been built yet.")


def setup(bot):
    bot.add_cog(Moderation(bot))