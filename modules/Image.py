import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import random
import requests
import aiohttp


class Image:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    async def neko(self, ctx):
        if ctx.message.channel.is_nsfw():
            url = 'https://nekos.life/api/v2/img/lewd'
        else:
            url = 'https://nekos.life/api/v2/img/neko'
        response = requests.get(url)
        image = response.json()
        embed = discord.Embed(title="From nekos.life")
        embed.set_image(url=image['url'])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, BucketType.user)
    async def danbooru(self, context, tags=None, secondtag=None):
        """Posts an image directly from Project Danbooru."""
        if context.message.channel.is_nsfw():
            safe_rating = False
            questionable_rating = False
            explicit_rating = False
            temp = "[-status]=deleted"
            # No tags
            if tags is None:
                pass
            else:
                # Do rating checks
                if "safe".lower() in tags or "safe".lower() in secondtag:
                    safe_rating = True
                elif "explicit".lower() in tags or "explicit".lower() in secondtag:
                    explicit_rating = True
                elif "questionable".lower() in tags or "questionable".lower() in secondtag:
                    questionable_rating = True
                # Check for tags we can't use
                if "loli".lower() in tags or "loli".lower() in secondtag:
                    if "shota".lower() in tags or "shota".lower() in secondtag:
                        await context.send("We can't show this as it violates Discord ToS.")
                        return
                    await context.send("We can't show this as it violates Discord ToS.")
                    return
                # One tag
                if secondtag is None:
                    if not safe_rating and not questionable_rating and not explicit_rating:
                        temp = temp + "&[tags]={}".format(tags)
                    else:
                        temp = temp + "&[tags]={}".format(self.rating(safe_rating, questionable_rating, explicit_rating))
                # Two tags
                else:
                    if not safe_rating and not questionable_rating and not explicit_rating:
                        temp = temp + "&[tags]={}+{}".format(tags, secondtag)
                    else:
                        if "safe".lower() in tags or "questionable".lower() in tags or "explicit".lower() in tags:
                            temp = temp + "&[tags]={}+{}".format(self.rating(safe_rating, questionable_rating, explicit_rating), secondtag)
                        else:
                            temp = temp + "&[tags]={}+{}".format(tags, self.rating(safe_rating, questionable_rating, explicit_rating))
            async with aiohttp.ClientSession() as session:
                async with session.get('https://danbooru.donmai.us/posts/random.json?search{}'
                                                   .format(temp)) as resp:
                    data = await resp.json()
                session.close()
            try:
                url = data['file_url']
            except Exception:
                await context.send("We could not find any images with that tag.")
                return
        else:
            await context.send("You need to be in a NSFW channel to run this command.")
            return
        if context.message.guild is not None:
            color = context.message.guild.me.color
        else:
            color = discord.Colour.blurple()
        embed = discord.Embed(color=color, title="Image from Project Danbooru!",
                              description="If you can't see the image, click the title.", url=url)
        embed.add_field(name="Known tags ({}): ".format(data['tag_count']), value="`{}`".format(data['tag_string']),
                        inline=False)
        embed.add_field(name="Original link: ", value="[Click here](https://danbooru.donmai.us/posts/{})".format(data['id']),
                        inline=True)
        embed.set_image(url=url)
        embed.set_footer(text="Powered by Project Danbooru.")
        await context.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, BucketType.user)
    async def konachan(self, context, tags=None, rating=None):
        """Picks a random image from Konachan and displays it."""
        url_list = []
        if context.message.channel.is_nsfw():
            if tags is None:
                temp = "?tags=-status%3Adeleted+-loli+-shota&limit=100"
            elif "safe".lower() in tags:
                temp = "?tags=-status%3Adeleted+-loli+-shota+rating:s&limit=100"
            elif "explicit".lower() in tags:
                temp = "?tags=-status%3Adeleted+-loli+-shota+rating:e&limit=100"
            elif "questionable".lower() in tags:
                temp = "?tags=-status%3Adeleted+-loli+-shota+rating:q&limit=100"
            elif "loli".lower() in tags:
                await context.send("We can't show this as it violates Discord ToS.")
                return
            elif "shota".lower() in tags:
                await context.send("We can't show this as it violates Discord ToS.")
                return
            else:
                if rating is None:
                    temp = "?tags=-status%3Adeleted+-loli+-shota+{}&limit=100".format(tags)
                elif "safe".lower() in rating:
                    temp = "?tags=-status%3Adeleted+-loli+-shota+{}+rating:s&limit=100".format(tags)
                elif "explicit".lower() in rating:
                    temp = "?tags=-status%3Adeleted+-loli+-shota+{}+rating:e&limit=100".format(tags)
                elif "questionable".lower() in rating:
                    temp = "?tags=-status%3Adeleted+-loli+-shota+{}+rating:q&limit=100".format(tags)
                else:
                    await context.send("Please specify a valid rating. "
                                       "Valid ratings include questionable, explicit, and safe.")
                    return
            async with aiohttp.ClientSession() as session:
                async with session.get('https://konachan.com/post/index.json{}'
                                               .format(temp)) as resp:
                    data = await resp.json()
                    for entry in data:
                        #print(entry['file_url'])
                        url_list.append(entry['file_url'])
                session.close()
            try:
                url = url_list[random.randint(0, len(url_list))]
            except Exception:
                await context.send("We could not find any images with that tag.")
                return
        else:
            await context.send("You need to be in a NSFW channel to run this command.")
            return
        if context.message.guild is not None:
            color = context.message.guild.me.color
        else:
            color = discord.Colour.blurple()
        embed = discord.Embed(color=color, title="Image from Konachan!",
                              description="If you can't see the image, click the title.", url=url)
        embed.set_image(url=url)
        embed.set_footer(text="Powered by Konachan.")
        await context.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, BucketType.user)
    async def yandere(self, context, tags=None, rating=None):
        url_list = []
        if context.message.channel.is_nsfw():
            if tags is None:
                temp = "?tags=-status%3Adeleted+-loli+-shota&limit=100"
            elif "safe".lower() in tags:
                temp = "?tags=-status%3Adeleted+-loli+-shota+rating:s&limit=100"
            elif "explicit".lower() in tags:
                temp = "?tags=-status%3Adeleted+-loli+-shota+rating:e&limit=100"
            elif "questionable".lower() in tags:
                temp = "?tags=-status%3Adeleted+-loli+-shota+rating:q&limit=100"
            elif "loli".lower() in tags:
                await context.send("We can't show this as it violates Discord ToS.")
                return
            elif "shota".lower() in tags:
                await context.send("We can't show this as it violates Discord ToS.")
                return
            else:
                if rating is None:
                    temp = "?tags=-status%3Adeleted+-loli+-shota+{}&limit=100".format(tags)
                elif "safe".lower() in rating:
                    temp = "?tags=-status%3Adeleted+-loli+-shota+{}+rating:s&limit=100".format(tags)
                elif "explicit".lower() in rating:
                    temp = "?tags=-status%3Adeleted+-loli+-shota+{}+rating:e&limit=100".format(tags)
                elif "questionable".lower() in rating:
                    temp = "?tags=-status%3Adeleted+-loli+-shota+{}+rating:q&limit=100".format(tags)
                else:
                    await context.send("Please specify a valid rating. "
                                       "Valid ratings include questionable, explicit, and safe.")
                    return
            async with aiohttp.ClientSession() as session:
                async with session.get('https://yande.re/post/index.json{}'
                                               .format(temp)) as resp:
                    data = await resp.json()
                    for entry in data:
                        # print(entry['file_url'])
                        url_list.append(entry['file_url'])
                session.close()
            try:
                url = url_list[random.randint(0, len(url_list))]
            except Exception:
                await context.send("We could not find any images with that tag.")
                return
        else:
            await context.send("You need to be in a NSFW channel to run this command.")
            return
        if context.message.guild is not None:
            color = context.message.guild.me.color
        else:
            color = discord.Colour.blurple()
        embed = discord.Embed(color=color, title="Image from Yande.re!",
                              description="If you can't see the image, click the title.", url=url)
        embed.set_image(url=url)
        embed.set_footer(text="Powered by Yande.re.")
        await context.send(embed=embed)

    def repairJSON(self, temp):
        temp = temp.replace("{\'", "{\"")
        temp = temp.replace("\': ", "\": ")
        temp = temp.replace("\": \'", "\": \"")
        temp = temp.replace("\', \'", "\", \"")
        temp = temp.replace(", \'", ", \"")
        temp = temp.replace("\'}", "\"}")
        temp = temp.replace("True", "\"True\"")
        temp = temp.replace("False", "\"False\"")
        temp = temp.replace("None", "\"None\"")
        temp = temp[1:-1]
        return temp

    @staticmethod
    def rating(safe, questionable, explicit):
        if safe:
            return "rating:s"
        elif questionable:
            return "rating:q"
        elif explicit:
            return "rating:e"


def setup(bot):
    bot.add_cog(Image(bot))
