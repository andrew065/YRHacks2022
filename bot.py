from config import token
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

bot.load_extension("somecommands")

bot.run(token)
