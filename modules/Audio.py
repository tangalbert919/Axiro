#very work in progress, doesn't actually do anything yet
import discord
from discord.ext import commands
import threading
import os
import youtube_dl
import re
import logging
import collections
import copy
import asyncio
import math
import time
import inspect
import subprocess
import urllib.parse
import datetime
youtube_dl_options = {
    'source_address': '0.0.0.0',
    'format': 'best',
    'extractaudio': True,
    'audioformat': "mp3",
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'quiet': False,
    'no_warnings': True,
    'outtmpl': "data/audio/cache/%(id)s",
    'default_search': 'auto',
    'encoding': 'utf-8'
}
