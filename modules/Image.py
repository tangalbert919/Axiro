import discord
from discord.ext import commands
from pybooru import Danbooru
from pybooru import Moebooru
import json
import random
import requests


class Image:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
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
    async def danbooru(self, context, tags=None, rating=None):
        """Posts an image directly from Project Danbooru."""
        client = Danbooru('danbooru', username=self.bot.config['danbooruname'],
                          api_key=self.bot.config['danboorutoken'])
        if context.message.channel.is_nsfw():
            image_found = False
            while not image_found:
                if tags is None:
                    temp = self.repairJSON(
                        str(client.post_list(random=True, limit=1, tags="-status:deleted")))
                else:
                    if rating is None:
                        temp = self.repairJSON(
                            str(client.post_list(random=True, limit=1,
                                                 tags="-status:deleted {}".format(tags))))
                    elif "safe".lower() in rating:
                        temp = self.repairJSON(
                            str(client.post_list(random=True, limit=1,
                                                 tags="rating:s -status:deleted {}".format(tags))))
                    elif "explicit".lower() in rating:
                        temp = self.repairJSON(
                        str(client.post_list(random=True, limit=1, tags="rating:e -status:deleted {}".format(tags))))
                data = json.loads(temp)
                if 'file_url' in data:
                    image_found = True
            url = data['file_url']
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
    async def konachan(self, context, tags=None, rating=None):
        """Picks a random image from Konachan and displays it."""
        client = Moebooru('konachan', username=self.bot.config['konachanname'],
                          password=self.bot.config['konachanpasswd'])
        image_found = False
        if context.message.channel.is_nsfw():
            latest_post = self.repairJSON(str(client.post_list(limit=1)))
            post_loaded = json.loads(latest_post)
            highest_id = post_loaded['id']
            while not image_found:
                if tags is None:
                    id_number = random.randint(1, highest_id)
                    temp = self.repairJSON(
                        str(client.post_list(limit=1, tags="-status:deleted id:{}".format(id_number))))
                else:
                    if "safe".lower() in rating:
                        temp = self.repairJSON(
                            str(client.post_list(limit=1, tags="-status:deleted rating:s {}".format(tags))))
                    elif "explicit".lower() in rating:
                        temp = self.repairJSON(
                            str(client.post_list(limit=1, tags="-status:deleted rating:e {}".format(tags))))
                    else:
                        temp = self.repairJSON(
                            str(client.post_list(limit=1, tags="-status:deleted {}".format(tags))))
                data = json.loads(temp)
                if 'file_url' in data:
                    image_found = True
        else:
            await context.send("You need to be in a NSFW channel for this.")
            return
        url = data['file_url']
        if context.message.guild is not None:
            color = context.message.guild.me.color
        else:
            color = discord.Colour.blurple()
        embed = discord.Embed(color=color, title="Image from Konachan!",
                              description="If you can't see the image, click the title.", url=url)
        embed.set_image(url=url)
        embed.set_footer(text="Powered by Konachan.")
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
