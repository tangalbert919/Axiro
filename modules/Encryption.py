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
            await ctx.send(crypto[2:-1])
        elif "binary".lower() in target:
            crypto = ' '.join(format(ord(x), 'b') for x in message)
            print(crypto)
            await ctx.send(crypto)

    @commands.command()
    async def decode(self, ctx, target, message):
        if "base64".lower() in target:
            decoded = str(base64.b64decode(bytes(message, 'utf-8')))
            print(decoded)
            await ctx.send(decoded)


def setup(bot):
    bot.add_cog(Encryption(bot))