import discord
from discord.ext import commands
import random
import requests
import aiohttp


class Fun:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, meme):
        await meme.send("This feature has not been implemented yet.")

    @commands.command(aliases=['ask'], name='8ball')
    async def _8ball(self, ctx, *, question):
        responses = [['Yes, definitely.', 'Of course! Bill Cipher would agree!', 'Did an iDroid program me?',
                      'The answer is simple: 25-5-19',
                      'Did Donald Trump get started on that wall?', 'Absolutely, you weirdo!',
                      'I am absolutely certain about your question and that Hillary Clinton lost fair and square.',
                      '**Yes.**', 'BHV', 'Sure. Why not?'],
                     ['Reply hazy, try again later.', 'I am unable to answer this right now.',
                      'You\'ll have to ask again later.', 'I don\'t know. I just want to watch \"Saturday Night Live.\"',
                      'I do not know. Perhaps Donald Trump can answer this.',
                      'I am certain there is not an answer for this.', 'Why are you asking me about this?',
                      'Hold on. I\'m playing \"Doki Doki Literature Club\" right now.',
                      'Go ask the man living ***IN A VAN DOWN BY THE RIVER!!!***', '```I AM ERROR```'],
                     ['Absolutely not.',
                      'Here\'s my answer: What\'s at the beginning of \"Never\" and what comes after that?',
                      'Is Hydra still operating?', 'Did Hillary Clinton win the presidency?', '**No.**',
                      'The answer to that question is also the answer to you surviving a fall from 10,000 feet.',
                      'Pffft. Of course not.']]
        await ctx.send(random.choice(random.choice(responses)))

    @commands.command()
    async def kiss(self, ctx):
        try:
            user = ctx.message.mentions[0]
        except Exception:
            ctx.send("Please specify a user.")
            return
        url = 'https://nekos.life/api/v2/img/kiss'
        image = self.getImage(url)
        embed = discord.Embed(title="{} has kissed {}. Weird...".format(ctx.message.author.name, user.name))
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @commands.command()
    async def hug(self, ctx):
        try:
            user = ctx.message.mentions[0]
        except Exception:
            ctx.send("Please specify a user.")
        url = 'https://nekos.life/api/v2/img/hug'
        image = self.getImage(url)
        embed = discord.Embed(title="{} hugged {}. How comforting.".format(ctx.message.author.name, user.name))
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @commands.command()
    async def urban(self, ctx, *, term):
        if not ctx.message.channel.is_nsfw():
            await ctx.send("Due to the fact that some definitions are not appropriate, this command can only be used in NSFW channels.")
            return
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('http://api.urbandictionary.com/v0/define?term={}'.format(term)) as entry:
                    entry = await entry.json()
                    entry = entry.get('list')[0]
        except Exception:
            await ctx.send("That term could not be found on Urban Dictionary.")
            return
        word = entry.get('word')
        definition = str(entry.get("definition"))
        example = str(entry.get("example"))
        link = str(entry.get("permalink"))
        author = str(entry.get("author"))
        thumbsup = str(entry.get("thumbs_up"))
        thumbsdown = str(entry.get("thumbs_down"))
        embed = discord.Embed(color=discord.Colour.lighter_grey(), title="{}".format(word), url=link,
                              description=definition)
        if len(example) == 0:
            embed.add_field(name="Example: ", value="There's no example for this term.", inline=False)
        elif len(example) >= 1024:
            example = example[:1021]
            embed.add_field(name="Example: ", value=example + "...", inline=False)
        else:
            embed.add_field(name="Example: ", value=example, inline=False)
        embed.add_field(name=":thumbsup: ", value=thumbsup + " liked this.")
        embed.add_field(name=":thumbsdown: ", value=thumbsdown + " disliked this.")
        embed.set_footer(text="{} wrote this definition on Urban Dictionary.".format(author))
        await ctx.send(embed=embed)

    def getImage(self, url):
        response = requests.get(url)
        image = response.json()
        image = image.get('url')
        return image


def setup(bot):
    bot.add_cog(Fun(bot))
