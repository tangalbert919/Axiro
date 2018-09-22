# INSTALL.md

If you are reading this document, it means you absolutely want to run an instance of this bot yourself. Do note that
this is not for the faint of heart, and as such, you must know what you're doing.

# Prerequisites

Before you begin, you need to have Python 3.6 or above installed. Linux distros (such as Ubuntu, Arch Linux, Linux Mint, Zorin) already
have this (it may require an update), but if you have macOS, you need to install it [here](https://www.python.org/downloads/).

I strongly discourage the use of Windows, as some parts of the bot require libraries that do not work on Windows.

Pip is required for this, and by default, it's already installed into Python for you. If not, go [here](https://pip.pypa.io/en/stable/installing/) 
to install it.

Now, with all of that being said, you will need to use Pip to install the following packages:

* yarl<1.2
* pybooru
* aiohttp
* lavalink
* asyncpg

To install them, run `python3 -m pip install -U --user <package>`.

If you are on Linux, you need to install libffi-dev (or libffi-devel for some distros) for installing the Discord rewrite,
as one of the dependencies (PyNaCl) needs that library for voice support to work. You have to use your distro's package
management tool for that.

Once you have that library installed, you can run this command:

`python3 -m pip install -U https://github.com/Rapptz/discord.py/archive/rewrite.zip#egg=discord.py[voice]`

# API Tokens

You absolutely **must** acquire these keys yourself. I am not getting them for you.

* Discord API Token (you can get them from the Developer's Portal on discordapp.com)
* News API Token
* Konachan Username & Password

# Unobtainable API tokens

* DiscordBots.org API token

# Initializing database

You need to install PostgreSQL if you want full functionality of the bot. You must create the database called "axiro"
yourself. The bot will handle the rest for you.

# How to get this bot running

1. Place all API Tokens in where they should go in config.json. That file needs to be created.
2. Install the requirements listed above.
3. Download the Lavalink.jar file (use the dev builds if you want working audio), and run it.
4. `python3 core.py`

# The config.json

```json
{
    "discordtoken": "discordapp.com API token",
    "newsapitoken": "newsapi token",
    "konachanname": "Konachan username",
    "konachanpasswd": "Konachan password",
    "lavalinkpass": "Lavalink password",
    "dbpass": "Database password",
    "dbuser": "Database username",
    "dbl_token": "DiscordBots.org token",
    "prefix": "x!"
}
```