import os
import json
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import asyncio

# Configuración inicial
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Wuthering Waves está en línea"

@app.route('/health')
def health_check():
    return "OK", 200

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# Configuración del bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents, case_insensitive=True, help_command=None)

# Cargar datos de personajes (versión mejorada)
def load_characters():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        characters_file = os.path.join(script_dir, 'data.json')
        
        with open(characters_file, 'r', encoding='utf-8') as f:
            print(f"✅ Datos cargados desde: {characters_file}")
            data = json.load(f)
            print(f"👥 Personajes disponibles: {len(data)}")
            return data
    except FileNotFoundError:
        print("❌ Error: Archivo data.json no encontrado")
        return {}
    except json.JSONDecodeError:
        print("❌ Error: Formato JSON inválido en data.json")
        return {}
    except Exception as e:
        print(f"❌ Error inesperado al cargar datos: {e}")
        return {}

characters = load_characters()

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user.name}')
    print(f'🆔 ID del bot: {bot.user.id}')
    print('------')
    await bot.change_presence(activity=discord.Game(name="Wuthering Waves | >help"))

@bot.command(name='help')
async def help_command(ctx):
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
        name=">ping",
        value="Comprueba si el bot está en línea y responde con 'Pong!'",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong! Latencia: {0}ms'.format(round(bot.latency * 1000, 1)))

@bot.command(name='personajes')
async def list_characters(ctx):
    if not characters:
        await ctx.send("No hay personajes disponibles en este momento.")
        return
    
    embed = discord.Embed(
        title="Personajes disponibles en Wuthering Waves",
        description="Aquí tienes la lista de personajes sobre los que puedes consultar información:",
        color=discord.Color.green()
    )
    
    available_chars = [char_data.get('name', char_id) for char_id, char_data in characters.items()]
    available_chars.sort()
    
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

# Manejo mejorado del inicio del bot
async def run_bot():
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ Error: No se encontró DISCORD_TOKEN en las variables de entorno")
        return

    try:
        print("🚀 Iniciando bot...")
        await bot.start(token)
    except discord.LoginError:
        print("❌ Error: Token de Discord inválido")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    finally:
        if not bot.is_closed():
            await bot.close()

if __name__ == "__main__":
    # Iniciar Flask en un hilo separado (como daemon)
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Configuración para Render - manejo de eventos asíncronos
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(run_bot())
    except KeyboardInterrupt:
        print("\n🔴 Bot detenido manualmente")
    finally:
        loop.close()