import discord
from discord import app_commands
from discord.ext import commands
import io
import os
import aiohttp


# AI ImageGenerations Class
class ImageGenerations(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #waking
    @commands.Cog.listener()
    async def on_ready(self):
        print("ImageGenerations is online.")

    # Imagine
    @app_commands.command(name = "imagine", description = "Generate images using Stable Diffusion")
    @app_commands.describe(prompt = "Describe the image")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def imagine(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        API_URL = "https://api-inference.huggingface.co/models/prompthero/openjourney"
        headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_TOKEN')}"}
        payload = {"inputs": f"{prompt}, mdjrny-v4 style"}
        async with aiohttp.ClientSession(headers = headers) as session:
            async with session.post(API_URL, json = payload) as response:
                image_bytes =  await response.read()
        with io.BytesIO(image_bytes) as file: # converts to file-like object
            await interaction.followup.send(f"Prompt: {prompt.strip()}", file = discord.File(file, "image.png"))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ImageGenerations(bot))