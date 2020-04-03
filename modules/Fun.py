import aiohttp, discord, json, random, requests
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from lxml import html


class Fun(commands.Cog, name='Fun'):

    def __init__(self, bot):
        self.bot = bot
        self.quotes = json.loads(open('quotes.json', 'r').read())

    @commands.command(aliases=['ask'], name='8ball')
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def _8ball(self, ctx, *, question):
        responses = [['Yes, definitely.', 'Of course! Bill Cipher would agree!', 'Did an iDroid program me?',
                      'The answer is simple: 25-5-19',
                      'My answer is the opposite of "no."', 'Absolutely, you weirdo!',
                      'I vote yes. What about you?',
                      '**Yes.**', 'BHV', 'Sure. Why not?'],
                     ['Reply hazy, try again later.', 'I am unable to answer this right now.',
                      'You\'ll have to ask again later.', 'I don\'t know. I just want to watch "Saturday Night Live."',
                      'I do not know. Perhaps Donald Trump can answer this.',
                      'I am certain there is not an answer for this.', 'Why are you asking me about this?',
                      'Hold on. I\'m playing "Doki Doki Literature Club" right now.',
                      'Go ask the man living ***IN A VAN DOWN BY THE RIVER!!!***', '```I AM ERROR```'],
                     ['Absolutely not.',
                      'Here\'s my answer: What\'s at the beginning of "Never" and what comes after that?',
                      'Keep wishing. Maybe you will get "yes" for an answer.', 'That\'s a definitive no.', '**No.**',
                      'The answer to that question is also the answer to you surviving a fall from 10,000 feet.',
                      'Pffft. Of course not.']]
        await ctx.send(random.choice(random.choice(responses)))

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def kiss(self, ctx, user: discord.User=None):
        if user is None:
            await ctx.send('Please specify a user.')
            return
        url = 'https://nekos.life/api/v2/img/kiss'
        image = self.getImage(url)
        embed = discord.Embed(title=f'{ctx.message.author.name} has kissed {user.name}. Weird...')
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def hug(self, ctx, user: discord.User=None):
        if user is None:
            await ctx.send('Please specify a user.')
            return
        url = 'https://nekos.life/api/v2/img/hug'
        image = self.getImage(url)
        embed = discord.Embed(title=f'{ctx.message.author.name} hugged {user.name}. How comforting.')
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def tickle(self, ctx, user: discord.User=None):
        if user is None:
            await ctx.send('Please specify a user.')
            return
        url = 'https://nekos.life/api/v2/img/tickle'
        image = self.getImage(url)
        embed = discord.Embed(title=f'{ctx.message.author.name} tickled {user.name}. They\'re having fun...')
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def poke(self, ctx, user: discord.User=None):
        if user is None:
            await ctx.send('Please specify a user.')
            return
        url = 'https://nekos.life/api/v2/img/poke'
        image = self.getImage(url)
        embed = discord.Embed(title=f'{ctx.message.author.name} poked {user.name}. Yikes.')
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def slap(self, ctx, user: discord.User=None):
        if user is None:
            await ctx.send('Please specify a user.')
            return
        url = 'https://nekos.life/api/v2/img/slap'
        image = self.getImage(url)
        embed = discord.Embed(title=f'{ctx.message.author.name} slapped {user.name}. Must\'ve been a real baka...')
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def cuddle(self, ctx, user: discord.User=None):
        if user is None:
            await ctx.send('Please specify a user.')
            return
        url = 'https://nekos.life/api/v2/img/cuddle'
        image = self.getImage(url)
        embed = discord.Embed(title=f'{ctx.message.author.name} cuddled {user.name}. How comforting.')
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def pat(self, ctx, user: discord.User=None):
        if user is None:
            await ctx.send('Please specify a user.')
            return
        url = 'https://nekos.life/api/v2/img/pat'
        image = self.getImage(url)
        embed = discord.Embed(title=f'{ctx.message.author.name} patted {user.name}. That\'s nice.')
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    @commands.is_nsfw()
    async def urban(self, ctx, *, term):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://api.urbandictionary.com/v0/define?term={term}') as entry:
                    entry = await entry.json()
                    entry = entry.get('list')[0]
        except Exception:
            await ctx.send('That term could not be found on Urban Dictionary.')
            return
        word = entry.get('word')
        definition = str(entry.get('definition'))
        example = str(entry.get('example'))
        link = str(entry.get('permalink'))
        author = str(entry.get('author'))
        thumbsup = str(entry.get('thumbs_up'))
        thumbsdown = str(entry.get('thumbs_down'))
        embed = discord.Embed(color=discord.Colour.lighter_grey(), title=f'{word}', url=link,
                              description=definition)
        if len(example) == 0:
            embed.add_field(name='Example: ', value='There\'s no example for this term.', inline=False)
        elif len(example) >= 1024:
            example = example[:1021]
            embed.add_field(name='Example: ', value=example + '...', inline=False)
        else:
            embed.add_field(name='Example: ', value=example, inline=False)
        embed.add_field(name=':thumbsup: ', value=thumbsup + ' liked this.')
        embed.add_field(name=':thumbsdown: ', value=thumbsdown + ' disliked this.')
        embed.set_footer(text=f'{author} wrote this definition on Urban Dictionary.')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def randomfact(self, ctx):
        """async with aiohttp.ClientSession() as session:
            async with session.get('https://www.cs.cmu.edu/~bingbin/index.html') as entry:
                tree = await html.fromstring(entry.content)"""
        page = requests.get('https://www.cs.cmu.edu/~bingbin/index.html')
        tree = html.fromstring(page.content)
        facts = tree.xpath('//p/text()')
        await ctx.send(facts[random.randint(0, len(facts))])

    @commands.command()
    @commands.cooldown(1, 3, BucketType.user)
    @commands.guild_only()
    async def randomquote(self, ctx):
        quote = self.quotes[str(random.randint(0, 10))]
        await ctx.send(quote)

    def getImage(self, url):
        response = requests.get(url)
        image = response.json()
        image = image.get('url')
        return image


def setup(bot):
    bot.add_cog(Fun(bot))
