import ast
import io
import json
import aiohttp
import aiosqlite
import discord
from discord import app_commands
from discord.ext import commands

class animeButtons(discord.ui.View):
    def __init__(self, *, timeout = 600):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Previous", style = discord.ButtonStyle.blurple)
    async def previous_anime(self, interaction: discord.Interaction, button: discord.ui.Button):
        # if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/anime.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(f"SELECT * FROM anime WHERE message_id = {interaction.message.id}")
                db_data = await cursor.fetchall()
        current_index = db_data[0][1]
        anime_results_list = ast.literal_eval(db_data[0][2])
        if current_index == 0: return await interaction.response.defer()
        updated_index = current_index - 1

        self.clear_items()
        self = animeButtons()
        if updated_index == 0:
            self.children[0].disabled = True
        view = self

        embed = discord.Embed(title = anime_results_list[updated_index]['title'], description = f"""**👓 Type:** {anime_results_list[updated_index]['the_type']}
**⭐ Score:** {anime_results_list[updated_index]['score']}
**📃 Episodes:** {anime_results_list[updated_index]['episodes']}
**📅 Year:** {anime_results_list[updated_index]['year']}
**🎆 Themes: **{anime_results_list[updated_index]['themes']}
**🎞️ Genres:** {anime_results_list[updated_index]['genres']}
**🏢 Studio:** {anime_results_list[updated_index]['studios']}
**🧬 Source:** {anime_results_list[updated_index]['source']}""")
        embed.set_image(url = anime_results_list[updated_index]['image_url'])
        embed.set_footer(text = f"Result {updated_index + 1} of 8")
        view.add_item(discord.ui.Button(label = "MAL", style = discord.ButtonStyle.link, url = anime_results_list[updated_index]['url']))
        if anime_results_list[updated_index]['trailer'] != None: view.add_item(discord.ui.Button(label = "Trailer", style = discord.ButtonStyle.link, url = anime_results_list[updated_index]['trailer']))
        await interaction.message.edit(embed = embed, view=view)
        await interaction.response.defer()

        async with aiosqlite.connect("db/anime.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("UPDATE anime SET current_index = ? WHERE message_id = ?", (updated_index, interaction.message.id))
                await connection.commit()

    @discord.ui.button(label = "Next", style = discord.ButtonStyle.blurple)
    async def next_anime(self, interaction: discord.Interaction, button: discord.ui.Button):
        # if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/anime.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(f"SELECT * FROM anime WHERE message_id = {interaction.message.id}")
                db_data = await cursor.fetchall()
        current_index = db_data[0][1]
        anime_results_list = ast.literal_eval(db_data[0][2])
        updated_index = current_index + 1

        self.clear_items()
        self = animeButtons()
        if updated_index == 7:
            self.children[1].disabled = True
        view = self

        embed = discord.Embed(title = anime_results_list[updated_index]['title'], description = f"""**👓 Type:** {anime_results_list[updated_index]['the_type']}
**⭐ Score:** {anime_results_list[updated_index]['score']}
**📃 Episodes:** {anime_results_list[updated_index]['episodes']}
**📅 Year:** {anime_results_list[updated_index]['year']}
**🎆 Themes: **{anime_results_list[updated_index]['themes']}
**🎞️ Genres:** {anime_results_list[updated_index]['genres']}
**🏢 Studio:** {anime_results_list[updated_index]['studios']}
**🧬 Source:** {anime_results_list[updated_index]['source']}""")
        embed.set_image(url = anime_results_list[updated_index]['image_url'])
        embed.set_footer(text = f"Result {updated_index + 1} of 8")
        view.add_item(discord.ui.Button(label = "MAL", style = discord.ButtonStyle.link, url = anime_results_list[updated_index]['url']))
        if anime_results_list[updated_index]['trailer'] != None: view.add_item(discord.ui.Button(label = "Trailer", style = discord.ButtonStyle.link, url = anime_results_list[updated_index]['trailer']))
        await interaction.message.edit(embed = embed, view=view)
        await interaction.response.defer()

        async with aiosqlite.connect("db/anime.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("UPDATE anime SET current_index = ? WHERE message_id = ?", (updated_index, interaction.message.id))
                await connection.commit()


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

# ui class for Character button
class characterButtons(discord.ui.View):
    def __init__(self, *, timeout = 600):
        super().__init__(timeout = timeout)

# Anime Class
class Anime(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Anime is online.")

    # aghpb
    @app_commands.command(name = "aghpb", description = "Anime girls holding programming books")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def aghpb(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.devgoldy.xyz/aghpb/v1/random") as response:
                img = await response.read()
                with io.BytesIO(img) as file:
                    file = discord.File(file, "aghpb.png")
        await interaction.response.send_message(file=file)

    # Anime Search
    @app_commands.command(name = "anime", description = "Search Anime from MAL")
    @app_commands.describe(title = "The title of the Anime you're looking for")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def anime(self, interaction: discord.Interaction, title: str):
        await interaction.response.send_message(f"Searching for \"{title}\"...")
        index = 0
        anime_results_list = []
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.jikan.moe/v4/anime?q={title}&order_by=favorites&sort=desc") as response:
                results = await response.json()
        for result in results['data']:
            this_result_dict = {}
            url = result["url"]
            this_result_dict['url'] = url
            image_url = result["images"]["jpg"]["large_image_url"]
            this_result_dict['image_url'] = image_url
            trailer = result["trailer"]["url"]
            this_result_dict['trailer'] = trailer
            title = result["title"]
            this_result_dict['title'] = title
            source = result["source"]
            this_result_dict['source'] = source
            episodes = result["episodes"]
            this_result_dict['episodes'] = episodes
            the_type = result["type"]
            this_result_dict['the_type'] = the_type
            year = result["aired"]["prop"]["from"]["year"]
            this_result_dict['year'] = year
            score = result["score"]
            this_result_dict['score'] = score
            themes = []
            for theme in result["themes"]:
                themes.append(theme["name"])
            themes = str(themes).replace("[", "").replace("]", "").replace("'", "")
            this_result_dict['themes'] = themes
            studios = []
            for studio in result["studios"]:
                studios.append(studio["name"])
            studios = str(studios).replace("[", "").replace("]", "").replace("'", "")
            this_result_dict['studios'] = studios
            genres = []
            for studio in result["genres"]:
                genres.append(studio["name"])
            genres = str(genres).replace("[", "").replace("]", "").replace("'", "")
            this_result_dict['genres'] = genres
            anime_results_list.append(this_result_dict)
            index += 1
            if index == 8: break
        if index == 0:
            return await interaction.followup.send("No results found.")
        else:
            embed = discord.Embed(title=anime_results_list[0]['title'], description=f"""**👓 Type:** {anime_results_list[0]['the_type']}
**⭐ Score:** {anime_results_list[0]['score']}
**📃 Episodes:** {anime_results_list[0]['episodes']}
**📅 Year:** {anime_results_list[0]['year']}
**🎆 Themes: **{anime_results_list[0]['themes']}
**🎞️ Genres:** {anime_results_list[0]['genres']}
**🏢 Studio:** {anime_results_list[0]['studios']}
**🧬 Source:** {anime_results_list[0]['source']}""")
            embed.set_image(url = anime_results_list[0]['image_url'])
            embed.set_footer(text = f"Result 1 of 8")
            animeButtons().children[0].disabled = True
            view = animeButtons()
            view.add_item(discord.ui.Button(label = "MAL", style = discord.ButtonStyle.link, url = anime_results_list[0]['url']))
            if anime_results_list[0]['trailer'] != None: view.add_item(discord.ui.Button(label = "Trailer", style = discord.ButtonStyle.link, url = anime_results_list[0]['trailer']))
            my_msg = await interaction.channel.send(embed=embed, view=view)

        async with aiosqlite.connect("db/anime.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS anime (message_id TEXT, current_index INTEGER, anime_result_list TEXT)")
                await cursor.execute("INSERT INTO anime (message_id, current_index, anime_result_list) VALUES (?, ?, ?)", (my_msg.id, 0, str(anime_results_list)))
                await connection.commit()

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

    # Character Search
    @app_commands.command(name = "character", description = "Search characters from MAL")
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
            embed = discord.Embed(title=character_results_list[0]['name'], description=f"""**⭐ Favorites:** {character_results_list[0]['favorites']}
**👓 About:** {character_results_list[0]['about']}""")
            embed.set_image(url = character_results_list[0]['image_url'])
            embed.set_footer(text = f"Result 1 of 8")
            view = characterButtons()
            view.add_item(discord.ui.Button(label = "MAL", style = discord.ButtonStyle.link, url = character_results_list[0]['url']))
            my_msg = await interaction.channel.send(embed=embed, view=view)

        async with aiosqlite.connect("db/anime.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS character (message_id TEXT, current_index INTEGER, character_result_list TEXT)")
                await cursor.execute("INSERT INTO character (message_id, current_index, character_result_list) VALUES (?, ?, ?)", (my_msg.id, 0, str(character_results_list)))
                await connection.commit()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Anime(bot))