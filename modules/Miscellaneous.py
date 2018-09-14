import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import json
from datetime import datetime
import aiohttp


class Miscellaneous:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    async def news(self, msg):
        config = json.loads(open('config.json', 'r').read())
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://newsapi.org/v2/top-headlines?country=us&pageSize=1&apiKey={}'
                                       .format(config.get('newsapitoken'))) as resp:
                    top_headlines = await resp.json()
        except Exception:
            await msg.send("I was completely unable to read the news. :(")
            return
        embed = discord.Embed(color=discord.Colour.dark_red(), title="Latest from the news.",
                              description="[{}]({})".format(top_headlines['articles'][0]['title'],
                                                            top_headlines['articles'][0]['url']))
        try:
            embed.set_image(url=top_headlines['articles'][0]['urlToImage'])
        except Exception:
            pass
        await msg.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send("I have been up for "f"{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds.")

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    async def translate(self, ctx):
        await ctx.send("Currently unavailable.")

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
        #temp = temp[1:-1]
        return temp

def setup(bot):
    bot.add_cog(Miscellaneous(bot))
