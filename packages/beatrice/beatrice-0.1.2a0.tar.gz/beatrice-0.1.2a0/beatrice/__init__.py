__title__ = 'Beatrice'
__author__ = 'Andre Augusto'
__license__ = 'MIT'
__copyright__ = 'Copyright 2018 Andre Augusto'
__version__ = '0.1.2a'

import discord
from .main import dfile
discord.abc.Messageable.open = dfile
