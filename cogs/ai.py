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
from imaginepy import AsyncImagine, Style, Ratio


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
    @app_commands.describe(prompt = "Describe the image.", style = "Default is IMAGINE_V4_Beta.", ratio = "Default is 4x3.", number_of_images = "Default is 1, maximum is 4.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.choices(style = [app_commands.Choice(name = "IMAGINE_V4_Beta", value = "IMAGINE_V4_Beta"),
                                  app_commands.Choice(name = "IMAGINE_V3 ", value = "IMAGINE_V3"),
                                  app_commands.Choice(name = "IMAGINE_V1 ", value = "IMAGINE_V1"),
                                  app_commands.Choice(name = "V4_CREATIVE ", value = "V4_CREATIVE"),
                                  app_commands.Choice(name = "COSMIC ", value = "COSMIC"),
                                  app_commands.Choice(name = "ANIME ", value = "ANIME"),
                                  app_commands.Choice(name = "ANIME_V2 ", value = "ANIME_V2"),
                                  app_commands.Choice(name = "CANDYLAND ", value = "CANDYLAND"),
                                  app_commands.Choice(name = "CYBERPUNK ", value = "CYBERPUNK"),
                                  app_commands.Choice(name = "VIBRANT ", value = "VIBRANT"),
                                  app_commands.Choice(name = "CINEMATIC_RENDER ", value = "CINEMATIC_RENDER"),
                                  app_commands.Choice(name = "SURREALISM ", value = "SURREALISM"),
                                  app_commands.Choice(name = "LOGO ", value = "LOGO"),
                                  app_commands.Choice(name = "GTA ", value = "GTA")
                                  ])
    @app_commands.choices(ratio = [app_commands.Choice(name = "16x9", value = "16x9"),
                                  app_commands.Choice(name = "1x1 ", value = "16x9"),
                                  app_commands.Choice(name = "3x2 ", value = "16x9"),
                                  app_commands.Choice(name = "4x3 ", value = "16x9"),
                                  app_commands.Choice(name = "9x16 ", value = "16x9")
                                  ])
    async def midjourney(self, interaction: discord.Interaction, prompt: str,
                         style: app_commands.Choice[str] = None,
                         ratio: app_commands.Choice[str] = None,
                         number_of_images: int = None):
        await interaction.response.defer()
        imagine = AsyncImagine()

        if style == None: style = Style.IMAGINE_V4_Beta
        elif style.value == "IMAGINE_V4_Beta": style = Style.IMAGINE_V4_Beta
        elif style.value == "IMAGINE_V3": style = Style.IMAGINE_V3
        elif style.value == "IMAGINE_V1": style = Style.IMAGINE_V1
        elif style.value == "V4_CREATIVE": style = Style.V4_CREATIVE
        elif style.value == "COSMIC": style = Style.COSMIC
        elif style.value == "ANIME": style = Style.ANIME
        elif style.value == "ANIME_V2": style = Style.ANIME_V2
        elif style.value == "CANDYLAND": style = Style.CANDYLAND
        elif style.value == "CYBERPUNK": style = Style.CYBERPUNK
        elif style.value == "VIBRANT": style = Style.VIBRANT
        elif style.value == "CINEMATIC_RENDER": style = Style.CINEMATIC_RENDER
        elif style.value == "SURREALISM": style = Style.SURREALISM
        elif style.value == "LOGO": style = Style.LOGO
        elif style.value == "GTA": style = Style.GTA
        if ratio == None: ratio = Ratio.RATIO_4X3
        elif ratio.value == "16x9": ratio = Ratio.RATIO_16X9
        elif ratio.value == "1x1": ratio = Ratio.RATIO_1X1
        elif ratio.value == "3x2": ratio = Ratio.RATIO_3X2
        elif ratio.value == "4x3": ratio = Ratio.RATIO_4X3
        elif ratio.value == "9x16": ratio = Ratio.RATIO_9X16
        if number_of_images == None: number_of_images = 1
        elif number_of_images > 4: return await interaction.followup.send("You can't generate more than 4 images at once.", ephemeral=True)

        images_list = []
        for an_image in range(number_of_images):
            img_data = await imagine.sdprem(
                prompt=prompt,
                style=style,
                ratio=ratio
            )

            if img_data is None:
                e = f"MidJourney error: while generating the image"
                global error, error_channel
                error = f"Midjourney: {e}"
                error_channel = self.bot.get_channel(int(os.getenv("ERROR_CHANNEL_ID")))
                embed = discord.Embed(title = "Error",
                                    description = f"Sorry, an unexpected error has occured, do you want to send the error message to the developer?",
                                    color = discord.Color.red())
                return await interaction.followup.send(embed = embed, view = errorButtons())
            img_data = await imagine.upscale(image=img_data)
            if img_data is None:
                e = f"MidJourney error: while upscaling the image"
                global error2, error_channel2
                error2 = f"Midjourney: {e}"
                error_channel2 = self.bot.get_channel(int(os.getenv("ERROR_CHANNEL_ID")))
                embed = discord.Embed(title = "Error",
                                    description = f"Sorry, an unexpected error has occured, do you want to send the error message to the developer?",
                                    color = discord.Color.red())
                return await interaction.followup.send(embed = embed, view = errorButtons())

            try:
                with io.BytesIO(img_data) as file:
                    file = discord.File(file, "image.png")
                    images_list.append(file)
            except Exception as e:
                global error3, error_channel3
                error3 = f"Midjourney: {e}"
                error_channel3 = self.bot.get_channel(int(os.getenv("ERROR_CHANNEL_ID")))
                embed = discord.Embed(title = "Error",
                                    description = f"Sorry, an unexpected error has occured, do you want to send the error message to the developer?",
                                    color = discord.Color.red())
                return await interaction.followup.send(embed = embed, view = errorButtons())
        await imagine.close()
        style_str = str(style).replace("Style.", "")
        await interaction.followup.send(f"- Prompt: `{prompt}`\n- Style: `{style_str}`", files=images_list)

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
            bot = await BingChatbot.create()
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
            session_cookie = os.getenv("BARD_COOKIE") # visit https://github.com/acheong08/Bard for guide on how to get
            bot = BardChatbot(session_cookie)
            response = bot.ask(prompt)
            response = str(response).split("{'content': ")[1].split(", 'conversation_id")[0].replace("\\n", "\n").replace("\\'", "'").replace('\\"', '"').replace("\\r", "\r")[1:-1]
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

    @app_commands.command(name = "chatbot", description = "Chat with powerful AI models.")
    @app_commands.describe(prompt = "The question you wanna ask.", model = "Choose the AI model you wanna chat with.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.choices(model = [
                                    app_commands.Choice(name = "gpt-4", value = "gpt-4"),
                                    app_commands.Choice(name = "gpt-3.5-turbo", value = "gpt-3.5-turbo"),
                                    app_commands.Choice(name = "alpaca-13b", value = "alpaca-13b"),
                                    app_commands.Choice(name = "vicuna-13b", value = "vicuna-13b"),
                                    app_commands.Choice(name = "koala-13b", value = "koala-13b"),
                                    app_commands.Choice(name = "llama-13b", value = "llama-13b"),
                                    app_commands.Choice(name = "oasst-pythia-12b", value = "oasst-pythia-12b"),
                                    app_commands.Choice(name = "fastchat-t5-3b", value = "fastchat-t5-3b")
                                    ])
    async def chatbot(self, interaction: discord.Interaction, prompt: str, model: app_commands.Choice[str]):
        await interaction.response.defer()
        try:
            if model.value == "gpt-4":
                chatbot = GPTChatbot(config={
                                    "email": os.getenv("CHATGPT_EMAIL"),
                                    "password": os.getenv("CHATGPT_PASS")
                                    })
                response = ""
                async for data in chatbot.ask(prompt, model=model.value):
                    response = data["message"]
                limit = 1800
                total_text = len(prompt) + len(response)
                if total_text > limit:
                    result = [response[i: i + limit] for i in range(0, len(response), limit)]
                    for half in result: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**{model.name}:** {half}")
                else: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**{model.name}:** {response}")
                return
            api_key = os.getenv("PAWAN_API_KEY")
            api_url = "https://api.pawan.krd/v1/chat/completions"
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
                    response = await response.json()
            response = response["choices"][0]["message"]["content"]
            limit = 1800
            total_text = len(prompt) + len(response)
            if total_text > limit:
                result = [response[i: i + limit] for i in range(0, len(response), limit)]
                for half in result: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**{model.name}:** {half}")
            else: await interaction.followup.send(f"**{interaction.user.display_name}:** {prompt}\n**{model.name}:** {response}")
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
