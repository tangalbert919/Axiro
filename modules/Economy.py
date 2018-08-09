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
            await ctx.send(":gem: **Balance of {}: ${}**".format(ctx.message.author.name, money))
        else:
            await ctx.send(":gem: **Your balance: ${}**".format(money))

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def pay(self, ctx):
        await ctx.send("This feature has not been implemented yet.")

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
            await ctx.send("You just got 100 credits.")

    @commands.command()
    @commands.cooldown(1, 604800, BucketType.user)
    async def weekly(self, ctx):
        await ctx.send("This feature has not been implemented yet.")


def setup(bot):
    bot.add_cog(Economy(bot))