from discord.ext import commands
from datetime import datetime

dt = datetime()

epoch_time = dt.timestamp()

class Time_Function(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    