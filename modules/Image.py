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
    async def danbooru(self, context, tags=None, rating=None):
        """Posts an image directly from Project Danbooru."""
        if context.message.channel.is_nsfw():
            if tags is None:
                temp = "[-status]=deleted"
            elif "safe".lower() in tags:
                temp = "[-status]=deleted&[tags]=rating:s"
            elif "explicit".lower() in tags:
                temp = "[-status]=deleted&[tags]=rating:e"
            elif "questionable".lower() in tags:
                temp = "[-status]=deleted&[tags]=rating:q"
            elif "loli".lower() in tags:
                await context.send("We can't show this as it violates Discord ToS.")
                return
            elif "shota".lower() in tags:
                await context.send("We can't show this as it violates Discord ToS.")
                return
            else:
                if rating is None:
                    temp = "[-status]=deleted&[tags]={}".format(tags)
                elif "safe".lower() in rating:
                    temp = "[-status]=deleted&[tags]={}+rating:s".format(tags)
                elif "explicit".lower() in rating:
                    temp = "[-status]=deleted&[tags]={}+rating:e".format(tags)
                elif "questionable".lower() in rating:
                    temp = "[-status]=deleted&[tags]={}+rating:q".format(tags)
                else:
                    await context.send("Please specify a valid rating. "
                                       "Valid ratings include questionable, explicit, and safe.")
                    return
            async with aiohttp.ClientSession() as session:
                async with session.get('https://danbooru.donmai.us/posts/random.json?search{}'
                                                   .format(temp)) as resp:
                    data = await resp.json()
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


def setup(bot):
    bot.add_cog(Image(bot))
