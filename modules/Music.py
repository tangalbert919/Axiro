import discord


class Music:

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Music(bot))