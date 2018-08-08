# INSTALL.md

If you are reading this document, it means you absolutely want to run an instance of this bot yourself. Do note that
this is not for the faint of heart, and as such, you must know what you're doing.

# How to install

To start, you need to have Python 3.6 installed. Linux distros (such as Ubuntu, Arch Linux, Linux Mint, Zorin) already
have this (it may require an update), but if you have macOS, you need to install it [here](https://www.python.org/downloads/).

I strongly discourage the use of Windows, as some parts of the bot require libraries that do not work on Windows.

Using Python 3.6, you need to install the following:

* yarl<1.2
* pybooru
* newsapi
* aiohttp
* lavalink

To install them, run `python -m pip install -U --user <package>`.

The Discord rewrite is a bit more complicated. For the sake of not giving you headaches, run this command:

`python3 -m pip install -U https://github.com/Rapptz/discord.py/archive/rewrite.zip#egg=discord.py[voice]`

You need libffi-dev installed on your machine for this.

# API Tokens

You absolutely must acquire these keys yourself. I am not getting them for you.

* Discord API Token
* News API Token
* Danbooru Username & API Token
* Konachan Username & Password

# How to get this bot running

1. Place all API Tokens in where they should go in config.json. That file needs to be created.
2. Install the requirements listed above.
3. Download the Lavalink.jar file (use the dev builds if you want working audio), and run it.
3. `python3 core.py`

# The config.json

```json
{
    "discordtoken": "discordapp.com API token",
    "newsapitoken": "newsapi token",
    "danbooruname": "Danbooru username",
    "danboorutoken": "Danbooru API token",
    "konachanname": "Konachan username",
    "konachanpasswd": "Konachan password",
    "lavalinkpass": "Lavalink password"
}
```