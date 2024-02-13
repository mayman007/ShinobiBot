import asyncio
import os
import discord
from discord import app_commands
from discord.ext import commands
import google.generativeai as genai


# AI Chat Class
class Chatbots(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #waking
    @commands.Cog.listener()
    async def on_ready(self):
        print("Chatbots is online.")

    # Gemini
    @app_commands.command(name = "gemini", description = "Chat with Google's Gemini Pro AI")
    @app_commands.describe(prompt = "The question you wanna ask.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def bard(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = await model.generate_content_async(prompt)
        response = response.text
        limit = 1800
        if len(response) > limit:
            result = [response[i: i + limit] for i in range(0, len(response), limit)]
            for half in result:
                await interaction.followup.send(f"Gemini Pro: {half}")
                await asyncio.sleep(0.5)
        else: await interaction.followup.send(f"Gemini Pro: {response}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Chatbots(bot))