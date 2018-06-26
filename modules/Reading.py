import discord
from discord.ext import commands
import json
from newsapi import NewsApiClient


class Reading:

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
    bot.add_cog(Reading(bot))