import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import aiosqlite


#hide all confirm
class hideallConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def hideall_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author: return await interaction.response.send_message("> This is not for you!", ephemeral = True)
        await interaction.response.defer()
        for channel in interaction.guild.channels:
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.read_messages = False
            await channel.set_permissions(interaction.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f":closed_lock_with_key: ┃ All Channels Hid! ┃ :closed_lock_with_key:", description = f"> {interaction.user.mention} had hid all channels in the server.")
        await interaction.followup.send(embed = emb)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def hideall_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author:
            return await interaction.response.send_message("> This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("> Process Canceled.")

#show all confirm
class showallConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def showall_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author: return await interaction.response.send_message("> This is not for you!", ephemeral = True)
        await interaction.response.defer()
        for channel in interaction.guild.channels:
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.read_messages = True
            await channel.set_permissions(interaction.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f"👁️ ┃ Channels Showed! ┃ 👁️", description = f"> {interaction.user.mention} had unhid all channels in the server.")
        await interaction.followup.send(embed = emb)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def showall_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author:
            return await interaction.response.send_message("> This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("> Process Canceled.")

#lock all confirm
class lockallConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def lockall_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author: return await interaction.response.send_message("> This is not for you!", ephemeral = True)
        await interaction.response.defer()
        for channel in interaction.guild.channels:
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.send_messages = False
            await channel.set_permissions(interaction.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f"🔒 ┃ All Channels Locked! ┃ 🔒", description = f"{interaction.user.mention} had locked all channels in the server.")
        await interaction.followup.send(embed = emb)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def lockall_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author:
            return await interaction.response.send_message("> This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("> Process Canceled.")

#unlock all confirm
class unlockallConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def unlockall_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author: return await interaction.response.send_message("> This is not for you!", ephemeral = True)
        await interaction.response.defer()
        for channel in interaction.guild.channels:
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.send_messages = True
            await channel.set_permissions(interaction.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f"🔓 ┃ All Channels Unlocked! ┃ 🔓", description = f"{interaction.user.mention} had unlocked all channels in the server.")
        await interaction.followup.send(embed = emb)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def unlockall_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author:
            return await interaction.response.send_message("> This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("> Process Canceled.")

#suggest confirm button
class suggestConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def suggest_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != suggest_author: return await interaction.response.send_message("> This is not for you!", ephemeral = True)
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
        if interaction.user != suggest_author:
            return await interaction.response.send_message("> This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("> Process Canceled.")

# suggestions votes buttons
class suggVotes(discord.ui.View):
    def __init__(self, *, timeout = None):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Upvote", style = discord.ButtonStyle.blurple, emoji = "🔼")
    async def sugg_upvote(self, interaction: discord.Interaction, button: discord.ui.Button):
        global upvotes, downvotes, upvoted_users, downvoted_users
        if interaction.user in upvoted_users:
            upvotes = upvotes - 1
            upvoted_users.remove(interaction.user)
            await interaction.response.send_message("Upvote removed.", ephemeral = True)
        elif interaction.user in downvoted_users:
            downvotes = downvotes - 1
            downvoted_users.remove(interaction.user)
            upvotes = upvotes + 1
            upvoted_users.append(interaction.user)
            await interaction.response.send_message("Upvoted.", ephemeral = True)
        else:
            upvotes = upvotes + 1
            upvoted_users.append(interaction.user)
            await interaction.response.send_message("Upvoted.", ephemeral = True)
        suggestEmbed = discord.Embed(title = "Suggestion", description = suggestion, color = 0xffd700)
        suggestEmbed.set_author(name = f"Suggested by {sugg_author}", icon_url = sugg_avatar)
        suggestEmbed.set_footer(text = f"{upvotes} Upvotes | {downvotes} Downvotes")
        view = suggVotes()
        await interaction.message.edit(embed = suggestEmbed, view = view)
    #cancel button
    @discord.ui.button(label = "Downvote", style = discord.ButtonStyle.blurple, emoji = "🔽")
    async def sugg_downvote(self, interaction: discord.Interaction, button: discord.ui.Button):
        global upvotes, downvotes, downvoted_users, upvoted_users
        if interaction.user in downvoted_users:
            downvotes = downvotes - 1
            downvoted_users.remove(interaction.user)
            await interaction.response.send_message("Downvote removed.", ephemeral = True)
        elif interaction.user in upvoted_users:
            upvotes = upvotes - 1
            upvoted_users.remove(interaction.user)
            downvotes = downvotes + 1
            downvoted_users.append(interaction.user)
            await interaction.response.send_message("Downvoted.", ephemeral = True)
        else:
            downvotes = downvotes + 1
            downvoted_users.append(interaction.user)
            await interaction.response.send_message("Downvoted.", ephemeral = True)
        suggestEmbed = discord.Embed(title = "Suggestion", description = suggestion, color = 0xffd700)
        suggestEmbed.set_author(name = f"Suggested by {sugg_author}", icon_url = sugg_avatar)
        suggestEmbed.set_footer(text = f"{upvotes} Upvotes | {downvotes} Downvotes")
        view = suggVotes()
        await interaction.message.edit(embed = suggestEmbed, view = view)

# Settings Class
class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Channels Settings is online.")

    #private channel
    @app_commands.command(name = "prvchannel", description = "Makes a temprory private channel.")
    @app_commands.describe(time = "Time of the channel before it gets deleted.", channel_name = "Channel's name.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def prvchannel(self, interaction: discord.Interaction, time: str, channel_name: str):
        guild = interaction.guild
        category = discord.utils.get(interaction.guild.categories)
        overwrites = {
                        guild.default_role: discord.PermissionOverwrite(read_messages = False),
                        guild.me: discord.PermissionOverwrite(read_messages = True)
                    }
        if time:
            get_time = {
            "s": 1, "m": 60, "h": 3600, "d": 86400,
            "w": 604800, "mo": 2592000, "y": 31104000 }
            timer = time
            a = time[-1]
            b = get_time.get(a)
            c = time[:-1]
            try: int(c)
            except: return await interaction.response.send_message("> Type time and time unit [s,m,h,d,w,mo,y] correctly.", ephemeral = True)
            try: sleep = int(b) * int(c)
            except: return await interaction.response.send_message("> Type time and time unit [s,m,h,d,w,mo,y] correctly.", ephemeral = True)
        channel = await guild.create_text_channel(name = channel_name , overwrites = overwrites , category = category)
        emb = discord.Embed(title = "Channel Created! ✅",
                            description = f"> Private Channel **{channel_name}** has been created for **{timer}**",
                            color = 0x2F3136)
        await interaction.response.send_message(embed = emb)
        await asyncio.sleep(int(sleep))
        await channel.delete()
        emb = discord.Embed(title = "Channel Deleted!", description = f"> Private Channel **{channel_name}** has been deleted after **{timer}**", color = 0x2F3136)
        await interaction.response.send_message(embed = emb)

    #hide
    @app_commands.command(name = "hide", description = "Hide a channel.")
    @app_commands.describe(channel = "Channel to hide (default is current channel).")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def hidechat(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        channel = channel or interaction.channel
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        if overwrite.read_messages == False:
            await interaction.response.send_message("> The channel is already hidden!", ephemeral = True)
            return
        overwrite.read_messages = False
        await channel.set_permissions(interaction.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f":closed_lock_with_key: ┃ Channel Hid!", description = f"> **{channel.mention}** has been hidden.", color = 0x2F3136)
        await interaction.response.send_message(embed = emb)

    #hide all
    @app_commands.command(name = "hideall", description = "Hide all channels in the server.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def hideall(self, interaction: discord.Interaction):
        global author
        author = interaction.user
        hideall_em = discord.Embed(title = "Confirm", description = "Are you sure that you want to hide all your channels?")
        view = hideallConfirm()
        await interaction.response.send_message(embed = hideall_em, view = view)

    #show
    @app_commands.command(name = "show", description = "Show a hidden channel.")
    @app_commands.describe(channel = "Channel to unhide (default is current channel).")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def showchat(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        channel = channel or interaction.channel
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        if overwrite.read_messages == True:
            return await interaction.response.send_message("> The channel is already shown!", ephemeral = True)
        overwrite.read_messages = True
        await channel.set_permissions(interaction.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f"👁️ ┃ Channel Showed!", description = f"> **{channel.mention}** has been shown.", color = 0x2F3136)
        await interaction.response.send_message(embed = emb)

    #show all
    @app_commands.command(name = "showall", description = "Unhide all channels in the server.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def showall(self, interaction: discord.Interaction):
        global author
        author = interaction.user
        hideall_em = discord.Embed(title = "Confirm", description = "Are you sure that you want to unhide all your channels?")
        view = showallConfirm()
        await interaction.response.send_message(embed = hideall_em, view = view)

    #lock
    @app_commands.command(name = "lock", description = "Lockes a channel.")
    @app_commands.describe(channel = "Channel to lock (default is current channel).")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def lock(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        channel = channel or interaction.channel
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        if overwrite.send_messages == False:
            return await interaction.response.send_message("> The channel is already locked", ephemeral = True)
        overwrite.send_messages = False
        await channel.set_permissions(interaction.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f"🔒 ┃ Channel Locked!", description = f"> **{channel.mention}** has been locked.", color = 0x2F3136)
        await interaction.response.send_message(embed = emb)

    #lock all
    @app_commands.command(name = "lockall", description = "Lockes all the channels.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def lockall(self, interaction: discord.Interaction):
        global author
        author = interaction.user
        lockall_em = discord.Embed(title = "Confirm", description = "Are you sure that you want to lock all your channels?")
        view = lockallConfirm()
        await interaction.response.send_message(embed = lockall_em, view = view)

    #unlock
    @app_commands.command(name = "unlock", description = "Unlocks a locked channel.")
    @app_commands.describe(channel = "Channel to unlock (default is current channel).")
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def unlock(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        channel = channel or interaction.channel
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        if overwrite.send_messages == True:
            return await interaction.response.send_message("> The channel is already unlocked", ephemeral = True)
        overwrite.send_messages = True
        await channel.set_permissions(interaction.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f"🔓 ┃ Channel Unlocked!", description = f"> **{channel.mention}** has been unlocked.", color = 0x2F3136)
        await interaction.response.send_message(embed = emb)

    #unlock all
    @app_commands.command(name = "unlockall", description = "unlockes all the channels.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def unlockall(self, interaction: discord.Interaction):
        global author
        author = interaction.user
        unlockall_em = discord.Embed(title = "Confirm", description = "Are you sure that you want to unlock all your channels?")
        view = unlockallConfirm()
        await interaction.response.send_message(embed = unlockall_em, view = view)

    #suggestions command
    @app_commands.command(name = "suggestions", description = "Set channels for suggestions.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(suggestions_channel = "Set a channel that members will sent their suggetions to.", switch = "Enable/Disable Suggetions System",
                           review_channel = "Set a private channel for admins to review the suggetions. (or make it the same suggestions channel if you want.)")
    @app_commands.choices(switch = [app_commands.Choice(name = "enable", value = "enable"), app_commands.Choice(name = "disable", value = "disable")])
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
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
                global suggest_author
                global sugg_ch_id
                global rev_ch_id
                suggest_author = interaction.user
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
                        msg = await message.channel.send(embed = emb)
                        await asyncio.sleep(3)
                        await msg.delete()
                        channel = self.bot.get_channel(rev_ch_id)
                        global suggestion, sugg_author, sugg_avatar, upvotes, downvotes, upvoted_users, downvoted_users
                        upvoted_users = []
                        downvoted_users = []
                        upvotes = 0
                        downvotes = 0
                        suggestion = message.content
                        sugg_author = message.author
                        sugg_avatar = message.author.avatar.url
                        suggestEmbed = discord.Embed(title = "Suggestion", description = suggestion, color = 0xffd700)
                        suggestEmbed.set_author(name = f"Suggested by {sugg_author}", icon_url = sugg_avatar)
                        suggestEmbed.set_footer(text = f"{upvotes} Upvotes | {downvotes} Downvotes")
                        view = suggVotes()
                        msg = await channel.send(embed = suggestEmbed, view = view)
                        await msg.create_thread(name = "Suggestion Discussion")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Settings(bot))
