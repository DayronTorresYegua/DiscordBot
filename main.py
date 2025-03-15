import os
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv

TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN and os.path.exists('.env'):
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents, case_insensitive=True, help_command=None) 

script_dir = os.path.dirname(os.path.abspath(__file__))
characters_file = os.path.join(script_dir, 'data.json')

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

@bot.command(name='help')
async def help_command(ctx):
    """Muestra información sobre los comandos disponibles"""
    embed = discord.Embed(
        title="Comandos de Bot Wuthering Waves",
        description="Aquí tienes la lista de comandos disponibles:",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name=">personaje [nombre]",
        value="Muestra información detallada sobre un personaje específico de Wuthering Waves.\n"
              "**Ejemplo:** `>personaje Rover`",
        inline=False
    )
    
    embed.add_field(
        name=">personajes",
        value="Muestra una lista de todos los personajes disponibles en el bot.",
        inline=False
    )
    
    embed.add_field(
        name=">clear [número]",
        value="*Solo para administradores*\n"
              "Borra un número específico de mensajes del canal actual.\n"
              "**Ejemplo:** `>clear 5`",
        inline=False
    )
    
    embed.add_field(
        name=">help",
        value="Muestra este mensaje de ayuda con información sobre todos los comandos disponibles.",
        inline=False
    )
    
    embed.add_field(
        name="Personajes disponibles",
        value="Para ver los personajes disponibles usa `>personajes`",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='personajes')
async def list_characters(ctx):
    """Muestra una lista de todos los personajes disponibles"""
    if not characters:
        await ctx.send("No hay personajes disponibles en este momento.")
        return
    
    embed = discord.Embed(
        title="Personajes disponibles en Wuthering Waves",
        description="Aquí tienes la lista de personajes sobre los que puedes consultar información:",
        color=discord.Color.green()
    )
    
    available_chars = [char_data.get('name', char_id) for char_id, char_data in characters.items()]
    
    # Ordenar alfabéticamente
    available_chars.sort()
    
    # Crear una lista formateada
    formatted_list = ""
    for char in available_chars:
        formatted_list += f"• {char}\n"
    
    embed.add_field(
        name="Personajes",
        value=formatted_list if formatted_list else "No hay personajes disponibles.",
        inline=False
    )
    
    embed.add_field(
        name="¿Cómo usar?",
        value="Para obtener información detallada sobre un personaje específico, usa el comando:\n"
              "`>personaje [nombre]`\n"
              "**Ejemplo:** `>personaje Rover`",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='personaje')
async def character_info(ctx, *, character_name=None):
    """Muestra información completa sobre un personaje de Wuthering Waves en un solo mensaje"""
    if character_name is None:
        await ctx.send("Por favor, especifica el nombre de un personaje. Ejemplo: `>personaje Rover`")
        return
    
    character_name = character_name.lower()
    character_found = None
    
    for char_id, char_data in characters.items():
        char_name = char_data.get('name', '').lower()
        if char_name == character_name:
            character_found = char_data
            break
    
    if character_found:
        embed = discord.Embed(
            title=f"{character_found['name']} - Guía completa",
            description=character_found.get('description', 'No hay descripción disponible'),
            color=discord.Color.blue()
        )
        
        basic_info = ""
        if 'rarity' in character_found:
            basic_info += f"**Rareza:** {character_found['rarity']}\n"
        if 'element' in character_found:
            basic_info += f"**Elemento:** {character_found['element']}\n"
        if 'weapon' in character_found:
            basic_info += f"**Arma:** {character_found['weapon']}\n"
        
        embed.add_field(name="Información básica", value=basic_info, inline=False)
        
        if 'recommended_builds' in character_found and character_found['recommended_builds']:
            build = character_found['recommended_builds'][0]  
            
            if 'echo_sets' in build:
                sets_info = build['echo_sets']
                sets_text = ""
                
                for set_name, pieces in sets_info.items():
                    sets_text += f"**{set_name}** ({pieces} piezas)\n"
                
                embed.add_field(name="Sets de Echos recomendados", value=sets_text, inline=False)
            
            if 'main_stats' in build:
                main_stats = build['main_stats']
                stats_text = ""
                
                for slot, stat in main_stats.items():
                    stats_text += f"**{slot}:** {stat}\n"
                
                embed.add_field(name="Estadísticas principales", value=stats_text, inline=False)
            
            if 'substats' in build:
                substats = build['substats']
                substats_text = "Prioridad: " + " > ".join(substats)
                
                embed.add_field(name="Subestadísticas recomendadas", value=substats_text, inline=False)
        
        if 'image_url' in character_found:
            embed.set_thumbnail(url=character_found['image_url'])
        
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"No se encontró información sobre el personaje '{character_name}'")
        await ctx.send("Para ver los personajes disponibles, usa `>personajes`")

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

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: No se encontró el token en las variables de entorno o en el archivo .env")