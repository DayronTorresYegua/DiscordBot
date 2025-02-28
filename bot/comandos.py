import discord
from discord.ext import commands
import requests

class PersonajeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="personaje")
    async def personaje(self, ctx, *, nombre: str):
        response = requests.get(f"{self.bot.api_url}/personajes/{nombre.lower()}")
        data = response.json()

        if "error" in data:
            await ctx.send("❌ Personaje no encontrado.")
            return

        embed = discord.Embed(title=data["nombre"], color=discord.Color.blue())
        embed.set_image(url=f"{self.bot.api_url}{data['imagen']}")
        embed.add_field(name="Elemento", value=data["elemento"])
        embed.add_field(name="Rareza", value=f"⭐ {data['rareza']}")
        embed.add_field(name="Arma Recomendada", value=data["arma_recomendada"])
        embed.add_field(name="Set de Ecos", value=data["set_de_ecos"])
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(PersonajeCommand(bot))
