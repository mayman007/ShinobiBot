import discord
from discord import app_commands
from discord.ext import commands
from Bard import AsyncChatbot as BardChatbot
from EdgeGPT.ImageGen import ImageGenAsync
import io
import os
import aiohttp


# AI Class
class AI(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #waking
    @commands.Cog.listener()
    async def on_ready(self):
        print("AI is online.")

    # Imagine
    @app_commands.command(name = "imagine", description = "Generate images using DALLE-3")
    @app_commands.describe(prompt = "Describe the image.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def imagine(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
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

    # Bard
    @app_commands.command(name = "bard", description = "Ask Bard.")
    @app_commands.describe(prompt = "The question you wanna ask.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def bard(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        Secure_1PSID = os.getenv("BARD_SECURE_1PSID")
        Secure_1PSIDTS = os.getenv("BARD_SECURE_1PSIDTS")
        chatbot = await BardChatbot.create(Secure_1PSID, Secure_1PSIDTS)
        response = await chatbot.ask(prompt)
        images = response['images']
        response = response['content']
        if images != set():
            bard_images_counter = 0
            response = f"{response}\n\n"
            for image in images:
                bard_images_counter += 1
                response += f"\nImage {bard_images_counter}: {image}"
        limit = 1800
        total_text = len(prompt) + len(response)
        if total_text > limit:
            result = [response[i: i + limit] for i in range(0, len(response), limit)]
            for half in result: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**Bard:** {half}")
        else: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**Bard:** {response}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AI(bot))
