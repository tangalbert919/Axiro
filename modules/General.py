import discord
from discord.ext import commands

class General:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def _help(self, beep):
        embed = discord.Embed(title="Hi! I am a bot being built!",
                              description="So here is my current list of commands:")
        embed.add_field(name="General:\n", value="``help`` ``test`` ``about``", inline=False)
        embed.add_field(name="Anime:\n", value="``danbooru`` ``safebooru`` ``konachan`` ``neko``", inline=False)
        embed.add_field(name="Encryption:\n", value="``encode`` ``decode`` ``encipher`` ``decipher``", inline=False)
        embed.add_field(name="Fun:\n", value="``8ball`` ``ask`` ``kiss`` ``hug``", inline=False)
        embed.add_field(name="Moderation:\n", value="``kick`` ``ban`` ``mute``", inline=False)
        await beep.send(embed=embed)

    @commands.command()
    async def test(self, beep):
        await beep.send('Testing, testing...')

    @commands.command()
    async def about(self, beep):
        embed = discord.Embed(title="About the Weirdness Bot:", description="This bot was created to do what most "
                                                                            "bots should do, and then some really "
                                                                            "weird things.")
        embed.add_field(name="Author: ", value="tangalbert919 (The Freaking iDroid)")
        await beep.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))
