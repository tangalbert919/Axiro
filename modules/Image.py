import aiohttp, discord, random, requests
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType


class Image(commands.Cog, name='Image'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def neko(self, ctx):
        if ctx.message.channel.is_nsfw():
            url = 'https://nekos.life/api/v2/img/lewd'
        else:
            url = 'https://nekos.life/api/v2/img/neko'
        response = requests.get(url)
        image = response.json()
        embed = discord.Embed(title='From nekos.life')
        embed.set_image(url=image['url'])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, BucketType.user)
    @commands.guild_only()
    @commands.is_nsfw()
    async def danbooru(self, ctx, tags=None, secondtag=None):
        """Posts an image directly from Project Danbooru."""
        rating = 0
        temp = '[-status]=deleted'
        # No tags
        if tags is None:
            pass
        # Tags
        else:
            if secondtag is None:
                rating = self.checktags(tags, '')
                if not self.nololitag(tags, ''):
                    await ctx.send('We can\'t show this as it violates Discord ToS.')
                    return
            else:
                rating = self.checktags(tags, secondtag)
                if not self.nololitag(tags, secondtag):
                    await ctx.send('We can\'t show this as it violates Discord ToS.')
                    return
            # One tag
            if secondtag is None:
                if rating == 0:
                    temp = temp + f'&[tags]={tags}'
                else:
                    temp = temp + f'&[tags]={self.rating(rating)}'
            # Two tags
            else:
                if rating == 0:
                    temp = temp + f'&[tags]={tags}+{secondtag}'
                else:
                    if ('safe'.lower() or 'questionable'.lower() or 'explicit'.lower()) in tags:
                        temp = temp + f'&[tags]={self.rating(rating)}+{secondtag}'
                    else:
                        temp = temp + f'&[tags]={tags}+{self.rating(rating)}'
        async with aiohttp.ClientSession() as session:
            async with session.get('https://danbooru.donmai.us/posts/random.json?search{temp}') as resp:
                data = await resp.json()
            await session.close()
        try:
            url = data['file_url']
        except Exception:
            await ctx.send('We could not find any images with that tag.')
            return
        embed = discord.Embed(color=ctx.message.guild.me.color, title='Image from Project Danbooru!',
                              description='If you can\'t see the image, click the title.', url=url)
        embed.add_field(name='Rating: ', value=f'{self.formatrating(data["rating"])}', inline=True)
        embed.add_field(name=f'Known tags ({data["tag_count"]}): ', value=f'`{data["tag_string"]}`',
                        inline=False)
        embed.add_field(name='Original link: ', value=f'[Click here](https://danbooru.donmai.us/posts/{data["id"]})',
                        inline=True)
        embed.set_image(url=url)
        embed.set_footer(text='Powered by Project Danbooru.')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, BucketType.user)
    @commands.guild_only()
    @commands.is_nsfw()
    async def konachan(self, ctx, tags=None, rating=None):
        """Picks a random image from Konachan and displays it."""
        if tags is None:
            temp = '?tags=-status%3Adeleted+-loli+-shota&limit=100'
        elif 'safe'.lower() in tags:
            temp = '?tags=-status%3Adeleted+-loli+-shota+rating:s&limit=100'
        elif 'explicit'.lower() in tags:
            temp = '?tags=-status%3Adeleted+-loli+-shota+rating:e&limit=100'
        elif 'questionable'.lower() in tags:
            temp = '?tags=-status%3Adeleted+-loli+-shota+rating:q&limit=100'
        elif ('loli'.lower() or 'shota'.lower()) in tags:
            await ctx.send('We can\'t show this as it violates Discord ToS.')
            return
        else:
            if rating is None:
                temp = f'?tags=-status%3Adeleted+-loli+-shota+{tags}&limit=100'
            elif 'safe'.lower() in rating:
                temp = f'?tags=-status%3Adeleted+-loli+-shota+{tags}+rating:s&limit=100'
            elif 'explicit'.lower() in rating:
                temp = f'?tags=-status%3Adeleted+-loli+-shota+{tags}+rating:e&limit=100'
            elif 'questionable'.lower() in rating:
                temp = f'?tags=-status%3Adeleted+-loli+-shota+{tags}+rating:q&limit=100'
            else: # It's a tag and not a rating.
                temp = f'?tags=-status%3Adeleted+-loli+-shota+{tags}+{rating}&limit=100'
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://konachan.com/post/index.json{temp}' as resp:
                data = await resp.json()
            await session.close()
        try:
            selected = random.randint(0, len(data))
            url = data[selected]['file_url']
        except Exception:
            await ctx.send('We could not find any images with that tag.')
            return
        embed = discord.Embed(color=ctx.message.guild.me.color, title='Image from Konachan!',
                              description='If you can\'t see the image, click the title.', url=url)
        embed.add_field(name='Known tags: ', value=f'`{data[selected]["tags"]}`',
                        inline=False)
        embed.add_field(name='Original link: ',
                        value=f'[Click here](https://konachan.com/post/{data[selected]["id"]})',
                        inline=True)
        embed.set_image(url=url)
        embed.set_footer(text='Powered by Konachan.')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, BucketType.user)
    @commands.guild_only()
    @commands.is_nsfw()
    async def yandere(self, ctx, tags=None, rating=None):
        """Picks a random image from Yande.re and displays it."""
        if tags is None:
            temp = '?tags=-status%3Adeleted+-loli+-shota&limit=100'
        elif 'safe'.lower() in tags:
            temp = '?tags=-status%3Adeleted+-loli+-shota+rating:s&limit=100'
        elif 'explicit'.lower() in tags:
            temp = '?tags=-status%3Adeleted+-loli+-shota+rating:e&limit=100'
        elif 'questionable'.lower() in tags:
            temp = '?tags=-status%3Adeleted+-loli+-shota+rating:q&limit=100'
        elif ('loli'.lower() or 'shota'.lower()) in tags:
            await ctx.send('We can\'t show this as it violates Discord ToS.')
            return
        else:
            if rating is None:
                temp = f'?tags=-status%3Adeleted+-loli+-shota+{tags}&limit=100'
            elif 'safe'.lower() in rating:
                temp = f'?tags=-status%3Adeleted+-loli+-shota+{tags}+rating:s&limit=100'
            elif 'explicit'.lower() in rating:
                temp = f'?tags=-status%3Adeleted+-loli+-shota+{tags}+rating:e&limit=100'
            elif 'questionable'.lower() in rating:
                temp = f'?tags=-status%3Adeleted+-loli+-shota+{tags}+rating:q&limit=100'
            else: # It's a tag, not a rating.
                temp = f'?tags=-status%3Adeleted+-loli+-shota+{tags}+{rating}&limit=100'
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://yande.re/post/index.json{temp}') as resp:
                data = await resp.json()
            await session.close()
        try:
            selected = random.randint(0, len(data))
            url = data[selected]['file_url']
        except Exception:
            await ctx.send('We could not find any images with that tag.')
            return
        embed = discord.Embed(color=ctx.message.guild.me.color, title='Image from Yande.re!',
                              description='If you can\'t see the image, click the title.', url=url)
        embed.add_field(name='Known tags: ', value=f'`{data[selected]["tags"]}`',
                        inline=False)
        embed.add_field(name='Original link: ',
                        value=f'[Click here](https://yande.re/post/show/{data[selected]["id"]})',
                        inline=True)
        embed.set_image(url=url)
        embed.set_footer(text='Powered by Yande.re.')
        await ctx.send(embed=embed)

    @commands.command(aliases=['r34'])
    @commands.cooldown(1, 3, BucketType.user)
    @commands.guild_only()
    @commands.is_nsfw()
    async def rule34(self, ctx, *, tags=None):
        await ctx.send('This command has not yet been implemented.')

    @commands.command()
    @commands.cooldown(1, 3, BucketType.user)
    @commands.guild_only()
    @commands.is_nsfw()
    async def gelbooru(self, ctx, *, tags=None):
        await ctx.send('This command has not yet been implemented.')

    @staticmethod
    def rating(integer):
        if integer == 1:
            return 'rating:s'
        elif integer == 2:
            return 'rating:q'
        elif integer == 3:
            return 'rating:e'

    @staticmethod
    def checktags(tagone, tagtwo):
        if 'safe'.lower() in tagone or 'safe'.lower() in tagtwo:
            return 1
        elif 'questionable'.lower() in tagone or 'questionable'.lower() in tagtwo:
            return 2
        elif 'explicit'.lower() in tagone or 'explicit'.lower() in tagtwo:
            return 3
        return 0

    @staticmethod
    def nololitag(tagone, tagtwo):
        if 'loli'.lower() in tagone or 'loli'.lower() in tagtwo:
            return False
        if 'shota'.lower() in tagone or 'shota'.lower() in tagtwo:
            return False
        return True

    @staticmethod
    def formatrating(tag):
        if 's' in tag:
            return 'safe'
        elif 'e' in tag:
            return 'explicit'
        elif 'q' in tag:
            return 'questionable'

    @staticmethod
    def taglistlength(taglist):
        if len(taglist) >= 1024:
            return taglist[:1021] + '...'
        else:
            return taglist


def setup(bot):
    bot.add_cog(Image(bot))
