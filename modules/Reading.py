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
        top_headlines = newsapi.get_top_headlines(language='en', country='us')
        print(top_headlines)
        await msg.send(top_headlines)
        """url = ('https://newsapi.org/v2/top-headlines?'
               'country=us&'
               'apiKey={}'.format(config.get('newsapitoken')))
        response = requests.get(url)
        print(response.json())
        newsurl = response.json()
        await msg.send(newsurl['url'])"""


def setup(bot):
    bot.add_cog(Reading(bot))