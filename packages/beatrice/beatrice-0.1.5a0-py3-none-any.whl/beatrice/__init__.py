__title__ = 'Beatrice'
__author__ = 'Andre Augusto'
__license__ = 'MIT'
__copyright__ = 'Copyright 2018 Andre Augusto'
__version__ = '0.1.5a'

import discord
from .main import dfile
discord.TextChannel.open = dfile
