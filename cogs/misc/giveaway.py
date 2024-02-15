import ast
import aiosqlite
import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random
from datetime import datetime


# giveaway button
class giveawayButton(discord.ui.View):
    def __init__(self, *, timeout = None):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Participate", style = discord.ButtonStyle.blurple, emoji = "🎉", custom_id="giveaway_button")
    async def giveaway_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with aiosqlite.connect("db/giveaways.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM giveaways WHERE give_id = ?", (interaction.message.id,))
                data = await cursor.fetchone()
                give_author = data[1]
                give_prize = data[2]
                give_timer = data[3]
                give_icon = data[4]
                give_clicked = ast.literal_eval(data[5])
                if interaction.user.mention in give_clicked:
                    give_clicked.remove(interaction.user.mention)
                    await interaction.response.send_message("You've left the giveaway.", ephemeral = True)
                else:
                    give_clicked.append(interaction.user.mention)
                    await interaction.response.send_message("You've Participated!", ephemeral = True)
                await cursor.execute("UPDATE giveaways SET give_clicked = ? WHERE give_id = ?", (str(give_clicked), interaction.message.id,))
                await db.commit()
        emb = discord.Embed(title = "__*🎉GIVEAWAY🎉*__",
                            description = f"Click 🎉 to enter!\nHosted by: {give_author}\nPrize: **{give_prize}**\nParticipators: **{len(give_clicked)}**\nEnds at: {give_timer}",
                            colour = 0xff0000)
        if give_icon != "no icon": emb.set_thumbnail(url = give_icon)
        view = giveawayButton()
        await interaction.message.edit(embed = emb, view = view)

# Giveaway Class
class Giveaway(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Giveaway is online.")

    #giveaway
    @app_commands.command(name = "giveaway", description = "Set a giveaway.")
    @app_commands.describe(time = "Giveaway's time.", prize = "Giveaway's prize.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def giveaway(self, interaction: discord.Interaction, time: str, prize: str):
        try: icon = str(interaction.guild.icon.url)
        except: icon = "no icon"
        if time:
            get_time = {
            "s": 1, "m": 60, "h": 3600, "d": 86400,
            "w": 604800, "mo": 2592000, "y": 31104000 }
            a = time[-1]
            b = get_time.get(a)
            c = time[:-1]
            try: int(c)
            except: return await interaction.response.send_message("> Type time and time unit [s,m,h,d,w,mo,y] correctly.", ephemeral = True)
            try: sleep = int(b) * int(c)
            except: return await interaction.response.send_message("> Type time and time unit [s,m,h,d,w,mo,y] correctly.", ephemeral = True)
        give_timer = f"<t:{int(datetime.timestamp(datetime.now())) + int(sleep)}:F>"
        emb = discord.Embed(title = "__*🎉GIVEAWAY🎉*__",
                            description = f"Click 🎉 to enter!\nHosted by: {interaction.user.mention}\nPrize: **{prize}**\nParticipators: **0**\nEnds at: {give_timer}",
                            colour = 0xff0000)
        if icon != "no icon": emb.set_thumbnail(url = icon)
        view = giveawayButton()
        await interaction.response.send_message("Giveaway Created!", ephemeral = True)
        msg = await interaction.channel.send(embed = emb, view = view)
        async with aiosqlite.connect("db/giveaways.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS giveaways (give_id INTEGER, give_author TEXT, give_prize TEXT, give_timer TEXT, give_icon TEXT, give_clicked TEXT)")
                await cursor.execute("INSERT INTO giveaways (give_id, give_author, give_prize, give_timer, give_icon, give_clicked) VALUES (?, ?, ?, ?, ?, ?)", (msg.id, interaction.user.mention, prize, give_timer, icon, "[]"))
                await db.commit()
        await asyncio.sleep(int(sleep))
        async with aiosqlite.connect("db/giveaways.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM giveaways WHERE give_id = ?", (msg.id,))
                data = await cursor.fetchone()
                give_clicked = ast.literal_eval(data[5])
        #Check if User list is not empty
        if len(give_clicked) <= 0:
            emptyEmbed = discord.Embed(title = "__*🎉GIVEAWAY🎉*__",
                                       description = f"No one participated in the giveaway\nHosted by: {interaction.user.mention}\nPrize: **{prize}**\nEnded at: {give_timer}")
            if icon != "no icon": emptyEmbed.set_thumbnail(url = icon)
            await msg.edit(embed = emptyEmbed, view = None)
        else:
            winner = random.choice(give_clicked)
            emb = discord.Embed(title = "__*🎉GIVEAWAY🎉*__",
                            description = f"Click 🎉 to enter!\nHosted by: {interaction.user.mention}\nPrize: **{prize}**\nParticipators: **{len(give_clicked)}**\nEnded at: {give_timer}",
                            colour = 0xff0000)
            if icon != "no icon": emb.set_thumbnail(url = icon)
            await msg.edit(content = f"__***🎉Giveway ended, {winner} won!🎉***__", view = None, embed = emb)
            await msg.reply(f"> **Congratulations {winner} On Winning {prize} 🎉🎉**")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Giveaway(bot))