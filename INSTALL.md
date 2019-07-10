# INSTALL.md

If you are reading this document, it means you absolutely want to run an instance of this bot yourself. Do note that
this is not for the faint of heart, and as such, you must know what you're doing.

## Prerequisites

Before you begin, you must have Python 3.6 or above installed. Linux distros (such as Ubuntu, Arch Linux, Linux Mint, Zorin) already
have this (it may require an update), but if you have macOS, you need to install it [here](https://www.python.org/downloads/).

Pip is required for this, and by default, it's already installed into Python for you. If not, go [here](https://pip.pypa.io/en/stable/installing/) 
to install it.

Now, with all of that being said, you need to install the `discord` package. Then you need to install these packages:

* lavalink
* asyncpg
* requests
* lxml

To install them, run `python3 -m pip install -U --user <package>`.

If you are on Linux, you need to install libffi-dev (or libffi-devel for some distros) for installing the Discord rewrite,
as one of the dependencies (PyNaCl) needs that library for voice support to work. You have to use your distro's package
management tool for that.

## API Tokens

You absolutely **must** acquire these keys yourself. I am not getting them for you.

* Discord API Token (you can get them from the Developer's Portal on discordapp.com)
* News API Token

## Unobtainable API tokens

* DiscordBots.org API token

## Initializing database

This is entirely optional, but if you plan on having the bot use a database, you need to download PostgreSQL and
create a database called "axiro". The bot will setup the database for you.

## How to get this bot running

1. Place all API Tokens in where they should go in config.json. That file needs to be created.
2. Install the requirements listed above.
3. Download the Lavalink.jar file (use the dev builds if you want working audio), and run it.
4. Depending on your platform, run either `python3 core.py` or `py core.py`.

## The config.json

```json
{
    "discordtoken": "discordapp.com API token",
    "newsapitoken": "newsapi token",
    "lavalinkpass": "Lavalink password",
    "dbpass": "Database password",
    "dbuser": "Database username",
    "dbl_token": "DiscordBots.org token",
    "prefix": "x!",
	"lavaport": "1337",
}
```