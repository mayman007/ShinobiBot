import aiohttp
import aiosqlite
import discord
from discord import app_commands
from discord.ext import commands

# ui class for Character button
class characterButtons(discord.ui.View):
    def __init__(self, *, timeout = 600):
        super().__init__(timeout = timeout)

# Character Class
class Character(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Character is online.")

    # Character Search
    @app_commands.command(name = "character", description = "Search Anime & Manga characters from MAL")
    @app_commands.describe(name = "The name of the Character you're looking for")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def character(self, interaction: discord.Interaction, name: str):
        await interaction.response.send_message(f"Searching for \"{name}\"...")
        index = 0
        character_results_list = []
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.jikan.moe/v4/characters?q={name}&order_by=favorites&sort=desc") as response:
                results = await response.json()
        for result in results['data']:
            this_result_dict = {}
            url = result["url"]
            this_result_dict['url'] = url
            image_url = result["images"]["jpg"]["image_url"]
            this_result_dict['image_url'] = image_url
            name = result["name"]
            this_result_dict['name'] = name
            favorites = result["favorites"]
            this_result_dict['favorites'] = favorites
            about = result["about"]
            print(about)
            if len(str(about)) > 800: about = about[:800] + "..."
            this_result_dict['about'] = about
            character_results_list.append(this_result_dict)
            index += 1
            if index == 8: break
        if index == 0:
            return await interaction.followup.send("No results found.")
        else:
            print(f"character_results_list[0]['image_url'] {character_results_list[0]['image_url']}")
            embed = discord.Embed(title=character_results_list[0]['name'], description=character_results_list[0]['about'])
            embed.set_image(url = character_results_list[0]['image_url'])
            embed.set_footer(text = f"⭐ Favorites: {character_results_list[0]['favorites']}")
            view = characterButtons()
            view.add_item(discord.ui.Button(label = "MAL", style = discord.ButtonStyle.link, url = character_results_list[0]['url']))
            my_msg = await interaction.channel.send(embed=embed, view=view)

        async with aiosqlite.connect("db/anime.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS character (message_id TEXT, current_index INTEGER, character_result_list TEXT)")
                await cursor.execute("INSERT INTO character (message_id, current_index, character_result_list) VALUES (?, ?, ?)", (my_msg.id, 0, str(character_results_list)))
                await connection.commit()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Character(bot))