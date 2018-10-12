import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType


class Moderation:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 5, BucketType.user)
    async def kick(self, ctx, user: discord.User, *, reason: str):
        if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).kick_members:
            await ctx.send(":x: I do not have permission to kick players.")
            return
        try:
            await ctx.message.guild.kick(user, reason=reason)
        except Exception:
            await ctx.send(":x: Player kick failed.")
            return
        await ctx.send(":white_check_mark: Player {} has been kicked from the server.".format(user.name))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, BucketType.user)
    async def ban(self, ctx, user: discord.User, *, reason: str):
        if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).ban_members:
            await ctx.send(":x: I do not have permission to ban players.")
            return
        try:
            await ctx.message.guild.ban(user, reason=reason)
        except Exception:
            await ctx.send(":x: I completely failed to ban that player.")
            return
        await ctx.send(":white_check_mark: Player {} has been banned from the server.".format(user.name))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, BucketType.user)
    async def mute(self, ctx, user: discord.Member):
        if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).manage_roles:
            await ctx.send(":x: I do not have permission to manage roles.")
            return
        try:
            await ctx.message.channel.category.set_permissions(user, send_messages=False)
        except Exception:
            await ctx.send("I was unable to mute that player.")
            return
        await ctx.send(":white_check_mark: Player {} has been muted.".format(user.display_name))


def setup(bot):
    bot.add_cog(Moderation(bot))