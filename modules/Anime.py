import discord
from discord.ext import commands
from pybooru import Danbooru
from pybooru import Moebooru
import json
import random
import requests

class Anime:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def neko(self, ctx):
        if ctx.message.channel.is_nsfw():
            url = 'https://nekos.life/api/v2/img/nsfw_neko_gif'
        else:
            url = 'https://nekos.life/api/v2/img/neko'
        response = requests.get(url)
        print(response.json())
        image = response.json()
        await ctx.send(image['url'])

    @commands.command()
    async def danbooru(self, context):
        """Posts an image directly from Project Danbooru."""
        client = Danbooru('danbooru', username=self.bot.config['danbooruname'], api_key=self.bot.config['danboorutoken'])
        if context.message.channel.is_nsfw():
            image_found = False
            while not image_found:
                temp = self.repairJSON(
                    str(client.post_list(random=True, limit=1, tags="rating:e -status:deleted")))
                data = json.loads(temp)
                if 'file_url' in data:
                    image_found = True
            url = data['file_url']
        else:
            await context.send("You need to be in a NSFW channel for this.")
            return
        if context.message.guild is not None:
            color = context.message.guild.me.color
        else:
            color = discord.Colour.blurple()
        embed = discord.Embed(color=color, title="Image from Project Danbooru!",
                              description="Here's your image, {}~".format(context.message.author.name))
        embed.set_image(url=url)
        embed.set_footer(text="Powered by Project Danbooru.")
        await context.send(embed=embed)

    @commands.command()
    async def safebooru(self, context):
        """Same as danbooru, but looks for safe images."""
        client = Danbooru('danbooru', username=self.bot.config['danbooruname'], api_key=self.bot.config['danboorutoken'])
        image_found = False
        while not image_found:
            temp = self.repairJSON(str(client.post_list(random=True, limit=1, tags="rating:s -status:deleted")))
            data = json.loads(temp)
            if 'file_url' in data:
                image_found = True
        url = data['file_url']
        if context.message.guild is not None:
            color = context.message.guild.me.color
        else:
            color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="Image from Project Danbooru!",
                              description="Here's your image, {}~".format(context.message.author.name))
        embed.set_image(url=url)
        embed.set_footer(text="Powered by Project Danbooru.")
        await context.send(embed=embed)

    @commands.command()
    async def konachan(self, context):
        """Picks a random image from Konachan and displays it."""
        client = Moebooru('konachan', username=self.bot.config['konachanname'],
                          password=self.bot.config['konachanpasswd'])
        image_found = False
        if context.message.channel.is_nsfw():
            latest_post = self.repairJSON(str(client.post_list(limit=1)))
            post_loaded = json.loads(latest_post)
            highest_id = post_loaded['id']
            while not image_found:
                id_number = random.randint(1, highest_id)
                temp = self.repairJSON(
                    str(client.post_list(limit=1, tags="-status:deleted id:{}".format(id_number))))
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
            color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="Image from Konachan!",
                              description="Here's your image, {}~".format(context.message.author.name))
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
    bot.add_cog(Anime(bot))