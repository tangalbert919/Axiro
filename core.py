import discord
from discord.ext import commands
import json
import os

class WeirdnessBot(commands.Bot):

    def __init__(self):
        self._prefix = '$'
        super().__init__(command_prefix=self._prefix)
        self.remove_command('help')

        self.config = json.loads(open('config.json', 'r').read())

        for file in os.listdir("modules"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.load_extension(f"modules.{name}")
                except:
                    print(f"The {name} module failed to load. Please repair it and load it.")


    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        await self.change_presence(activity=discord.Activity(name='The Testing Grounds', type=discord.ActivityType.playing))
        

    async def on_message(self, message):
        if message.author == self.user:
            return
        await self.process_commands(message)

    async def on_command_error(self, context, exception):
        if isinstance(exception, discord.ext.commands.errors.MissingRequiredArgument):
            await context.send("You're missing one or more required arguments.")


client = WeirdnessBot()
config = json.loads(open('config.json', 'r').read())
client.run(config.get('discordtoken'))