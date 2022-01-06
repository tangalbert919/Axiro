import asyncio
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType


class Moderation(commands.Cog, name='Moderation'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def kick(self, ctx, user: discord.User, *, reason: str):
        if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).kick_members:
            return await ctx.send(':x: I do not have permission to kick players.')
        try:
            await ctx.message.guild.kick(user, reason=reason)
        except Exception:
            return await ctx.send(':x: Player kick failed.')
        await ctx.send(f':white_check_mark: Player {user.name} has been kicked from the server.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def ban(self, ctx, user, *, reason=None):
        if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).ban_members:
            return await ctx.send(':x: I do not have permission to ban players.')
        try:
            user = ctx.message.mentions[0]
        except IndexError: # Mentioned user is not present in the server.
            pass

        # If an ID was specified, get a User object with it.
        try:
            user = await self.bot.fetch_user(user)
        except:
            return await ctx.send('Either the player mentioned is not present in the server, or their ID is incorrect.')

        # Now attempt to ban them.
        try:
            await ctx.guild.ban(user, reason=reason)
            await ctx.send(f':white_check_mark: <@{user.id}> is now banned.')
        except (discord.Forbidden, discord.HTTPException):
            await ctx.send(':negative_squared_cross_mark: I was unable to ban that player.')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def mute(self, ctx, user: discord.User):
        if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).manage_roles:
            return await ctx.send(':x: I do not have permission to manage roles.')
        try:
            await ctx.message.channel.category.set_permissions(user, send_messages=False, add_reactions=False)
        except Exception:
            return await ctx.send('I was unable to mute that player.')
        await ctx.send(f':white_check_mark: Player {user.name} has been muted.')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def unmute(self, ctx, user: discord.User):
        if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).manage_roles:
            return await ctx.send(':x: I do not have permission to manage roles.')
        try:
            await ctx.message.channel.category.set_permissions(user, overwrite=None)
        except Exception:
            return await ctx.send('I was unable to unmute that player.')
        await ctx.send(f':white_check_mark: Player {user.name} has been unmuted.')

    @commands.command()
    @commands.has_permissions(ban_members = True)
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def unban(self, ctx, user: int = None, *, reason=None):
        if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).ban_members:
             return await ctx.send(':x: I do not have permission to unban players.')
        if user is None:
            return await ctx.send('Please provide the user\'s ID to unban them.')
        else:
            try:
                user = await self.bot.fetch_user(user)
            except:
                return await ctx.send('I cannot find the user with that ID. Perhaps it is incorrect?')
        try:
            await ctx.guild.unban(user, reason=reason)
            await ctx.send(f':white_check_mark: Successfully unbanned the user: <@{user.id}>.')
        except (discord.Forbidden, discord.HTTPException):
            await ctx.send(':negative_squared_cross_mark: I was unable to unban that player.')
    
    @commands.command(aliases=['banlist'])
    @commands.has_permissions(kick_members = True, ban_members = True)
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def bans(self, ctx):
        '''Lists currently banned users (MOD ONLY)'''
        users = await ctx.guild.bans()
        if len(users) > 0:
            msg = f'`{"ID":21}{"Name":25} Reason\n'
            for entry in users:
                userID = entry.user.id
                userName = str(entry.user)
                if entry.user.bot:
                    username = '🤖' + userName #:robot: emoji
                reason = str(entry.reason) #Could be None
                msg += f'{userID:<21}{userName:25} {reason}\n'
            embed = discord.Embed(color=0xe74c3c) #Red
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(text=f'Server: {ctx.guild.name}')
            embed.add_field(name='Ranks', value=msg + '`', inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send('**:negative_squared_cross_mark:** There are no banned users!')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 10, BucketType.guild)
    @commands.guild_only()
    async def prune(self, ctx, number: int):
        if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).manage_messages:
            return await ctx.send('I do not have permission to delete messages.')
        to_delete = []
        async for message in ctx.message.channel.history(limit=number+1):
            to_delete.append(message)
        while to_delete:
            if len(to_delete) > 1:
                await ctx.message.channel.delete_messages(to_delete[:50])
                to_delete = to_delete[50:]
            else:
                await to_delete.delete()
                to_delete = []
            await asyncio.sleep(5)


def setup(bot):
    bot.add_cog(Moderation(bot))