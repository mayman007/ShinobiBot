import discord
from discord import app_commands
from discord.ext import commands
from Bard import AsyncChatbot as BardChatbot
from EdgeGPT.EdgeGPT import Chatbot as BingChatbot, ConversationStyle
from EdgeGPT.ImageGen import ImageGenAsync
import json
import io
import os
import aiohttp


class errorButtons(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Yes", style = discord.ButtonStyle.green)
    async def edits_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        try:
            await error_channel.send(error)
        except Exception as e:
            report_failed_message = f"Error report failed due to: {e}"
            await error_channel.send(report_failed_message)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Error sent to the developer.")
    @discord.ui.button(label = "No", style = discord.ButtonStyle.red)
    async def edits_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Cancelled.")

# AI Class
class AI(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #waking
    @commands.Cog.listener()
    async def on_ready(self):
        print("AI is online.")

    # MidJourney
    @app_commands.command(name = "midjourney", description = "Generate images using Midjourney-like model.")
    @app_commands.describe(prompt = "Describe the image.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def midjourney(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.send_message("Wanna generate images using powerful models? Use </imagine:1122943777326256413>!", ephemeral = True)

    # Imagine
    @app_commands.command(name = "imagine", description = "Generate images using powerful Stable Diffusion models.")
    @app_commands.describe(prompt = "Describe the image.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def imagine(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        try:
            API_URL = "https://api-inference.huggingface.co/models/prompthero/openjourney"
            headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_TOKEN')}"}
            payload = {"inputs": f"{prompt}, mdjrny-v4 style"}
            print(1)
            async with aiohttp.ClientSession(headers = headers) as session:
                print(2)
                async with session.post(API_URL, json = payload) as response:
                    print(3)
                    image_bytes =  await response.read()
                    print(4)
            with io.BytesIO(image_bytes) as file: # converts to file-like object
                print(5)
                await interaction.followup.send(f"Prompt: {prompt.strip()}", file = discord.File(file, "image.png"))
                print(6)
        except Exception as e:
            print(f"Imagine error: {e}")
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
            global error, error_channel
            error = f"Dalle: {e}"
            error_channel = self.bot.get_channel(int(os.getenv("ERROR_CHANNEL_ID")))
            embed = discord.Embed(title = "Error",
                                  description = f"Sorry, an unexpected error has occured, do you want to send the error message to the developer?",
                                  color = discord.Color.red())
            await interaction.followup.send(embed = embed, view = errorButtons())

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
            global error, error_channel
            error = f"BingImageCreator: {e}"
            error_channel = self.bot.get_channel(int(os.getenv("ERROR_CHANNEL_ID")))
            embed = discord.Embed(title = "Error",
                                  description = f"Sorry, an unexpected error has occured, do you want to send the error message to the developer?",
                                  color = discord.Color.red())
            await interaction.followup.send(embed = embed, view = errorButtons())

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
            cookies = json.loads(open("bing_cookies_*.json", encoding="utf-8").read()) # https://github.com/acheong08/EdgeGPT#collect-cookies
            bot = await BingChatbot.create(cookies=cookies)
            if conversation_style == None or conversation_style.value == "balanced": style = ConversationStyle.balanced
            elif conversation_style.value == "creative": style = ConversationStyle.creative
            elif conversation_style.value == "precise": style = ConversationStyle.precise
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
            global error, error_channel
            error = f"Bing: {e}"
            error_channel = self.bot.get_channel(int(os.getenv("ERROR_CHANNEL_ID")))
            embed = discord.Embed(title = "Error",
                                  description = f"Sorry, an unexpected error has occured, do you want to send the error message to the developer?",
                                  color = discord.Color.red())
            await interaction.followup.send(embed = embed, view = errorButtons())

    # Bard
    @app_commands.command(name = "bard", description = "Ask Bard.")
    @app_commands.describe(prompt = "The question you wanna ask.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def bard(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        try:
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
        except Exception as e:
            global error, error_channel
            error = f"Bard: {e}"
            error_channel = self.bot.get_channel(int(os.getenv("ERROR_CHANNEL_ID")))
            embed = discord.Embed(title = "Error",
                                  description = f"Sorry, an unexpected error has occured, do you want to send the error message to the developer?",
                                  color = discord.Color.red())
            await interaction.followup.send(embed = embed, view = errorButtons())

    # ChatGPT category
    chatgpt = app_commands.Group(name = "chatgpt", description = "ChatGPT")

    # ChatGPT Ask
    @chatgpt.command(name = "ask", description = "Ask ChatGPT-4.")
    @app_commands.describe(prompt = "The question you wanna ask.", model = "Default is GPT-4 unless if it has issues. (Only GPT-4 saves conversations)")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.choices(model = [app_commands.Choice(name = "GPT-4", value = "gpt-4"),
                                   app_commands.Choice(name = "GPT-3.5-Turbo", value = "gpt-3.5-turbo")])
    async def chatgpt_ask(self, interaction: discord.Interaction, prompt: str, model: app_commands.Choice[str] = None):
        await interaction.response.send_message("Wanna chat with GPT and other AI models? Use </chatbot:1112553506457526353>!", ephemeral = True)


    # Chatbot command
    @app_commands.command(name = "chatbot", description = "Chat with powerful AI models.")
    @app_commands.describe(prompt = "The question you wanna ask.", model = "Choose the AI model you wanna chat with.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.choices(model = [
                                    app_commands.Choice(name = "gpt-4", value = "gpt-4"),
                                    app_commands.Choice(name = "gpt-3.5-turbo", value = "gpt-3.5-turbo"),
                                    # app_commands.Choice(name = "alpaca-13b", value = "alpaca-13b"),
                                    # app_commands.Choice(name = "vicuna-13b", value = "vicuna-13b"),
                                    # app_commands.Choice(name = "koala-13b", value = "koala-13b"),
                                    # app_commands.Choice(name = "llama-13b", value = "llama-13b"),
                                    # app_commands.Choice(name = "oasst-pythia-12b", value = "oasst-pythia-12b"),
                                    # app_commands.Choice(name = "fastchat-t5-3b", value = "fastchat-t5-3b")
                                    ])
    async def chatbot(self, interaction: discord.Interaction, prompt: str, model: app_commands.Choice[str]):
        async def get_response(provider):
            if provider == "CATTO":
                api_key = os.getenv("CATTO_GPT")
                api_url = "https://api.cattto.repl.co/v1/chat/completions"
            elif provider == "CHURCHLESS":
                api_key = os.getenv("CHURCHLESS_AUTH")
                api_url = "https://free.churchless.tech/v1/chat/completions"
            elif provider == "FOX":
                api_key = os.getenv("FOX_API_KEY")
                api_url = "https://api.hypere.app/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            data = {
                "model": model.value,
                "max_tokens": 4000,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, headers = headers, data = json.dumps(data)) as response:
                    response = await response.text()
            response = json.loads(response)
            response = response["choices"][0]["message"]["content"]
            limit = 1800
            total_text = len(prompt) + len(response)
            if total_text > limit:
                result = [response[i: i + limit] for i in range(0, len(response), limit)]
                for half in result: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**{model.name}:** {half}")
            else: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**{model.name}:** {response}")

        await interaction.response.defer()
        try: await get_response("CATTO")
        except Exception as e:
            print(f"CATTO: {e}")
            try: await get_response(f"CHURCHLESS: {e}")
            except Exception as e:
                print(e)
                try: await get_response(f"FOX: {e}")
                except Exception as e:
                    global error, error_channel
                    error = f"{model.value}: {e}"
                    error_channel = self.bot.get_channel(int(os.getenv("ERROR_CHANNEL_ID")))
                    embed = discord.Embed(title = "Error",
                                          description = f"Sorry, an unexpected error has occured, do you want to send the error message to the developer?",
                                          color = discord.Color.red())
                    await interaction.followup.send(embed = embed, view = errorButtons())

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AI(bot))
