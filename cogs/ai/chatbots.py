import asyncio
import os
import discord
from discord import app_commands
from discord.ext import commands
import google.generativeai as genai
from re_edge_gpt import Chatbot, ConversationStyle
from pathlib import Path
import json


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
    async def gemini(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = await model.generate_content_async(prompt)
        response = f"**{interaction.user.display_name}:** {prompt}\n**Gemini Pro:** {response.text}"
        limit = 1800
        if len(response) > limit:
            result = [response[i: i + limit] for i in range(0, len(response), limit)]
            for half in result:
                await interaction.followup.send(half)
                await asyncio.sleep(0.5)
        else: await interaction.followup.send(response)

    # Bing
    @app_commands.command(name = "bing", description = "Chat with Bing GPT-4 AI")
    @app_commands.describe(prompt = "The question you wanna ask", conversation_style = "Default is Balanced")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    @app_commands.choices(conversation_style = [
        app_commands.Choice(name = "creative", value = "creative"),
        app_commands.Choice(name = "balanced", value = "balanced"),
        app_commands.Choice(name = "precise", value = "precise")
        ])
    async def bing(self, interaction: discord.Interaction, prompt: str, conversation_style: app_commands.Choice[str] = None):
        await interaction.response.defer()
        # Setting convo style
        if conversation_style == None:
            convo_style = ConversationStyle.balanced
            string_style = " Balanced"
        elif conversation_style.value == "creative":
            convo_style = ConversationStyle.creative
            string_style = " Creative"
        elif conversation_style.value == "balanced":
            convo_style = ConversationStyle.balanced
            string_style = " Balanced"
        elif conversation_style.value == "precise":
            convo_style = ConversationStyle.precise
            string_style = " Precise"

        # Opening cookies and getting response
        with open(Path.cwd() / "bing_cookies.json", encoding="utf-8") as file: cookies = json.load(file)
        bot = await Chatbot.create(cookies=cookies)
        response = await bot.ask(
            prompt=prompt,
            conversation_style=convo_style,
            simplify_response=True
        )
        response_text = f"**{interaction.user.display_name}:** {prompt}\n**Bing{string_style}:** {response['text']}"

        # Getting web search results
        web_search_results_bool = False
        if '"web_search_results":' in response_text:
            try:
                web_search_results = json.loads(response_text.split('"web_search_results":')[1].split('"}]}')[0] + '"}]')
                web_search_results_text = ""
                for result in web_search_results:
                    web_search_results_text += f"\n**[{result['title']}]({result['url']})**\n"
                    for snippit in result["snippets"]:
                        if len(snippit) > 130: snippit = snippit[:127] + "..."
                        web_search_results_text += f"- {snippit}\n"
                web_search_results_bool = True
            except Exception as e:
                print(f"Bing web_search_results error: {e}")
            response_text = response_text.split("Generating answers for you... ")[0]

        # Getting sources
        if response["source_keys"] != []:
            index = 0
            sources_text = ""
            for source_key in response["source_keys"]:
                source_url = response['source_values'][index]
                index += 1
                if source_key == "": sources_text += f"\n- {source_url}"
                else: sources_text += f"\n- [{source_key}]({source_url})"

        # Formatting and sending
        limit = 1800
        if len(response_text) > limit: # If the message exceeds the limit
            result = [response_text[i: i + limit] for i in range(0, len(response_text), limit)]
            first_msg_sent = False
            for half in result:
                if first_msg_sent == False:
                    if response["source_keys"] != []: # If there are sources
                        embed = discord.Embed(title="Sources", description=sources_text)
                        await interaction.followup.send(half, embed=embed)
                        first_msg_sent = True
                    else:
                        await interaction.followup.send(half)
                else:
                    await interaction.followup.send(half)
                await asyncio.sleep(0.3)
        else: # If it's within the limit
            if response["source_keys"] != []: # If there are sources
                embed = discord.Embed(title="Sources", description=sources_text)
                await interaction.followup.send(response_text, embed=embed)
            else:
                await interaction.followup.send(response_text)

        if web_search_results_bool:
            embed = discord.Embed(title="Web Search Results", description=web_search_results_text)
            await interaction.followup.send(embed=embed)

        await bot.close()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Chatbots(bot))