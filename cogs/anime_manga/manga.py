import ast
import aiohttp
import aiosqlite
import discord
from discord import app_commands
from discord.ext import commands

class mangaButtons(discord.ui.View):
    def __init__(self, *, timeout = 600):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Previous", style = discord.ButtonStyle.blurple)
    async def previous_manga(self, interaction: discord.Interaction, button: discord.ui.Button):
        # if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/anime.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(f"SELECT * FROM manga WHERE message_id = {interaction.message.id}")
                db_data = await cursor.fetchall()
        current_index = db_data[0][1]
        manga_results_list = ast.literal_eval(db_data[0][2])
        if current_index == 0: return await interaction.response.defer()
        updated_index = current_index - 1

        self.clear_items()
        self = mangaButtons()
        if updated_index == 0:
            self.children[0].disabled = True
        view = self

        embed = discord.Embed(title = manga_results_list[updated_index]['title'], description = f"""**👓 Type:** {manga_results_list[updated_index]['the_type']}
**⭐ Score:** {manga_results_list[updated_index]['score']}
**📃 Chapters:** {manga_results_list[updated_index]['chapters']}
**📅 Year:** {manga_results_list[updated_index]['year']}
**🎆 Themes: **{manga_results_list[updated_index]['themes']}
**🎞️ Genres:** {manga_results_list[updated_index]['genres']}""")
        embed.set_image(url = manga_results_list[updated_index]['image_url'])
        embed.set_footer(text = f"Result {updated_index + 1} of 8")
        view.add_item(discord.ui.Button(label = "MAL", style = discord.ButtonStyle.link, url = manga_results_list[updated_index]['url']))
        await interaction.message.edit(embed = embed, view=view)
        await interaction.response.defer()

        async with aiosqlite.connect("db/anime.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("UPDATE manga SET current_index = ? WHERE message_id = ?", (updated_index, interaction.message.id))
                await connection.commit()

    @discord.ui.button(label = "Next", style = discord.ButtonStyle.blurple)
    async def next_manga(self, interaction: discord.Interaction, button: discord.ui.Button):
        # if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/anime.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(f"SELECT * FROM manga WHERE message_id = {interaction.message.id}")
                db_data = await cursor.fetchall()
        current_index = db_data[0][1]
        manga_results_list = ast.literal_eval(db_data[0][2])
        updated_index = current_index + 1

        self.clear_items()
        self = mangaButtons()
        if updated_index == 7:
            self.children[1].disabled = True
        view = self

        embed = discord.Embed(title = manga_results_list[updated_index]['title'], description = f"""**👓 Type:** {manga_results_list[updated_index]['the_type']}
**⭐ Score:** {manga_results_list[updated_index]['score']}
**📃 Chapters:** {manga_results_list[updated_index]['chapters']}
**📅 Year:** {manga_results_list[updated_index]['year']}
**🎆 Themes: **{manga_results_list[updated_index]['themes']}
**🎞️ Genres:** {manga_results_list[updated_index]['genres']}""")
        embed.set_image(url = manga_results_list[updated_index]['image_url'])
        embed.set_footer(text = f"Result {updated_index + 1} of 8")
        view.add_item(discord.ui.Button(label = "MAL", style = discord.ButtonStyle.link, url = manga_results_list[updated_index]['url']))
        await interaction.message.edit(embed = embed, view=view)
        await interaction.response.defer()

        async with aiosqlite.connect("db/anime.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("UPDATE manga SET current_index = ? WHERE message_id = ?", (updated_index, interaction.message.id))
                await connection.commit()

# Manga Class
class Manga(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Manga is online.")

    # Manga Search
    @app_commands.command(name = "manga", description = "Search manga from MAL")
    @app_commands.describe(title = "The title of the Manga you're looking for")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def manga(self, interaction: discord.Interaction, title: str):
        await interaction.response.send_message(f"Searching for \"{title}\"...")
        index = 0
        manga_results_list = []
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.jikan.moe/v4/manga?q={title}&order_by=favorites&sort=desc") as response:
                results = await response.json()
        for result in results['data']:
            this_result_dict = {}
            url = result["url"]
            this_result_dict['url'] = url
            image_url = result["images"]["jpg"]["large_image_url"]
            this_result_dict['image_url'] = image_url
            title = result["title"]
            this_result_dict['title'] = title
            chapters = result["chapters"]
            this_result_dict['chapters'] = chapters
            the_type = result["type"]
            this_result_dict['the_type'] = the_type
            year = result["published"]["prop"]["from"]["year"]
            this_result_dict['year'] = year
            score = result["score"]
            this_result_dict['score'] = score
            themes = []
            for theme in result["themes"]:
                themes.append(theme["name"])
            themes = str(themes).replace("[", "").replace("]", "").replace("'", "")
            this_result_dict['themes'] = themes
            genres = []
            for studio in result["genres"]:
                genres.append(studio["name"])
            genres = str(genres).replace("[", "").replace("]", "").replace("'", "")
            this_result_dict['genres'] = genres
            manga_results_list.append(this_result_dict)
            index += 1
            if index == 8: break
        if index == 0:
            return await interaction.followup.send("No results found.")
        else:
            embed = discord.Embed(title=manga_results_list[0]['title'], description=f"""**👓 Type:** {manga_results_list[0]['the_type']}
**⭐ Score:** {manga_results_list[0]['score']}
**📃 Chapters:** {manga_results_list[0]['chapters']}
**📅 Year:** {manga_results_list[0]['year']}
**🎆 Themes: **{manga_results_list[0]['themes']}
**🎞️ Genres:** {manga_results_list[0]['genres']}""")
            embed.set_image(url = manga_results_list[0]['image_url'])
            embed.set_footer(text = f"Result 1 of 8")
            mangaButtons().children[0].disabled = True
            view = mangaButtons()
            view.add_item(discord.ui.Button(label = "MAL", style = discord.ButtonStyle.link, url = manga_results_list[0]['url']))
            my_msg = await interaction.channel.send(embed=embed, view=view)

        async with aiosqlite.connect("db/anime.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS manga (message_id TEXT, current_index INTEGER, manga_result_list TEXT)")
                await cursor.execute("INSERT INTO manga (message_id, current_index, manga_result_list) VALUES (?, ?, ?)", (my_msg.id, 0, str(manga_results_list)))
                await connection.commit()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Manga(bot))