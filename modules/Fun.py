from discord.ext import commands


class Fun:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, meme):
        await meme.send("This feature has not been implemented yet.")

def setup(bot):
    bot.add_cog(Fun(bot))