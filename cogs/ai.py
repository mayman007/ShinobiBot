import discord
from discord import app_commands
from discord.ext import commands
import revChatGPT.V1
import EdgeGPT
import openai
import Bard
import io
from ImageGen import ImageGenAsync
import os
import aiohttp
import asyncio

# AI Class
class AI(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #waking
    @commands.Cog.listener()
    async def on_ready(self):
        print("AI is online.")

    # bingimagecreator
    @app_commands.command(name = "bing_image", description = "Use Bing Image Creator to create images.")
    @app_commands.describe(prompt = "Describe the image.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def bing_image(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        try:
            auth_cookie = os.getenv("BING_AUTH_COOKIE") # visit https://github.com/acheong08/BingImageCreator for guide on how to get
            async with ImageGenAsync(auth_cookie, quiet = True) as image_generator:
                images_links = await image_generator.get_images(prompt)
            images_list = []
            for image_link in images_links:
                async with aiohttp.ClientSession() as session: # creates session
                    async with session.get(image_link) as resp: # gets image from url
                        img = await resp.read() # reads image from response
                        with io.BytesIO(img) as file: # converts to file-like object
                            file = discord.File(file, "image.png")
                            images_list.append(file)
            await interaction.followup.send(f"Prompt: {prompt}", files = images_list)
        except Exception as e:
            print(f"BingImageCreator error: {e}")
            await interaction.followup.send("Sorry, an unexpected error has occured.")

    # midjourney
    @app_commands.command(name = "midjourney", description = "Use MidJourney AI to create images.")
    @app_commands.describe(prompt = "Describe the image.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def midjourney(self, interaction: discord.Interaction, prompt: str):
        banned_words = ["sex", "s.ex", "se.x",
                        "porn", "p.orn", "po.rn", "por.n",
                        "pussy", "p.ussy", "pu.ssy", "pus.sy", "puss.y",
                        "boob", "b.oob", "bo.ob", "boo.b",
                        "tits", "t.its", "ti.ts", "tit.s",
                        "nude", "n.ude", "nu.de", "nud.e",
                        "nake", "n.ake", "na.ke", "nak.e"]
        for word in banned_words:
            if word in prompt.lower(): return await interaction.response.send_message("I can't do that.")
        await interaction.response.defer()
        try:
            API_TOKEN = os.getenv("MJ_TOKEN") # search for openjourney
            API_URL = "https://api-inference.huggingface.co/models/prompthero/openjourney"
            headers = {"Authorization": f"Bearer {API_TOKEN}"}
            payload = {"inputs": f"{prompt}, mdjrny-v4 style"}
            async with aiohttp.ClientSession(headers = headers) as session:
                async with session.post(API_URL, json = payload) as response:
                    image_bytes =  await response.read()
            with io.BytesIO(image_bytes) as file: # converts to file-like object
                await interaction.followup.send(f"Prompt: {prompt.strip()}", file = discord.File(file, "image.png"))
        except Exception as e:
            print(f"MidJourney error: {e}")
            await interaction.followup.send("Sorry, an unexpected error has occured.")

    # bard
    @app_commands.command(name = "bard", description = "Ask Bard.")
    @app_commands.describe(prompt = "The question you wanna ask.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def bard(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        try:
            session_cookie = os.getenv("BARD_COOKIE") # visit https://github.com/acheong08/Bard for guide on how to get
            bot = Bard.Chatbot(session_cookie)
            response = bot.ask(prompt)
            response = str(response).split("{'content': ")[1].split(", 'conversation_id")[0].replace("\\n", "\n").replace("\\'", "'").replace('\\"', '"')[1:-1]
            limit = 1900
            total_text = len(prompt) + len(response)
            if total_text > limit:
                result = [response[i: i + limit] for i in range(0, len(response), limit)]
                for half in result: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**Bard:** {half}")
            else: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**Bard:** {response}")
        except Exception as e:
            print(f"Bard error: {e}")
            await interaction.followup.send("Sorry, an unexpected error has occured.")

    # dalle
    @app_commands.command(name = "dalle", description = "Use Dall-E AI to create images.")
    @app_commands.describe(prompt = "Describe the image.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def dalle(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        try:
            openai.api_key = "" # leave ths blank
            openai.api_base = "https://api.hypere.app"
            try:
                img = openai.Image.create(
                    prompt = prompt,
                    n = 1,
                    size = "1024x1024"
                )
            except openai.error.InvalidRequestError as e: return await interaction.followup.send(e)
            image_url = str(img).split('"url": "')[1].split('"')[0]
            embed = discord.Embed(colour = 0x2F3136)
            embed.set_image(url = image_url)
            await interaction.followup.send(f"Prompt: {prompt}", embed = embed)
        except Exception as e:
            print(f"Dalle error: {e}")
            await interaction.followup.send("Sorry, an unexpected error has occured.")

    # bing
    @app_commands.command(name = "bing", description = "Ask Bing AI.")
    @app_commands.describe(prompt = "The question you wanna ask.", conversation_style = "default is balanced")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.choices(conversation_style = [app_commands.Choice(name = "creative", value = "creative"),
                                                app_commands.Choice(name = "balanced", value = "balanced"),
                                                app_commands.Choice(name = "precise", value = "precise")])
    async def bing(self, interaction: discord.Interaction, prompt: str, conversation_style: app_commands.Choice[str] = None):
        await interaction.response.defer()
        try:
            bot = EdgeGPT.Chatbot(cookiePath = os.getenv("BING_COOKIE_DIR")) # visit https://github.com/acheong08/EdgeGPT for guide on how to get
            if conversation_style == None or conversation_style.value == "balanced": style = EdgeGPT.ConversationStyle.balanced
            elif conversation_style.value == "creative": style = EdgeGPT.ConversationStyle.creative
            elif conversation_style.value == "precise": style = EdgeGPT.ConversationStyle.precise
            response = await bot.ask(prompt = prompt, conversation_style = style)
            response = str(response).split("[{'type': 'TextBlock', 'text': ")[1].split(", 'wrap': True}")[0].replace("\\n", "\n").replace("\\'", "'").replace('\\"', '"')[1:-1]
            limit = 1900
            total_text = len(prompt) + len(response)
            if total_text > limit:
                result = [response[i: i + limit] for i in range(0, len(response), limit)]
                for half in result: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**Bing AI:** {half}")
            else: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**Bing AI:** {response}")
            await bot.close()
        except Exception as e:
            print(f"Bing error: {e}")
            await interaction.followup.send("Sorry, an unexpected error has occured.")

    # chatgpt
    @app_commands.command(name = "chatgpt", description = "Ask ChatGPT-4.")
    @app_commands.describe(prompt = "The question you wanna ask.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def chatgpt(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        try:
            chatbot = revChatGPT.V1.Chatbot(config = {"email": os.getenv("CHATGPT_EMAIL"),
                                                      "password": os.getenv("CHATGPT_PASS"),
                                                      "model": "gpt-4"
                                                      }
                                            )
            response = ""
            while True:
                try:
                    for data in chatbot.ask(prompt): response = data["message"]
                    break
                except revChatGPT.typings.Error: await asyncio.sleep(2)
            limit = 1900
            total_text = len(prompt) + len(response)
            if total_text > limit:
                result = [response[i: i + limit] for i in range(0, len(response), limit)]
                for half in result: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**ChatGPT-4:** {half}")
            else: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**ChatGPT-4:** {response}")
        except Exception as e:
            print(f"Chatgpt error: {e}")
            await interaction.followup.send("Sorry, an unexpected error has occured.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AI(bot))