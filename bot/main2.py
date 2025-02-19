import discord
from discord.ext import commands
import requests
import os 

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = "http://127.0.0.1:8000"

intents = discord.Intents.default()  # Intenciones de acceder a diferentes eventos de la API de Discord
intents.message_content = True  # Intención de acceder a los mensajes
bot = commands.Bot(command_prefix='>', intents=intents)  # Crear el bot con el prefijo de comando ">" y las intenciones

@bot.event
async def on_ready():
    print(f"{bot.user} está en linea")  # Imprimir en consola el nombre del bot

@bot.command()
async def personaje(ctx,* , nombre: str):
    try:
        # Obtiene infromacion de un personaje desde la API
        resultado = requests.get(f"{API_URL}{nombre.lower()}")

        # Verificar si la respuesta es exitosa
        if resultado.status_code == 200:
            personaje = resultado.json()
            print(image_url)
            await ctx.send(image_url)
        else:
            await ctx.send(f"El Pokémon `{pokemon}` no fue encontrado. Por favor, verifica el nombre.")

    except Exception as e:
        print(f"Error: {e}")
        await ctx.send("Ocurrió un error inesperado. Por favor, intenta de nuevo.")


@poke.error
async def error_type(ctx, error):
    if isinstance(error, commands.errors.MissingRequirednombreument):
        await ctx.send("Falta el nombre del Pokémon. Usa el comando así: `>poke nombre_del_pokemon`")




@bot.command()
async def limpiar(ctx):
    await ctx.channel.purge(limit=100)
    await ctx.send("Mensajes eliminados", delete_after=3)

webserver.keep_alive()  # Iniciar el servidor web
bot.run(DISCORD_TOKEN)  # Iniciar el bot con el token de la aplicación