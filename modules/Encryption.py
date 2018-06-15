import discord
from discord.ext import commands

class Encryption:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def encode(self, *ctx):
        return

def setup(bot):
    bot.add_cog(Encryption(bot))