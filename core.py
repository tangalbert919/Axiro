import discord
from discord.ext import commands
import json
import os
import asyncio


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
        self.loop.create_task(self.status_task())

    async def on_message(self, message):
        if message.author == self.user:
            return
        await self.process_commands(message)

    async def on_command_error(self, context, exception):
        if isinstance(exception, discord.ext.commands.errors.MissingRequiredArgument):
            await context.send("You're missing one or more required arguments.")

    async def status_task(self):
        await self.change_presence(activity=discord.Activity(name='Do \"$help\" for help', type=discord.ActivityType.playing))
        await asyncio.sleep(30)
        await self.change_presence(activity=discord.Activity(name='PyCharm Community', type=discord.ActivityType.playing))
        await asyncio.sleep(30)
        await self.change_presence(activity=discord.Activity(name='24K Magic', type=discord.ActivityType.listening))
        await asyncio.sleep(30)
        await self.change_presence(activity=discord.Activity(name='A whole lot of anime stuff', type=discord.ActivityType.streaming))
        await asyncio.sleep(30)


client = WeirdnessBot()
config = json.loads(open('config.json', 'r').read())
client.run(config.get('discordtoken'))