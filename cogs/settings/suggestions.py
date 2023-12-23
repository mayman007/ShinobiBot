import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import aiosqlite


#suggest confirm button
class suggestConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def suggest_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("> This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/suggestions.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS channels (sugg_channel INTEGER, rev_channel INTEGER, guild ID)") # Create the table if not exists
                await cursor.execute("SELECT sugg_channel AND rev_channel FROM channels WHERE guild = ?", (interaction.guild.id,)) # Select channels from the same row that has guild.id
                data = await cursor.fetchone() # Fetch that row
                if data: # If the row has data (already has channels id)
                    await cursor.execute("UPDATE channels SET sugg_channel = ? WHERE guild = ?", (sugg_ch_id, interaction.guild.id,)) # Update it
                    await cursor.execute("UPDATE channels SET rev_channel = ? WHERE guild = ?", (rev_ch_id, interaction.guild.id,)) # Update it
                else: # If not
                    await cursor.execute("INSERT INTO channels (sugg_channel, rev_channel, guild) VALUES (?, ?, ?)", (sugg_ch_id, rev_ch_id, interaction.guild.id,)) # Insert it
                embed = discord.Embed(title = "⚙️ ┃ Suggestions System", description = "Your suggestions channels have been updated succesfully!", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def suggest_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user:
            return await interaction.response.send_message("> This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("> Process Canceled.")

# suggestions votes buttons
class suggVotes(discord.ui.View):
    def __init__(self, *, timeout = None):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Upvote", style = discord.ButtonStyle.blurple, emoji = "🔼", custom_id = "sugg_upvote_button")
    async def sugg_upvote(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with aiosqlite.connect("db/suggestions.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM suggestions WHERE sugg_id = ?", (interaction.message.id,))
                data = await cursor.fetchone()
                upvoted_users = []
                downvoted_users = []
                if data[1] != "[]":
                    upvoted_users = []
                    for user_id in data[1][1:-1].split(", "):
                        upvoted_users.append(int(user_id))
                if data[2] != "[]":
                    downvoted_users = []
                    for user_id in data[2][1:-1].split(", "):
                        downvoted_users.append(int(user_id))
                if interaction.user.id in upvoted_users:
                    upvoted_users.remove(interaction.user.id)
                    await interaction.response.send_message("Upvote removed.", ephemeral = True)
                elif interaction.user.id in downvoted_users:
                    downvoted_users.remove(interaction.user.id)
                    upvoted_users.append(interaction.user.id)
                    await interaction.response.send_message("Upvoted.", ephemeral = True)
                else:
                    upvoted_users.append(interaction.user.id)
                    await interaction.response.send_message("Upvoted.", ephemeral = True)
                await cursor.execute("UPDATE suggestions SET upvoted_users = ?, downvoted_users = ? WHERE sugg_id = ?", (str(upvoted_users), str(downvoted_users), interaction.message.id,))
                await db.commit()
        upvotes = len(upvoted_users)
        downvotes = len(downvoted_users)
        author = interaction.guild.get_member(data[4])
        suggestEmbed = discord.Embed(title = "Suggestion", description = data[3], color = 0xffd700)
        suggestEmbed.set_author(name = f"Suggested by {author}", icon_url = author.display_avatar.url)
        suggestEmbed.set_footer(text = f"{upvotes} Upvotes | {downvotes} Downvotes")
        view = suggVotes()
        await interaction.message.edit(embed = suggestEmbed, view = view)
    #cancel button
    @discord.ui.button(label = "Downvote", style = discord.ButtonStyle.blurple, emoji = "🔽", custom_id = "sugg_downvote_button")
    async def sugg_downvote(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with aiosqlite.connect("db/suggestions.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM suggestions WHERE sugg_id = ?", (interaction.message.id,))
                data = await cursor.fetchone()
                upvoted_users = []
                downvoted_users = []
                if data[1] != "[]":
                    upvoted_users = []
                    for user_id in data[1][1:-1].split(", "):
                        upvoted_users.append(int(user_id))
                if data[2] != "[]":
                    downvoted_users = []
                    for user_id in data[2][1:-1].split(", "):
                        downvoted_users.append(int(user_id))
                if interaction.user.id in downvoted_users:
                    downvoted_users.remove(interaction.user.id)
                    await interaction.response.send_message("Downvote removed.", ephemeral = True)
                elif interaction.user.id in upvoted_users:
                    upvoted_users.remove(interaction.user.id)
                    downvoted_users.append(interaction.user.id)
                    await interaction.response.send_message("Downvoted.", ephemeral = True)
                else:
                    downvoted_users.append(interaction.user.id)
                    await interaction.response.send_message("Downvoted.", ephemeral = True)
                await cursor.execute("UPDATE suggestions SET upvoted_users = ?, downvoted_users = ? WHERE sugg_id = ?", (str(upvoted_users), str(downvoted_users), interaction.message.id,))
                await db.commit()
        upvotes = len(upvoted_users)
        downvotes = len(downvoted_users)
        author = interaction.guild.get_member(data[4])
        suggestEmbed = discord.Embed(title = "Suggestion", description = data[3], color = 0xffd700)
        suggestEmbed.set_author(name = f"Suggested by {author}", icon_url = author.display_avatar.url)
        suggestEmbed.set_footer(text = f"{upvotes} Upvotes | {downvotes} Downvotes")
        view = suggVotes()
        await interaction.message.edit(embed = suggestEmbed, view = view)

# Suggestions Class
class Suggestions(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Suggestions is online.")

    #suggestions command
    @app_commands.command(name = "suggestions", description = "Set channels for suggestions.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(suggestions_channel = "Set a channel that members will sent their suggetions to.", switch = "Enable/Disable Suggetions System",
                           review_channel = "Set a private channel for admins to review the suggetions. (or make it the same suggestions channel if you want.)")
    @app_commands.choices(switch = [app_commands.Choice(name = "enable", value = "enable"), app_commands.Choice(name = "disable", value = "disable")])
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def suggestions(self, interaction: discord.Interaction, switch: app_commands.Choice[str], suggestions_channel: discord.TextChannel = None, review_channel: discord.TextChannel = None):
            if switch.value == "disable":
                async with aiosqlite.connect("db/suggestions.db") as db: # Open the db
                    async with db.cursor() as cursor:
                        await cursor.execute("CREATE TABLE IF NOT EXISTS channels (sugg_channel INTEGER, rev_channel INTEGER, guild ID)") # Create the table if not exists
                        await cursor.execute("SELECT sugg_channel AND rev_channel FROM channels WHERE guild = ?", (interaction.guild.id,)) # Select channels from the same row that has guild.id
                        data = await cursor.fetchone() # Fetch that row
                        if data: # If the row has data (already has channels id)
                            await cursor.execute("DELETE FROM channels WHERE guild = ?", (interaction.guild.id,)) # Delete it
                            await interaction.response.send_message("Suggestions System disabled successfully.")
                        else: # If not
                            await interaction.response.send_message(f"Suggestions System is already disabled in this server.", ephemeral = True)
                    await db.commit()
            elif switch.value == "enable":
                if suggestions_channel == None or review_channel == None:
                    return await interaction.response.send_message("You must include a suggestions channel and a review channel.", ephemeral = True)
                global sugg_ch_id
                global rev_ch_id
                sugg_ch_id = suggestions_channel.id
                rev_ch_id = review_channel.id
                view = suggestConfirm()
                em = discord.Embed(title = "Confirmation",
                description = f"Are you sure that you want {suggestions_channel.mention} to be your suggestions channel and {review_channel.mention} to be your suggestions' review channel?",
                color = 0x2F3136)
                await interaction.response.send_message(embed = em, view = view)

    # On message events
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot: return # If bot ignore it

        # Suggetions
        async with aiosqlite.connect("db/suggestions.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS channels (sugg_channel INTEGER, rev_channel INTEGER, guild ID)") # Create the table if not exists
                await cursor.execute("SELECT sugg_channel FROM channels WHERE guild = ?", (message.guild.id,))
                data1 = await cursor.fetchone()
                await cursor.execute("SELECT rev_channel FROM channels WHERE guild = ?", (message.guild.id,))
                data2 = await cursor.fetchone()
                if data1:
                    if message.channel.id == data1[0]:
                        rev_ch_id = data2[0]
                        await message.delete()
                        emb = discord.Embed(title = f"Thanks **{message.author}**", description = "Your suggetion was sent.", colour = discord.Colour.gold())
                        thx_msg = await message.channel.send(embed = emb)
                        await asyncio.sleep(3)
                        await thx_msg.delete()
                        channel = self.bot.get_channel(rev_ch_id)
                        suggestEmbed = discord.Embed(title = "Suggestion", description = message.content, color = 0xffd700)
                        suggestEmbed.set_author(name = f"Suggested by {message.author}", icon_url = message.author.display_avatar.url)
                        suggestEmbed.set_footer(text = f"0 Upvotes | 0 Downvotes")
                        view = suggVotes()
                        sugg_msg = await channel.send(embed = suggestEmbed, view = view)
                        await sugg_msg.create_thread(name = "Suggestion Discussion")
                        await cursor.execute("INSERT INTO suggestions (sugg_id, upvoted_users, downvoted_users, msg_content, msg_author_id) VALUES (?, ?, ?, ?, ?)", (sugg_msg.id, "[]", "[]", message.content, message.author.id))
                        await db.commit()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Suggestions(bot))