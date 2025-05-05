import os
import json
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import asyncio

# Initial setup
app = Flask(__name__)

@app.route('/')
def home():
    return "Wuthering Waves Bot is online"

@app.route('/health')
def health_check():
    return "OK", 200

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents, case_insensitive=True, help_command=None)

# Load character data (improved version)
def load_characters():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        characters_file = os.path.join(script_dir, 'data.json')
        
        with open(characters_file, 'r', encoding='utf-8') as f:
            print(f"✅ Data loaded from: {characters_file}")
            data = json.load(f)
            print(f"👥 Available characters: {len(data)}")
            return data
    except FileNotFoundError:
        print("❌ Error: data.json file not found")
        return {}
    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON format in data.json")
        return {}
    except Exception as e:
        print(f"❌ Unexpected error loading data: {e}")
        return {}

characters = load_characters()

@bot.event
async def on_ready():
    print(f'✅ Bot connected as {bot.user.name}')
    print(f'🆔 Bot ID: {bot.user.id}')
    print('------')
    await bot.change_presence(activity=discord.Game(name="Wuthering Waves | >help"))

@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(
        title="Wuthering Waves Bot Commands",
        description="Here's the list of available commands:",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name=">character [name]",
        value="Shows detailed information about a specific Wuthering Waves character.\n"
              "**Example:** >character Rover",
        inline=False
    )
    
    embed.add_field(
        name=">characters",
        value="Shows a list of all available characters in the bot.",
        inline=False
    )
    
    embed.add_field(
        name=">clear [number]",
        value="*Only for administrators*\n"
              "Deletes a specific number of messages from the current channel.\n"
              "**Example:** >clear 5",
        inline=False
    )
    
    embed.add_field(
        name=">help",
        value="Shows this help message with information about all available commands.",
        inline=False
    )
    
    embed.add_field(
        name=">ping",
        value="Checks if the bot is online and responds with 'Pong!'",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong! Latency: {0}ms'.format(round(bot.latency * 1000, 1)))

@bot.command(name='characters')
async def list_characters(ctx):
    if not characters:
        await ctx.send("No characters available at the moment.")
        return
    
    embed = discord.Embed(
        title="Available Characters in Wuthering Waves",
        description="Here's the list of characters you can get information about:",
        color=discord.Color.green()
    )
    
    available_chars = [char_data.get('name', char_id) for char_id, char_data in characters.items()]
    available_chars.sort()
    
    formatted_list = ""
    for char in available_chars:
        formatted_list += f"• {char}\n"
    
    embed.add_field(
        name="Characters",
        value=formatted_list if formatted_list else "No characters available.",
        inline=False
    )
    
    embed.add_field(
        name="How to use?",
        value="To get detailed information about a specific character, use the command:\n"
              ">character [name]\n"
              "**Example:** >character Rover",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='character')
async def character_info(ctx, *, character_name=None):
    if character_name is None:
        await ctx.send("Please specify a character name. Example: >character Rover")
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
            title=f"{character_found['name']} - Complete Guide",
            color=discord.Color.blue()
        )
        
        basic_info = ""
        if 'rarity' in character_found:
            basic_info += f"**Rarity:** {character_found['rarity']}\n"
        if 'element' in character_found:
            basic_info += f"**Element:** {character_found['element']}\n"
        if 'weapon' in character_found:
            basic_info += f"**Weapon:** {character_found['weapon']}\n"
        
        embed.add_field(name="Basic Information", value=basic_info, inline=False)
        
        if 'recommended_builds' in character_found and character_found['recommended_builds']:
            build = character_found['recommended_builds'][0]  
            
            if 'echo_sets' in build:
                sets_info = build['echo_sets']
                sets_text = ""
                
                for set_name, pieces in sets_info.items():
                    sets_text += f"**{set_name}** ({pieces} pieces)\n"
                
                embed.add_field(name="Recommended Echo Sets", value=sets_text, inline=False)
            
            if 'main_stats' in build:
                main_stats = build['main_stats']
                stats_text = ""
                
                for slot, stat in main_stats.items():
                    stats_text += f"**{slot}:** {stat}\n"
                
                embed.add_field(name="Main Stats", value=stats_text, inline=False)
            
            if 'substats' in build:
                substats = build['substats']
                substats_text = "Priority: " + " > ".join(substats)
                
                embed.add_field(name="Recommended Substats", value=substats_text, inline=False)
        
        if 'image_url' in character_found:
            embed.set_thumbnail(url=character_found['image_url'])
        
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"No information found for character '{character_name}'")
        await ctx.send("To see available characters, use >characters")

@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):
    if amount <= 0:
        await ctx.send("Please provide a positive number of messages to delete.")
        return
    
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f'{len(deleted)} messages have been deleted.', delete_after=5)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have administrator permissions to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide a number of messages to delete.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")

# Improved bot startup handling
async def run_bot():
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ Error: DISCORD_TOKEN not found in environment variables")
        return

    try:
        print("🚀 Starting bot...")
        await bot.start(token)
    except discord.LoginError:
        print("❌ Error: Invalid Discord token")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        if not bot.is_closed():
            await bot.close()

if __name__ == "__main__":
    # Start Flask in a separate thread (as daemon)
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Configuration for Render - handling async events
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(run_bot())
    except KeyboardInterrupt:
        print("\n🔴 Bot stopped manually")
    finally:
        loop.close()