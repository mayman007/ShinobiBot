import discord
from discord import app_commands
from discord.ext import commands
import revChatGPT
from revChatGPT.V1 import AsyncChatbot as GPTChatbot
from Bard import Chatbot as BardChatbot
import EdgeGPT
from EdgeGPT import Chatbot as BingChatbot
from ImageGen import ImageGenAsync
import json
import io
import os
import aiohttp
import aiosqlite
import asyncio

# AI Class
class AI(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #waking
    @commands.Cog.listener()
    async def on_ready(self):
        print("AI is online.")

    # MidJourney
    @app_commands.command(name = "midjourney", description = "Generate an image using fine-tuned Stable Diffustion trained on midjourney images.")
    @app_commands.describe(prompt = "Describe the image.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def midjourney(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        with open("cogs/swear_words.txt") as file:
            while line := file.readline():
                line = line.rstrip()
                if line in prompt.lower():
                    return await interaction.followup.send("I detected an inappropriate word, I can't generate that.", ephemeral = True)
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
            await interaction.followup.send("Sorry, an unexpected error has occured.", ephemeral = True)

    # Dall-E
    @app_commands.command(name = "dalle", description = "Generate images using Dall-E.")
    @app_commands.describe(prompt = "Describe the image.", number_of_images = "default is 1.", size = "default is 1024x1024.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.choices(size = [app_commands.Choice(name = "256x256", value = "256x256"),
                                  app_commands.Choice(name = "512x512 ", value = "512x512"),
                                  app_commands.Choice(name = "1024x1024", value = "1024x1024")])
    async def dalle(self, interaction: discord.Interaction, prompt: str, number_of_images: int = None, size: app_commands.Choice[str] = None):
        if number_of_images == None: number_of_images = 1
        elif number_of_images > 5: return await interaction.response.send_message("The maximum number of images is 5.", ephemeral = True)
        if size == None: size = "1024x1024"
        else: size = size.value
        await interaction.response.defer()
        try:
            api_key = os.getenv("FOX_API_KEY")
            api_url = "https://api.hypere.app/images/generations"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            data = {
                "prompt": prompt,
                "n": number_of_images,
                "size": size
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, headers = headers, data = json.dumps(data)) as response:
                    images = await response.text()
            images_dict = json.loads(images)
            images_list = []
            for image_url in images_dict["data"]:
                async with aiohttp.ClientSession() as session: # creates session
                    async with session.get(str(image_url["url"])) as response: # gets image from url
                        image = await response.read() # reads image from response
                        with io.BytesIO(image) as file: # converts to file-like object
                            file = discord.File(file, "image.png")
                            images_list.append(file)
            await interaction.followup.send(f"Prompt: {prompt}", files = images_list)
        except Exception as e:
            print(f"Dalle error: {e}")
            await interaction.followup.send("Sorry, an unexpected error has occured.", ephemeral = True)

    # Bing category
    bing = app_commands.Group(name = "bing", description = "Bing AI")

    # Bing Image Creator
    @bing.command(name = "image_creator", description = "Generate images using Bing Image Creator.")
    @app_commands.describe(prompt = "Describe the image.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def bing_image_creator(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        try:
            auth_cookie = os.getenv("BING_AUTH_COOKIE") # visit https://github.com/acheong08/EdgeGPT for guide on how to get
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
            await interaction.followup.send("Sorry, an unexpected error has occured.", ephemeral = True)

    # Bing Ask
    @bing.command(name = "ask", description = "Ask Bing AI.")
    @app_commands.describe(prompt = "The question you wanna ask.", conversation_style = "default is balanced")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.choices(conversation_style = [app_commands.Choice(name = "creative", value = "creative"),
                                                app_commands.Choice(name = "balanced", value = "balanced"),
                                                app_commands.Choice(name = "precise", value = "precise")])
    async def bing_chat(self, interaction: discord.Interaction, prompt: str, conversation_style: app_commands.Choice[str] = None):
        await interaction.response.defer()
        try:
            bot = BingChatbot(cookiePath = os.getenv("BING_COOKIE_DIR")) # visit https://github.com/acheong08/EdgeGPT for guide on how to get
            if conversation_style == None or conversation_style.value == "balanced": style = EdgeGPT.ConversationStyle.balanced
            elif conversation_style.value == "creative": style = EdgeGPT.ConversationStyle.creative
            elif conversation_style.value == "precise": style = EdgeGPT.ConversationStyle.precise
            response = await bot.ask(prompt = prompt, conversation_style = style)
            response = str(response).split("[{'type': 'TextBlock', 'text': ")[1].split(", 'wrap': True}")[0].replace("\\n", "\n").replace("\\'", "'").replace('\\"', '"')[1:-1]
            limit = 1800
            total_text = len(prompt) + len(response)
            if total_text > limit:
                result = [response[i: i + limit] for i in range(0, len(response), limit)]
                for half in result: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**Bing AI:** {half}")
            else: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**Bing AI:** {response}")
            await bot.close()
        except Exception as e:
            print(f"Bing error: {e}")
            await interaction.followup.send("Sorry, an unexpected error has occured.", ephemeral = True)

    # Bard
    @app_commands.command(name = "bard", description = "Ask Bard.")
    @app_commands.describe(prompt = "The question you wanna ask.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def bard(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        try:
            session_cookie = os.getenv("BARD_COOKIE") # visit https://github.com/acheong08/Bard for guide on how to get
            bot = BardChatbot(session_cookie)
            response = bot.ask(prompt)
            response = str(response).split("{'content': ")[1].split(", 'conversation_id")[0].replace("\\n", "\n").replace("\\'", "'").replace('\\"', '"')[1:-1]
            limit = 1800
            total_text = len(prompt) + len(response)
            if total_text > limit:
                result = [response[i: i + limit] for i in range(0, len(response), limit)]
                for half in result: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**Bard:** {half}")
            else: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**Bard:** {response}")
        except Exception as e:
            print(f"Bard error: {e}")
            await interaction.followup.send("Sorry, an unexpected error has occured.", ephemeral = True)

    # ChatGPT category
    chatgpt = app_commands.Group(name = "chatgpt", description = "ChatGPT")

    # ChatGPT Reset Chat
    @chatgpt.command(name = "reset_chat", description = "Resets your conversation with ChatGPT-4.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def chatgpt_reset_chat(self, interaction: discord.Interaction):
        await interaction.response.defer()
        async with aiosqlite.connect("db/chatgpt_convos.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS convos (convo_id TEXT, user ID)") # Create the table if not exists
                await cursor.execute("SELECT convo_id FROM convos WHERE user = ?", (interaction.user.id,))
                data = await cursor.fetchone()
                if data:
                    await cursor.execute("DELETE FROM convos WHERE user = ?", (interaction.user.id,))
                    await interaction.followup.send("Your conversation with ChatGPT has been reseted successfully.")
                else:
                    await interaction.followup.send("You don't have a conversation with ChatGPT yet, start one with </chatgpt ask:1088511615072206962>!", ephemeral = True)
            await db.commit()

    # ChatGPT Ask
    @chatgpt.command(name = "ask", description = "Ask ChatGPT-4.")
    @app_commands.describe(prompt = "The question you wanna ask.", model = "Default is GPT-4 unless if it has issues.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.choices(model = [app_commands.Choice(name = "GPT-4", value = "gpt-4"),
                                   app_commands.Choice(name = "GPT-3.5-Turbo", value = "gpt-3.5-turbo")])
    async def chatgpt_ask(self, interaction: discord.Interaction, prompt: str, model: app_commands.Choice[str] = None):
        await interaction.response.defer()
        gpt3_api_key = os.getenv("FOX_API_KEY")
        gpt3_api_url = "https://api.hypere.app/v1/chat/completions"
        gpt3_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {gpt3_api_key}"
        }
        gpt3_data = {
            "model": "gpt-3.5-turbo",
            "max_tokens": 4000,
            "messages": [
                {
                    "role": "system",
                    "content": "You are ChatGPT, an helpful assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        if model == None or model.value == "gpt-4":
            try:
                chatbot = GPTChatbot(config = {"access_token": os.getenv("CHATGPT_ACCESS_TOKEN")})
                response = ""
                async with aiosqlite.connect("db/chatgpt_convos.db") as db: # Open the db
                    async with db.cursor() as cursor:
                        await cursor.execute("CREATE TABLE IF NOT EXISTS convos (convo_id TEXT, user ID)") # Create the table if not exists
                        await cursor.execute("SELECT convo_id FROM convos WHERE user = ?", (interaction.user.id,))
                        data = await cursor.fetchone()
                        if data:
                            convo_id = data[0]
                            try:
                                await chatbot.get_msg_history(convo_id)
                            except:
                                await cursor.execute("DELETE FROM convos WHERE user = ?", (interaction.user.id,))
                                await db.commit()
                                try:
                                    while True:
                                        async for data in chatbot.ask(prompt, model = "gpt-4"):
                                            response = data["message"]
                                            convo_id = data["conversation_id"]
                                            await cursor.execute("INSERT INTO convos (convo_id, user) VALUES (?, ?)", (convo_id, interaction.user.id,))
                                            await db.commit()
                                            break
                                except revChatGPT.typings.Error: await asyncio.sleep(2)
                            else:
                                while True:
                                    try:
                                        async for data in chatbot.ask(prompt, conversation_id = convo_id, model = "gpt-4"): response = data["message"]
                                        break
                                    except revChatGPT.typings.Error:
                                        await asyncio.sleep(2)
                        else:
                            while True:
                                try:
                                    async for data in chatbot.ask(prompt, model = "gpt-4"):
                                        response = data["message"]
                                        convo_id = data["conversation_id"]
                                        await cursor.execute("INSERT INTO convos (convo_id, user) VALUES (?, ?)", (convo_id, interaction.user.id,))
                                        await db.commit()
                                    break
                                except revChatGPT.typings.Error: await asyncio.sleep(2)
                limit = 1800
                total_text = len(prompt) + len(response)
                if total_text > limit:
                    result = [response[i: i + limit] for i in range(0, len(response), limit)]
                    for half in result: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**ChatGPT-4:** {half}")
                else: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**ChatGPT-4:** {response}")
            except Exception as e:
                if model == None:
                    try:
                        async with aiohttp.ClientSession() as session:
                            async with session.post(gpt3_api_url, headers = gpt3_headers, data = json.dumps(gpt3_data)) as response:
                                response = await response.text()
                        response = response.split('{"role":"assistant","content":"')[1].split('"},"finish_reason"')[0].replace("\\n", "\n").replace("\\'", "'").replace('\\"', '"')
                        limit = 1800
                        total_text = len(prompt) + len(response)
                        if total_text > limit:
                            result = [response[i: i + limit] for i in range(0, len(response), limit)]
                            for half in result: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**ChatGPT-3.5-Turbo:** {half}")
                        else: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**ChatGPT-3.5-Turbo:** {response}")
                    except Exception as e:
                        print(f"Chatgpt error (gpt-3.5-turbo): {e}")
                        await interaction.followup.send("Sorry, an unexpected error has occured.", ephemeral = True)
                elif model.value == "gpt-4":
                    print(f"Chatgpt error (gpt-4): {e}")
                    await interaction.followup.send("Sorry, an unexpected error has occured in GPT-4, Try changing the model to GPT-3-Turbo.", ephemeral = True)
        elif model.value == "gpt-3.5-turbo":
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(gpt3_api_url, headers = gpt3_headers, data = json.dumps(gpt3_data)) as response:
                        response = await response.text()
                response = response.split('{"role":"assistant","content":"')[1].split('"},"finish_reason"')[0].replace("\\n", "\n").replace("\\'", "'").replace('\\"', '"')
                limit = 1800
                total_text = len(prompt) + len(response)
                if total_text > limit:
                    result = [response[i: i + limit] for i in range(0, len(response), limit)]
                    for half in result: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**ChatGPT-3.5-Turbo:** {half}")
                else: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**ChatGPT-3.5-Turbo:** {response}")
            except Exception as e:
                print(f"Chatgpt error (gpt-3.5-turbo): {e}")
                await interaction.followup.send("Sorry, an unexpected error has occured in GPT-3.5-Turbo, Try changing the model to GPT-4.", ephemeral = True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AI(bot))
