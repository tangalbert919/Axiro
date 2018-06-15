import discord
from discord.ext import commands
import asyncio
import json

class WeirdnessBot(commands.Bot):

    def __init__(self):
        self._prefix = '$'
        super().__init__(command_prefix=self._prefix)

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        await self.change_presence(activity=discord.Activity(name='The Testing Grounds', type=discord.ActivityType.playing))
        

    async def on_message(self, message):
        if message.author == self.user:
            return
        await self.process_commands(message)

    @commands.command(name='help')
    async def _help(self, beep):
        embed = discord.Embed(title="Hi! I am a bot being built!", description="I am currently being built by my creator, so feel free to ignore me right now. :(")
        await beep.send(embed=embed)
    
    @commands.command(name='test')
    async def test(self, beep):
        await beep.send('Testing, testing...')
    
client = WeirdnessBot()
config = json.loads(open('config.json', 'r').read())
client.run(config.get('discordtoken'))