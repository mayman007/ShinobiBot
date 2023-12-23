import discord
from discord import app_commands
from discord.ext import commands
from EdgeGPT.ImageGen import ImageGenAsync
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
    @app_commands.command(name = "imagine", description = "Generate images using AI models")
    @app_commands.describe(prompt = "Describe the image.", model = "The model to use (Default is Dalle-3).")
    @app_commands.choices(model = [app_commands.Choice(name = "Dalle-3", value = "dalle"),
                                  app_commands.Choice(name = "Stable Diffusion (Prototype)", value = "sd")])
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def imagine(self, interaction: discord.Interaction, prompt: str, model: app_commands.Choice[str] = None):
        await interaction.response.defer()
        if model == None or model.value == "dalle":
            auth_cookie = os.getenv("BING_AUTH_COOKIE")
            async with ImageGenAsync(auth_cookie, quiet = True) as image_generator:
                images_links = await image_generator.get_images(prompt)
            images_list = []
            for image_link in images_links:
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_link) as resp:
                        img = await resp.read()
                        with io.BytesIO(img) as file:
                            file = discord.File(file, "image.png")
                            images_list.append(file)
            await interaction.followup.send(f"Prompt: {prompt}", files = images_list)
        elif model.value == "sd":
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