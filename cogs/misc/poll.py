import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
import ast


# poll buttons
class pollButtons(discord.ui.View):
    def __init__(self, *, timeout = None):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Yes", style = discord.ButtonStyle.blurple, emoji = "<:pepeyes:1070834912782987424>", custom_id = "poll_yes_button")
    async def poll_yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Fetching poll data...
        async with aiosqlite.connect("db/polls.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM polls WHERE poll_id = ?", (interaction.message.id,))
                data = await cursor.fetchone()
                poll_title = data[1]
                poll_description = data[2]
                poll_author = data[3]
                poll_avatar = data[4]
                upvotes = data[5]
                downvotes = data[6]
                upvote_users = ast.literal_eval(data[7])
                downvote_users = ast.literal_eval(data[8])

                if interaction.user.id in upvote_users:
                    upvotes = upvotes - 1
                    upvote_users.remove(interaction.user.id)
                    await cursor.execute("UPDATE polls SET upvotes = ?, upvote_users = ? WHERE poll_id = ?", (upvotes, str(upvote_users), interaction.message.id,))
                    await interaction.response.send_message("Vote removed.", ephemeral = True)
                elif interaction.user.id in downvote_users:
                    downvotes = downvotes - 1
                    downvote_users.remove(interaction.user.id)
                    upvotes = upvotes + 1
                    upvote_users.append(interaction.user.id)
                    await cursor.execute("UPDATE polls SET upvotes = ?, upvote_users = ?, downvotes = ?, downvote_users = ? WHERE poll_id = ?", (upvotes, str(upvote_users), downvotes, str(downvote_users), interaction.message.id,))
                    await interaction.response.send_message("Voted.", ephemeral = True)
                else:
                    upvotes = upvotes + 1
                    upvote_users.append(interaction.user.id)
                    await cursor.execute("UPDATE polls SET upvotes = ?, upvote_users = ? WHERE poll_id = ?", (upvotes, str(upvote_users), interaction.message.id,))
                    await interaction.response.send_message("Voted.", ephemeral = True)
                await db.commit()
        emb = discord.Embed(title = poll_title, description = poll_description)
        if poll_avatar != "no avatar": emb.set_author(name = f"Poll by {poll_author}", icon_url = poll_avatar)
        else: emb.set_author(name = f"Poll by {poll_author}")
        emb.set_footer(text = f"{upvotes} Yes | {downvotes} No")
        view = pollButtons()
        await interaction.message.edit(embed = emb, view = view)
    #no button
    @discord.ui.button(label = "No", style = discord.ButtonStyle.blurple, emoji = "<:pepeno:1070834894537773087>", custom_id = "poll_no_button")
    async def sugg_downvote(self, interaction: discord.Interaction, button: discord.ui.Button):
         # Fetching poll data...
        async with aiosqlite.connect("db/polls.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM polls WHERE poll_id = ?", (interaction.message.id,))
                data = await cursor.fetchone()
                poll_title = data[1]
                poll_description = data[2]
                poll_author = data[3]
                poll_avatar = data[4]
                upvotes = data[5]
                downvotes = data[6]
                upvote_users = ast.literal_eval(data[7])
                downvote_users = ast.literal_eval(data[8])

                if interaction.user.id in downvote_users:
                    downvotes = downvotes - 1
                    downvote_users.remove(interaction.user.id)
                    await cursor.execute("UPDATE polls SET downvotes = ?, downvote_users = ? WHERE poll_id = ?", (downvotes, str(downvote_users), interaction.message.id,))
                    await interaction.response.send_message("Vote removed.", ephemeral = True)
                elif interaction.user.id in upvote_users:
                    upvotes = upvotes - 1
                    upvote_users.remove(interaction.user.id)
                    downvotes = downvotes + 1
                    downvote_users.append(interaction.user.id)
                    await cursor.execute("UPDATE polls SET downvotes = ?, downvote_users = ?, upvotes = ?, upvote_users = ? WHERE poll_id = ?", (downvotes, str(downvote_users), upvotes, str(upvote_users), interaction.message.id,))
                    await interaction.response.send_message("Voted.", ephemeral = True)
                else:
                    downvotes = downvotes + 1
                    downvote_users.append(interaction.user.id)
                    await cursor.execute("UPDATE polls SET downvotes = ?, downvote_users = ? WHERE poll_id = ?", (downvotes, str(downvote_users), interaction.message.id,))
                    await interaction.response.send_message("Voted.", ephemeral = True)
                await db.commit()
        emb = discord.Embed(title = poll_title, description = poll_description)
        emb.set_author(name = f"Poll by {poll_author}", icon_url = poll_avatar)
        emb.set_footer(text = f"{upvotes} Yes | {downvotes} No")
        view = pollButtons()
        await interaction.message.edit(embed = emb, view = view)

# Poll Class
class Poll(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Poll is online.")

    #poll command
    @app_commands.command(name = "poll", description = "Make a poll.")
    @app_commands.describe(title = "The title of the poll.", description = "The description of the poll.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(manage_messages = True)
    async def poll(self, interaction: discord.Interaction, title: str, description: str):
        try: user_avatar = interaction.user.avatar.url
        except: user_avatar = "no avatar"
        view = pollButtons()
        emb = discord.Embed(title = title, description = description)
        if user_avatar != "no avatar": emb.set_author(name = f"Poll by {interaction.user.display_name}", icon_url = interaction.user.avatar.url)
        else: emb.set_author(name = f"Poll by {interaction.user.display_name}")
        emb.set_footer(text = f"0 Yes | 0 No")
        await interaction.response.send_message("Poll Created!", ephemeral=True)
        poll_msg = await interaction.channel.send(embed = emb, view = view)
        async with aiosqlite.connect("db/polls.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS polls (poll_id INTEGER, poll_title TEXT, poll_description TEXT, poll_author TEXT, poll_avatar TEXT, upvotes INTEGER, downvotes INTEGER, upvote_users TEXT, downvote_users TEXT)")
                await cursor.execute("INSERT INTO polls (poll_id, poll_title, poll_description, poll_author, poll_avatar, upvotes, downvotes, upvote_users, downvote_users) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (poll_msg.id, title, description, interaction.user.display_name, user_avatar, 0, 0, "[]", "[]"))
                await db.commit()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Poll(bot))