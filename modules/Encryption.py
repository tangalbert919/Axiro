import discord
from discord.ext import commands
import base64
import binascii


class Encryption:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def encode(self, ctx, target, *, message: str):
        if "base64".lower() in target:
            crypto = str(base64.b64encode(bytes(message, 'utf-8')))
            print(crypto)
            await ctx.send(crypto[2:-1])
        elif "binary".lower() in target:
            crypto = ' '.join(format(ord(x), 'b') for x in message)
            print(crypto)
            await ctx.send(crypto)
        else:
            await ctx.send('That is not a valid target.')

    @commands.command()
    async def decode(self, ctx, target, *, message: str):
        if "base64".lower() in target:
            decoded = str(base64.b64decode(bytes(message, 'utf-8')))
            print(decoded)
            await ctx.send(decoded[2:-1])
        elif "binary".lower() in target:
            """This currently does not work."""
            # decoded = ''.join(chr(int(message[i*8:i*8+8],2)) for i in range(len(message)//8))
            decoded = binascii.b2a_qp(message)
            print(decoded)
            await ctx.send(decoded)
        else:
            await ctx.send('That is not a valid target.')

    @commands.command()
    async def encipher(self, ctx, target, *, message: str):
        if "caesar".lower() in target:
            L2I = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", range(26)))
            I2L = dict(zip(range(26), "ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
            key = 3
            ciphertext = ""
            for c in message.upper():
                if c.isalpha():
                    ciphertext += I2L[(L2I[c] + key) % 26]
                else:
                    ciphertext += c
            await ctx.send(ciphertext)
        else:
            await ctx.send('That\'s not a valid cipher option.')

    @commands.command()
    async def decipher(self, ctx, target, *, message: str):
        if "caesar".lower() in target:
            L2I = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", range(26)))
            I2L = dict(zip(range(26), "ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
            key = 3
            plaintext = ""
            for c in message.upper():
                if c.isalpha():
                    plaintext += I2L[(L2I[c] - key) % 26]
                else:
                    plaintext += c
            await ctx.send(plaintext)
        else:
            await ctx.send('That\'s not a valid cipher option.')


def setup(bot):
    bot.add_cog(Encryption(bot))
