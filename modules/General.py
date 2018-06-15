import discord
from discord.ext import commands

class General:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def _help(self, beep):
        embed = discord.Embed(title="Hi! I am a bot being built!",
                              description="I am currently being built by my creator, so feel free to ignore me right now. :(")
        await beep.send(embed=embed)

    @commands.command()
    async def test(self, beep):
        await beep.send('Testing, testing...')

def setup(bot):
    bot.add_cog(General(bot))