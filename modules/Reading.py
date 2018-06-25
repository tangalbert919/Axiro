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
        top_headlines = top_headlines['articles'][0]['url']
        print(top_headlines)
        await msg.send(top_headlines)

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