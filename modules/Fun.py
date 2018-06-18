import discord
from discord.ext import commands
import random
import requests


class Fun:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, meme):
        await meme.send("This feature has not been implemented yet.")

    @commands.command(aliases=['ask'],name='8ball')
    async def _8ball(self, ctx, *, question):
        responses = [['Yes, definitely.', 'Of course! Bill Cipher would agree!', 'Did an iDroid program me?', 'The answer is simple: 25-5-19',
                      'Did Donald Trump get started on that wall?', 'Absolutely, you weirdo!', 'I am as positive as there is 24 KARAT MAGIC IN THE AIR!!!',
                      '**Yes.**', 'BHV'],
                     ['Reply hazy, try again later.', 'I am unable to answer this right now.',
                      'You\'ll have to ask again later.', 'Is it Saturday Night yet?', 'I do not know. Perhaps Donald Trump can answer this.',
                      'I am certain there is not an answer for this.', 'Why are you asking me about this?', 'Hold on. I\'m playing \"Doki Doki Literature Club\" right now.',
                      'Are you living in a van down by the river?', '```I AM ERROR```'],
                     ['Absolutely not.', 'Here\'s my answer: What\'s at the beginning of \"Never\" and what comes after that?',
                      'Did Ultron defeat the Avengers?', 'Is Hydra still operating?', 'Did Hillary Clinton win the presidency?',
                      '**No.**', 'The answer to that question is also the answer to you surviving a fall from 10,000 feet.',
                      'Pffft. Of course not.']]
        await ctx.send(random.choice(random.choice(responses)))

    @commands.command()
    async def kiss(self, ctx, user: discord.User):
        url = 'https://nekos.life/api/v2/img/kiss'
        image = getImage(url)
        embed = discord.Embed(title="{} has kissed {}. Weird...".format(ctx.message.author.name, user.name))
        embed.set_image(url=image)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def hug(self, ctx, user: discord.User):
    	url = 'https://nekos.life/api/v2/img/hug'
    	image = getImage(url)
    	embed = discord.Embed(title="{} hugged {}. How comforting.".format(ctx.message.author.name, user.name))
    	embed.set_image(url=image)
    	await ctx.send(embed=embed)
    	
    def getImage(self, url):
    	response = requests.get(url)
    	image = response.json()
    	image = image.get('url')
    	return image


def setup(bot):
    bot.add_cog(Fun(bot))