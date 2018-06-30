import discord
from discord.ext import commands
import json
from newsapi import NewsApiClient
from datetime import datetime


class Miscellaneous:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def news(self, msg):
        config = json.loads(open('config.json', 'r').read())
        newsapi = NewsApiClient(api_key=config.get('newsapitoken'))
        top_headlines = newsapi.get_top_headlines(language='en', country='us', page_size=1)
        top_headlines = self.repairJSON(str(top_headlines))
        top_headlines = json.loads(top_headlines)
        print(top_headlines)
        embed = discord.Embed(color=discord.Colour.dark_red(), title="Latest from the news.",
                              description="[{}]({})".format(top_headlines['articles'][0]['title'],
                                                            top_headlines['articles'][0]['url']))
        embed.set_image(url=top_headlines['articles'][0]['urlToImage'])
        await msg.send(embed=embed)

    @commands.command()
    async def math(self, ctx, *, message: str):
        try:
            answer = eval(message)
            await ctx.send("Answer: ", answer)
        except Exception:
            await ctx.send("This is not an equation.")

    @commands.command()
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f"{days}d, {hours}h, {minutes}m, {seconds}s")


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