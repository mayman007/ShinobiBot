import discord
from discord import app_commands
from discord.ext import commands
from bardapi import BardAsync as BardChatbot # install the git version for all the features that i use
from EdgeGPT.EdgeGPT import Chatbot as BingChatbot, ConversationStyle
from EdgeGPT.ImageGen import ImageGenAsync
import json
import io
import os
import aiohttp
from imaginepy import AsyncImagine
from imaginepy.constants import *


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
        await interaction.response.send_message("Wanna generate images using powerful models? Use /imagine!", ephemeral = True)

    # Imagine
    @app_commands.command(name = "imagine", description = "Generate images using powerful Stable Diffusion models.")
    @app_commands.describe(prompt = "Describe the image.",
                           model = "Choose the model.",
                           style = "Choose the style.",
                           ratio = "Choose the ratio.",
                           negative = "What you DO NOT want to generate.",
                           cfg = "Creativity scale. Must be between 1 and 16. Default is 7.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.choices(model = [app_commands.Choice(name = "Imagine V4 Beta", value = "Model.V4_BETA"),
                                  app_commands.Choice(name = "Imagine V3", value = "Model.V3"),
                                  app_commands.Choice(name = "Imagine V1", value = "Model.V1"),
                                  app_commands.Choice(name = "Creative", value = "Model.CREATIVE"),
                                  app_commands.Choice(name = "Portrait", value = "Model.PORTRAIT"),
                                  app_commands.Choice(name = "Realistic", value = "Model.REALISTIC"),
                                  app_commands.Choice(name = "Anime", value = "Model.ANIME"),
                                  ])
    @app_commands.choices(style = [app_commands.Choice(name = "No Style", value = "Style.NO_STYLE"),
                                  app_commands.Choice(name = "Cosmic", value = "Style.COSMIC"),
                                  app_commands.Choice(name = "Chromatic", value = "Style.CHROMATIC"),
                                  app_commands.Choice(name = "Anime V2", value = "Style.ANIME_V2"),
                                  app_commands.Choice(name = "Candyland", value = "Style.CANDYLAND"),
                                  app_commands.Choice(name = "Cyberpunk", value = "Style.CYBERPUNK"),
                                  app_commands.Choice(name = "Vibrant", value = "Style.VIBRANT"),
                                  app_commands.Choice(name = "Cinematic Render", value = "Style.CINEMATIC_RENDER"),
                                  app_commands.Choice(name = "Surrealism", value = "Style.SURREALISM"),
                                  app_commands.Choice(name = "Logo", value = "Style.LOGO"),
                                  app_commands.Choice(name = "GTA", value = "Style.GTA"),
                                  app_commands.Choice(name = "Samurai", value = "Style.SAMURAI"),
                                  app_commands.Choice(name = "Disney", value = "Style.DISNEY"),
                                  app_commands.Choice(name = "Comic Book", value = "Style.COMIC_BOOK"),
                                  app_commands.Choice(name = "Comic V2", value = "Style.COMIC_V2"),
                                  app_commands.Choice(name = "Sketch", value = "Style.SKETCH"),
                                  app_commands.Choice(name = "Fantasy", value = "Style.FANTASY"),
                                  app_commands.Choice(name = "Futuristic", value = "Style.FUTURISTIC"),
                                  app_commands.Choice(name = "Icon", value = "Style.ICON"),
                                  app_commands.Choice(name = "Illustration", value = "Style.ILLUSTRATION"),
                                  app_commands.Choice(name = "Japanese Art", value = "Style.JAPANESE_ART"),
                                  app_commands.Choice(name = "Kawaii Chibi", value = "Style.KAWAII_CHIBI"),
                                  app_commands.Choice(name = "Picasso", value = "Style.PICASSO"),
                                  app_commands.Choice(name = "Pixel Art", value = "Style.PIXEL_ART"),
                                  app_commands.Choice(name = "Neon", value = "Style.NEON"),
                                  ])
    @app_commands.choices(ratio = [app_commands.Choice(name = "16x9", value = "Ratio.RATIO_16X9"),
                                  app_commands.Choice(name = "1x1", value = "Ratio.RATIO_1X1"),
                                  app_commands.Choice(name = "3x2", value = "Ratio.RATIO_3X2"),
                                  app_commands.Choice(name = "4x3", value = "Ratio.RATIO_4X3"),
                                  app_commands.Choice(name = "9x16", value = "Ratio.RATIO_9X16")
                                  ])
    async def imagine(self,
                      interaction: discord.Interaction,
                      prompt: str,
                      model: app_commands.Choice[str],
                      style: app_commands.Choice[str],
                      ratio: app_commands.Choice[str],
                      negative: str = None,
                      cfg: float = None):

        if cfg == None: cfg = 7
        elif not cfg in range(1, 17): return await interaction.response.send_message("cfg must be between 1 and 16.", ephemeral=True)

        if model.value == "Model.V4_BETA": model.value = Model.V4_BETA
        elif model.value == "Model.V3": model.value = Model.V3
        elif model.value == "Model.V1": model.value = Model.V1
        elif model.value == "Model.CREATIVE": model.value = Model.CREATIVE
        elif model.value == "Model.PORTRAIT": model.value = Model.PORTRAIT
        elif model.value == "Model.REALISTIC": model.value = Model.REALISTIC
        elif model.value == "Model.ANIME": model.value = Model.ANIME

        if style.value == "Style.NO_STYLE": style.value = Style.NO_STYLE
        elif style.value == "Style.COSMIC": style.value = Style.COSMIC
        elif style.value == "Style.CHROMATIC": style.value = Style.CHROMATIC
        elif style.value == "Style.ANIME_V2": style.value = Style.ANIME_V2
        elif style.value == "Style.CANDYLAND": style.value = Style.CANDYLAND
        elif style.value == "Style.CYBERPUNK": style.value = Style.CYBERPUNK
        elif style.value == "Style.VIBRANT": style.value = Style.VIBRANT
        elif style.value == "Style.CINEMATIC_RENDER": style.value = Style.CINEMATIC_RENDER
        elif style.value == "Style.SURREALISM": style.value = Style.SURREALISM
        elif style.value == "Style.LOGO": style.value = Style.LOGO
        elif style.value == "Style.GTA": style.value = Style.GTA
        elif style.value == "Style.SAMURAI": style.value = Style.SAMURAI
        elif style.value == "Style.DISNEY": style.value = Style.DISNEY
        elif style.value == "Style.COMIC_BOOK": style.value = Style.COMIC_BOOK
        elif style.value == "Style.COMIC_V2": style.value = Style.COMIC_V2
        elif style.value == "Style.SKETCH": style.value = Style.SKETCH
        elif style.value == "Style.FANTASY": style.value = Style.FANTASY
        elif style.value == "Style.FUTURISTIC": style.value = Style.FUTURISTIC
        elif style.value == "Style.ICON": style.value = Style.ICON
        elif style.value == "Style.ILLUSTRATION": style.value = Style.ILLUSTRATION
        elif style.value == "Style.JAPANESE_ART": style.value = Style.JAPANESE_ART
        elif style.value == "Style.KAWAII_CHIBI": style.value = Style.KAWAII_CHIBI
        elif style.value == "Style.PICASSO": style.value = Style.PICASSO
        elif style.value == "Style.PIXEL_ART": style.value = Style.PIXEL_ART
        elif style.value == "Style.NEON": style.value = Style.NEON

        if ratio.value == "Ratio.RATIO_16X9": ratio.value = Ratio.RATIO_16X9
        elif ratio.value == "Ratio.RATIO_1X1": ratio.value = Ratio.RATIO_1X1
        elif ratio.value == "Ratio.RATIO_3X2": ratio.value = Ratio.RATIO_3X2
        elif ratio.value == "Ratio.RATIO_4X3": ratio.value = Ratio.RATIO_4X3
        elif ratio.value == "Ratio.RATIO_9X16": ratio.value = Ratio.RATIO_9X16

        if negative == None: negative = ""

        await interaction.response.defer()
        imagine = AsyncImagine()
        img_data = await imagine.sdprem(
            prompt=prompt,
            model=model.value,
            style=style.value,
            ratio=ratio.value,
            negative=negative,
            # seed=4294967295,
            cfg=cfg,
            high_result=True
        )

        if img_data is None:
            e = f"MidJourney error: while generating the image"
            global error, error_channel
            error = f"Midjourney: {e}"
            error_channel = self.bot.get_channel(int(os.getenv("ERROR_CHANNEL_ID")))
            embed = discord.Embed(title = "Error",
                                description = f"Sorry, an unexpected error has occured, do you want to send the error message to the developer?",
                                color = discord.Color.red())
            await interaction.followup.send(embed = embed, view = errorButtons())
            return await imagine.close()
        img_data = await imagine.upscale(img_data)
        if img_data is None:
            e = f"MidJourney error: while upscaling the image"
            global error2, error_channel2
            error2 = f"Midjourney: {e}"
            error_channel2 = self.bot.get_channel(int(os.getenv("ERROR_CHANNEL_ID")))
            embed = discord.Embed(title = "Error",
                                description = f"Sorry, an unexpected error has occured, do you want to send the error message to the developer?",
                                color = discord.Color.red())
            await interaction.followup.send(embed = embed, view = errorButtons())
            return await imagine.close()

        try:
            with io.BytesIO(img_data) as file:
                file = discord.File(file, "image.png")
        except Exception as e:
            global error3, error_channel3
            error3 = f"Midjourney: {e}"
            error_channel3 = self.bot.get_channel(int(os.getenv("ERROR_CHANNEL_ID")))
            embed = discord.Embed(title = "Error",
                                description = f"Sorry, an unexpected error has occured, do you want to send the error message to the developer?",
                                color = discord.Color.red())
            await interaction.followup.send(embed = embed, view = errorButtons())
            return await imagine.close()
        await imagine.close()
        info = ""
        info = info + f"- Prompt: `{prompt}`"
        info = info + f"\n- Model: `{model.name}`"
        info = info + f" \n- Style: `{style.name}`"
        info = info + f"\n- Ratio: `{ratio.name}`"
        if negative != "": info = info + f"\n- Negative: `{negative}`"
        info = info + f"\n- CFG: `{cfg}`"
        await interaction.followup.send(info, file=file)

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
            session_cookie = os.getenv("BARD_COOKIE")
            bot = BardChatbot(token=session_cookie)
            response = await bot.get_answer(prompt)
            response = response['content']
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
