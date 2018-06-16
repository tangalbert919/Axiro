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

    @commands.command()
    async def about(self, beep):
        embed = discord.Embed(title="About the Weirdness Bot:", description="This bot was created to do what most bots should do, and then some really weird things.")
        embed.add_field(name="Version: ", value="1.0.0 Alpha \"Axiro\"")
        embed.add_field(name="Author: ", value="tangalbert919 (The Freaking iDroid)")
        await beep.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))