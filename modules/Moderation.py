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
            await ctx.send(':x: I do not have permission to kick players.')
            return
        try:
            await ctx.message.guild.kick(user, reason=reason)
        except Exception:
            await ctx.send(':x: Player kick failed.')
            return
        await ctx.send(f':white_check_mark: Player {user.name} has been kicked from the server.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def ban(self, ctx, user: int = None, *, reason=None):
        '''Bans a member with a reason (MOD ONLY)
        The user ID must be specified, name + discriminator is not enough
        example:
        -----------
        :ban 102815825781596160
        '''
        if user is None:
            return await ctx.send("Please provide the user's ID to ban him.")
        elif len(str(user)) > 18 or len(str(user)) < 18:
            return await ctx.send("Please provide a valid user's ID")
        try:
            await ctx.guild.ban(discord.Object(user), reason=reason)
            await ctx.send(":white_check_mark: Successfully banned the user: <@{}>.".format(user))
        except (discord.Forbidden, discord.HTTPException):
            await ctx.send(":negative_squared_cross_mark: ban failed! or No user specified!")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def mute(self, ctx, user: discord.User):
        if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).manage_roles:
            await ctx.send(':x: I do not have permission to manage roles.')
            return
        try:
            await ctx.message.channel.category.set_permissions(user, send_messages=False, add_reactions=False)
        except Exception:
            await ctx.send('I was unable to mute that player.')
            return
        await ctx.send(f':white_check_mark: Player {user.name} has been muted.')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def unmute(self, ctx, user: discord.User):
        if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).manage_roles:
            await ctx.send(':x: I do not have permission to manage roles.')
            return
        try:
            await ctx.message.channel.category.set_permissions(user, overwrite=None)
        except Exception:
            await ctx.send('I was unable to unmute that player.')
            return
        await ctx.send(f':white_check_mark: Player {user.name} has been unmuted.')

    @commands.command()
    @commands.has_permissions(ban_members = True)
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def unban(self, ctx, user: int = None, *, reason=None):
        """Unban a person from the guild"""
        if user is None:
            return await ctx.send("Please provide the user's ID to unban him.")
        elif len(str(user)) > 18 or len(str(user)) < 18:
            return await ctx.send("Please provide a valid user's ID")
        try:
            await ctx.guild.unban(discord.Object(user), reason=reason)
            await ctx.send(":white_check_mark: Successfully unbanned the user: <@{}>.".format(user))
        except (discord.Forbidden, discord.HTTPException):
            await ctx.send(":negative_squared_cross_mark: Unban failed! or No user specified!")
    
    @commands.command()
    @commands.has_permissions(kick_members = True)
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
    @commands.cooldown(1, 10, BucketType.guild)
    @commands.guild_only()
    async def hierarchy(self, ctx):
        '''Lists the role hierarchy of the current server'''
        msg = f'Role hierarchy for servers **{ctx.guild}**:\n\n'
        roleDict = {}

        for role in ctx.guild.roles:
            if role.is_default():
                roleDict[role.position] = 'everyone'
            else:
                roleDict[role.position] = role.name

        for role in sorted(roleDict.items(), reverse=True):
            msg += role[1] + '\n'
        await ctx.send(msg)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 10, BucketType.guild)
    @commands.guild_only()
    async def prune(self, ctx, number: int):
        if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).manage_messages:
            await ctx.send('I do not have permission to delete messages.')
            return
        if number > 500:
            await ctx.send('Please specify a lower number.')
            return
        to_delete = []
        async for message in ctx.message.channel.history(limit=number+1):
            to_delete.append(message)
        while to_delete:
            if len(to_delete) > 1:
                await ctx.message.channel.delete_messages(to_delete[:100])
                to_delete = to_delete[100:]
            else:
                await to_delete.delete()
                to_delete = []
            await asyncio.sleep(1.5)


def setup(bot):
    bot.add_cog(Moderation(bot))