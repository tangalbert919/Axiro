import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType


class Economy:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def balance(self, ctx):
        try:
            user = ctx.message.mentions[0]
        except Exception:
            user = ctx.message.author
        if user.id == self.bot.user.id:
            await ctx.send("I do not need money, since I'm a bot.")
            return
        sql = "SELECT money FROM users WHERE id = $1"
        temp = await self.bot.db.fetchval(sql, user.id)
        money = int(temp)
        if user.id != ctx.message.author.id:
            await ctx.send(":chicken: **{} has {} chickens.**".format(user.name, money))
        else:
            await ctx.send(":chicken: **You have {} chickens.**".format(money))

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def pay(self, ctx, user: discord.User, payment):
        try:
            check = int(payment)
        except Exception:
            ctx.send("Please specify an actual amount.")
        if user.id == self.bot.user.id:
            await ctx.send("You can't give me money, since I'm a bot.")
            return
        sql = "SELECT money FROM users WHERE id = $1"
        payer = await self.bot.db.fetchval(sql, ctx.message.author.id)
        receiver = await self.bot.db.fetchval(sql, user.id)
        money = int(payer)
        money_two = int(receiver)
        if money < check:
            await ctx.send("You do not have enough chickens to perform this payment.")
            return
        elif check < 0:
            await ctx.send("Using negative numbers will not work.")
            return
        paid = money - check
        paid_two = money_two + check
        next_sql = "UPDATE users SET money = $1 WHERE id = $2"
        await self.bot.db.execute(next_sql, str(paid), ctx.message.author.id)
        await self.bot.db.execute(next_sql, str(paid_two), user.id)
        await ctx.send("Successfully paid ${} to {}".format(payment, user.name))

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def gamble(self, ctx):
        await ctx.send("This feature has not been implemented yet.")

    @commands.command()
    @commands.cooldown(1, 86400, BucketType.user)
    async def daily(self, ctx):
        try:
            user = ctx.message.mentions[0]
        except Exception:
            user = ctx.message.author
        if user.id == self.bot.user.id:
            user = ctx.message.author
        sql = "SELECT money FROM users WHERE id = $1"
        temp = await self.bot.db.fetchval(sql, user.id)
        money = int(temp) + 100
        next_sql = "UPDATE users SET money = $1 WHERE id = $2"
        await self.bot.db.execute(next_sql, str(money), user.id)
        if user.id != ctx.message.author.id:
            await ctx.send("You just gave your ${} to {}".format(money, ctx.message.author.name))
        else:
            await ctx.send("You just got 100 chickens.")

    @commands.command()
    @commands.cooldown(1, 604800, BucketType.user)
    async def weekly(self, ctx):
        await ctx.send("This feature has not been implemented yet.")


def setup(bot):
    bot.add_cog(Economy(bot))