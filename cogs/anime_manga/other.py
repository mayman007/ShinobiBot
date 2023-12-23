import ast
import io
import aiohttp
import aiosqlite
import discord
from discord import app_commands
from discord.ext import commands


# Anime Other Class
class AnimeMangaOther(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("AnimeMangaOther is online.")

    # aghpb
    @app_commands.command(name = "aghpb", description = "Anime girls holding programming books")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def aghpb(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.devgoldy.xyz/aghpb/v1/random") as response:
                img = await response.read()
                with io.BytesIO(img) as file:
                    file = discord.File(file, "aghpb.png")
        await interaction.response.send_message(file=file)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AnimeMangaOther(bot))