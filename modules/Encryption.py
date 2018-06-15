import discord
from discord.ext import commands
import base64

class Encryption:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def encode(self, ctx, target, message):
        if "base64".lower() in target:
            crypto = str(base64.b64encode(bytes(message, 'utf-8')))
            print(crypto)
            await ctx.send(crypto)
        elif "binary".lower() in target:
            crypto = ' '.join(format(ord(x), 'b') for x in message)
            print(crypto)
            await ctx.send(crypto)

def setup(bot):
    bot.add_cog(Encryption(bot))