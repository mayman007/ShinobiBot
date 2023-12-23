import discord
from discord import app_commands
from discord.ext import commands
from Bard import AsyncChatbot as BardChatbot
import io
import os
import aiohttp


# AI Chat Class
class Chatbots(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #waking
    @commands.Cog.listener()
    async def on_ready(self):
        print("Chatbots is online.")

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
        images_links = []
        if images != set():
            for image in images:
                images_links.append(image)
        if images_links != []:
            images_list = []
            for image_link in images_links:
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_link) as resp:
                        img = await resp.read()
                        with io.BytesIO(img) as file:
                            file = discord.File(file, "image.png")
                            images_list.append(file)
        limit = 1800
        total_text = len(prompt) + len(response)
        if total_text > limit:
            result = [response[i: i + limit] for i in range(0, len(response), limit)]
            image_already_sent = False
            for half in result:
                if images_links == []:
                    await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**Bard:** {half}")
                else:
                    if image_already_sent == False:
                        await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**Bard:** {half}", files = images_list)
                        image_already_sent = True
                    else:
                        await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**Bard:** {half}")
        else:
            if images_links == []:
                await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**Bard:** {response}")
            else:
                await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**Bard:** {response}", files = images_list)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Chatbots(bot))