import discord
from discord.ext import commands
import json
import os
import asyncio
import asyncpg
import lavalink
from datetime import datetime
import random
import dbl
import logging


class WeirdnessBot(commands.AutoShardedBot):

    def __init__(self):
        self.config = json.loads(open('config.json', 'r').read())
        self._prefix = self.config['prefix']
        super().__init__(command_prefix=self._prefix)
        self.remove_command('help')

        self.music_client = lavalink.Client(bot=self, password=self.config['lavalinkpass'], loop=self.loop, ws_port=1337)
        self.launch_time = datetime.utcnow()
        self.loop.create_task(self.status_task())

        self.version_code = "Release 4 Beta"

        dbpass = self.config['dbpass']
        dbuser = self.config['dbuser']
        govinfo = {"user": dbuser, "password": dbpass, "database": "axiro", "host": "localhost"}

        async def _init_db():
            self.db = await asyncpg.create_pool(**govinfo)
            await self.db.execute(
                "CREATE TABLE IF NOT EXISTS users (id bigint primary key, name text, discrim varchar (4), money text);")
            await self.db.execute(
                "CREATE TABLE IF NOT EXISTS guilds (id bigint primary key, name text, prefix text);")

        self.loop.create_task(_init_db())

        self.status_msg = json.loads(open('status.json', 'r').read())

        self.dbl_token = self.config['dbl_token']
        self.dblpy = dbl.Client(self, self.dbl_token)
        self.loop.create_task(self.update_stats())

        for file in os.listdir("modules"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.load_extension(f"modules.{name}")
                except Exception:
                    print(f"The {name} module failed to load. Please repair it and load it.")

        logger = logging.getLogger('discord')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(handler)

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""
        while True:
            print('Attempting to post server count')
            try:
                await self.dblpy.post_server_count()
                print('posted server count ({})'.format(len(self.bot.guilds)))
            except Exception as e:
                print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
            await asyncio.sleep(1800)

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.author.bot:
            return
        if not message.author.bot:
            sql = "SELECT * FROM users WHERE id = $1"
            user = await self.db.fetchrow(sql, message.author.id)
            if not user:
                add_user = "INSERT INTO users (id, name, discrim, money) VALUES ($1, $2, $3, 0);"
                await self.db.execute(add_user, message.author.id, message.author.name, message.author.discriminator)
            else:
                update_user = "UPDATE users SET name = $1, discrim = $2 WHERE id = $3"
                await self.db.execute(update_user, message.author.name, message.author.discriminator, message.author.id)
        await self.process_commands(message)

    async def on_command_error(self, context, exception):
        if isinstance(exception, discord.ext.commands.errors.MissingRequiredArgument):
            await context.send("You're missing one or more required arguments.")
        elif isinstance(exception, discord.ext.commands.errors.BotMissingPermissions):
            await context.send("I am missing the required permissions to perform this command successfully.")
        elif isinstance(exception, discord.ext.commands.errors.MissingPermissions):
            await context.send("You do not have permission to perform this command.")
        elif isinstance(exception, discord.ext.commands.errors.CommandNotFound):
            pass
        elif isinstance(exception, discord.ext.commands.errors.BadArgument):
            await context.send("You used an invalid argument.")
        elif isinstance(exception, discord.ext.commands.errors.CommandOnCooldown):
            m, s = divmod(exception.retry_after, 60)
            h, m = divmod(m, 60)
            await context.send("Please slow down! (Rate-limited) :watch:\n"
                               "You can use this command in {} hours, {} minutes, and {} seconds."
                               .format(int(h), int(m), int(s)))
        else:
            await context.send("An error has occurred.")

    async def status_task(self):
        while True:
            selected = random.randint(1, 10)
            message = "x!help | " + self.status_msg.get(str(selected))
            await self.change_presence(activity=discord.Activity(name=message,
                                                                 type=discord.ActivityType.playing))
            await asyncio.sleep(300)

    async def on_guild_join(self, guild):
        sql = "INSERT INTO guilds (id, name, prefix) VALUES ($1, $2, $3)"
        await self.db.execute(sql, guild.id, guild.name, "x!")
        channel = self.get_channel(477206313139699722)
        embed = discord.Embed(title="Guild joined!", color=discord.Colour.blue(),
                              description="We have joined a guild, bringing us to {} guilds!".format(len(self.guilds)))
        embed.add_field(name="Guild name:", value=guild.name)
        embed.add_field(name="Guild Owner: ", value=guild.owner)
        embed.add_field(name="Member count: ", value=guild.member_count)
        embed.set_thumbnail(url=guild.icon_url)
        await channel.send(embed=embed)

    async def on_guild_remove(self, guild):
        sql = "DELETE FROM guilds where id = $1"
        await self.db.execute(sql, guild.id)
        channel = self.get_channel(477206313139699722)
        embed = discord.Embed(title="Guild lost!", color=discord.Colour.red(),
                              description="We have lost a guild, dropping us to {} guilds!".format(len(self.guilds)))
        embed.add_field(name="Guild name:", value=guild.name)
        embed.add_field(name="Guild Owner: ", value=guild.owner)
        embed.add_field(name="Member count: ", value=guild.member_count)
        embed.set_thumbnail(url=guild.icon_url)
        await channel.send(embed=embed)

    async def restart_music(self):
        del self.music_client
        self.music_client = lavalink.Client(bot=self, password=self.config['lavalinkpass'], loop=self.loop,
                                            ws_port=1337)


client = WeirdnessBot()
config = json.loads(open('config.json', 'r').read())
client.run(config.get('discordtoken'))
