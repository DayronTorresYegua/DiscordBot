import os
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener el token desde las variables de entorno
TOKEN = os.getenv('DISCORD_TOKEN')

# Configurar el bot con el prefijo ">"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

# Obtener la ruta absoluta al directorio actual donde se encuentra el script
script_dir = os.path.dirname(os.path.abspath(__file__))
characters_file = os.path.join(script_dir, 'data.json')

# Cargar datos de personajes desde el archivo JSON
try:
    with open(characters_file, 'r', encoding='utf-8') as f:
        print(f"Cargando datos de personajes desde: {characters_file}")
        characters = json.load(f)
        print(f"Personajes cargados: {list(characters.keys())}")
except FileNotFoundError:
    print(f"Error: No se encontró el archivo {characters_file}")
    characters = {}
except json.JSONDecodeError:
    print(f"Error: El archivo {characters_file} no tiene un formato JSON válido")
    characters = {}

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    print(f'ID del bot: {bot.user.id}')
    print('------')

@bot.command(name='personaje')
async def character_info(ctx, *, character_name=None):
    """Muestra información completa sobre un personaje de Wuthering Waves en un solo mensaje"""
    if character_name is None:
        await ctx.send("Por favor, especifica el nombre de un personaje. Ejemplo: `>personaje Rover`")
        return
    
    # Buscar el personaje en el JSON (ignorando mayúsculas/minúsculas)
    character_name = character_name.lower()
    character_found = None
    
    for char_id, char_data in characters.items():
        char_name = char_data.get('name', '').lower()
        if char_name == character_name:
            character_found = char_data
            break
    
    if character_found:
        # Crear embed único con toda la información
        embed = discord.Embed(
            title=f"{character_found['name']} - Guía completa",
            description=character_found.get('description', 'No hay descripción disponible'),
            color=discord.Color.blue()
        )
        
        # Sección 1: Información básica
        basic_info = ""
        if 'rarity' in character_found:
            basic_info += f"**Rareza:** {character_found['rarity']}\n"
        if 'element' in character_found:
            basic_info += f"**Elemento:** {character_found['element']}\n"
        if 'weapon' in character_found:
            basic_info += f"**Arma:** {character_found['weapon']}\n"
        
        embed.add_field(name="Información básica", value=basic_info, inline=False)
        
        # Sección 2: Sets de Echos recomendados
        if 'recommended_builds' in character_found and character_found['recommended_builds']:
            build = character_found['recommended_builds'][0]  # Tomamos la primera build recomendada
            
            # Sets de Echos
            if 'echo_sets' in build:
                sets_info = build['echo_sets']
                sets_text = ""
                
                for set_name, pieces in sets_info.items():
                    sets_text += f"**{set_name}** ({pieces} piezas)\n"
                
                embed.add_field(name="Sets de Echos recomendados", value=sets_text, inline=False)
            
            # Estadísticas principales
            if 'main_stats' in build:
                main_stats = build['main_stats']
                stats_text = ""
                
                for slot, stat in main_stats.items():
                    stats_text += f"**{slot}:** {stat}\n"
                
                embed.add_field(name="Estadísticas principales", value=stats_text, inline=False)
            
            # Subestadísticas
            if 'substats' in build:
                substats = build['substats']
                substats_text = "Prioridad: " + " > ".join(substats)
                
                embed.add_field(name="Subestadísticas recomendadas", value=substats_text, inline=False)
            
        # Establecer la imagen del personaje
        if 'image_url' in character_found:
            embed.set_thumbnail(url=character_found['image_url'])
        
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"No se encontró información sobre el personaje '{character_name}'")
        
        # Sugerir personajes disponibles
        if characters:
            available_chars = [char_data.get('name', char_id) for char_id, char_data in characters.items()]
            await ctx.send(f"Personajes disponibles: {', '.join(available_chars)}")

@bot.command()
@commands.has_role("Admin")
async def clear(ctx, amount: int):
    if amount <= 0:
        await ctx.send("Por favor, proporciona un número positivo de mensajes a borrar.")
        return
    
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f'Se han borrado {len(deleted)} mensajes.', delete_after=5)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("No tienes el rol necesario para usar este comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Por favor, proporciona un número de mensajes a borrar.")
    else:
        await ctx.send(f"Ocurrió un error: {str(error)}")

# Iniciar el bot
if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: No se encontró el token en el archivo .env")