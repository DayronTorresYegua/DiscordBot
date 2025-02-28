import discord
from discord.ext import commands
import config

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=">", intents=intents)
bot.api_url = config.API_URL

bot.load_extension("bot.comandos")

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

bot.run(config.TOKEN)
