import discord
from discord import ui, app_commands, utils
import aiohttp
from discord.ext import commands
from cogs.ticket import ticket_launcher, main
from cogs.settings import suggVotes
from cogs.utility import pollButtons, giveawayButton
from datetime import datetime
import logging
import logging.handlers
import aiosqlite
import os
from dotenv import load_dotenv
load_dotenv()


#MyBot Class
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix = None, intents = intents, application_id = os.getenv("APP_ID"))
        files = [file_name for file_name in os.listdir("cogs") if file_name.endswith(".py")]
        cogs = []
        for file_name in files: cogs.append(f"cogs.{file_name[:-3]}")
        self.initial_extensions = cogs
        self.added = False
    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        for cogs in self.initial_extensions: await self.load_extension(cogs)
        await self.tree.sync() # Sync app commands
        print("Synced Successfully")
    async def close(self):
        await super().close()
        await self.session.close()
    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")
        if not self.added:
            self.add_view(ticket_launcher())
            self.add_view(main())
            self.add_view(suggVotes())
            self.add_view(pollButtons())
            self.add_view(giveawayButton())
            self.added = True
            await bot.change_presence(activity = discord.Game(name = "/help start")) # Setting `Playing` status
        if not os.path.exists("db"): os.makedirs("db") # Create db dir if not there
    async def on_message(self, message: discord.Message): pass

bot = MyBot()
bot.remove_command("help")

# Logging stuff
logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(
    filename = "discord.log",
    encoding = "utf-8",
    maxBytes = 32 * 1024 * 1024,  # 32 MiB
    backupCount = 5,  # Rotate through 5 files
    )
dt_fmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style = "{")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Errors handling
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        cool_error = discord.Embed(title = f"Slow it down bro!", description = f"Try again in {error.retry_after:.2f}s.", colour = discord.Colour.light_grey())
        await interaction.response.send_message(embed = cool_error, ephemeral = True)
    elif isinstance(error, app_commands.MissingPermissions):
        missing_perm = error.missing_permissions[0].replace("_", " ").title()
        per_error = discord.Embed(title = f"You're Missing Permissions!", description = f"You don't have {missing_perm} permission.", colour = discord.Colour.light_grey())
        await interaction.response.send_message(embed = per_error, ephemeral = True)
    elif isinstance(error, app_commands.BotMissingPermissions):
        missing_perm = error.missing_permissions[0].replace("_", " ").title()
        per_error = discord.Embed(title = f"I'm Missing Permissions!", description = f"I don't have {missing_perm} permission.", colour = discord.Colour.light_grey())
        await interaction.response.send_message(embed = per_error, ephemeral = True)
    else:
        error_channel = bot.get_channel(int(os.getenv("ERROR_CHANNEL_ID")))
        await error_channel.send(error)
        await interaction.response.send_message(f"Sorry, an error had occured.\nIf you are facing any issues with me you can always send your </feedback:1027218853127794780>.", ephemeral = True)
        raise error

# User info context menu
@bot.tree.context_menu(name = "User Info")
async def open_ticket_context_menu(interaction: discord.Interaction, member: discord.Member):
    if member is None: member = interaction.user
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(description = member.mention, color = 0x2F3136)
    embed.set_author(name = str(member), icon_url = member.avatar.url)
    embed.set_thumbnail(url = member.avatar.url)
    embed.add_field(name = "**Joined**", value = f"> {member.joined_at.strftime(date_format)}")
    members = sorted(interaction.guild.members, key = lambda m: m.joined_at)
    embed.add_field(name = "**Join position**", value = f"> {str(members.index(member)+1)}")
    embed.add_field(name = "**Registered**", value = f"> {member.created_at.strftime(date_format)}")
    if len(member.roles) > 1:
        role_string = ' '.join([r.mention for r in member.roles][1:])
        embed.add_field(name = "**Roles [{}]**".format(len(member.roles)-1), value = f"> {role_string}", inline = False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in member.guild_permissions if p[1]])
    embed.add_field(name = "**Guild permissions**", value = f"> {perm_string}", inline = False)
    embed.set_footer(text = 'ID: ' + str(member.id))
    await interaction.response.send_message(embed = embed)

# Ticket context menu
@bot.tree.context_menu(name = "Open a Ticket")
async def open_ticket_context_menu(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.top_role <= member.top_role and not interaction.user == interaction.guild.owner:
        return await interaction.response.send_message(f"Your role must be higher than {member.mention}!", ephemeral = True)
    ticket = utils.get(interaction.guild.text_channels, name = f"ticket-for-{member.name.lower().replace(' ', '-')}-{member.discriminator}")
    if ticket is not None: await interaction.response.send_message(f"{member.mention} already have a ticket open at {ticket.mention}!", ephemeral = True)
    else:
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
            member: discord.PermissionOverwrite(view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True),
            interaction.guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True)
        }
        async with aiosqlite.connect("db/tickets_role.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT role FROM roles WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: ticket_role = data[0]
                else: ticket_role = None
        if not ticket_role == None:
            ticket_role = interaction.guild.get_role(ticket_role)
            overwrites[ticket_role] = discord.PermissionOverwrite(view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True)
            ticket_sentence = f"{ticket_role.mention}, {interaction.user.mention} created a ticket for {member.mention}!"
        else:
            ticket_sentence = f"{interaction.user.mention} created a ticket for {member.mention}!"
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name = "tickets")
        if category is None: #If there's no category matching with the `name`
            category = await guild.create_category("tickets") #Creates the category
        try:
            channel = await interaction.guild.create_text_channel(name = f"ticket-for-{member.name}-{member.discriminator}", overwrites = overwrites, reason = f"Ticket for {member}", category = category)
        except: return await interaction.response.send_message("Ticket creation failed! Make sure I have `Manage Channels` permissions!", ephemeral = True)
        await channel.send(ticket_sentence, view = main())
        await interaction.response.send_message(f"I've opened a ticket for {member.mention} at {channel.mention}!", ephemeral = True)

# Feedback button
class feedbackButton(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 600, commands.BucketType.member)
    @discord.ui.button(label = "Send Feedback", style = discord.ButtonStyle.blurple)
    async def feedback_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author: return await interaction.response.send_message("> This is not for you!", ephemeral = True)
        retry = self.cooldown.get_bucket(interaction.message).update_rate_limit()
        if retry: return await interaction.response.send_message(f"Slow down! Try again in {round(retry, 1)} seconds!", ephemeral = True)
        await interaction.response.send_modal(feedbackModal())

# Feedback modal
class feedbackModal(ui.Modal, title = "Send Your Feedback"):
    ftitle = ui.TextInput(label = "Title", style = discord.TextStyle.short, placeholder = "Write a title for the issue/suggestion.", required = True, max_length = 50)
    fdes = ui.TextInput(label = "Long Description", style = discord.TextStyle.short, placeholder = "Descripe the issue/suggestion.", required = True, max_length = 1000)
    fsol = ui.TextInput(label = "Solution (optional)", style = discord.TextStyle.short, placeholder = "Write a solution for the issue.", required = False, max_length = 1000)
    async def on_submit(self, interaction: discord.Interaction):
        channel = bot.get_channel(int(os.getenv("FEEDBACK_CHANNEL_ID")))
        invite = await interaction.channel.create_invite(max_age = 300)
        try:
            embed = discord.Embed(title = f"User: {interaction.user}\nServer: {interaction.guild.name}\n{invite}", description = f"**{self.ftitle}**", timestamp = datetime.now())
            embed.add_field(name = "Description", value = self.fdes)
            embed.add_field(name = "Solution", value = self.fsol)
            try: embed.set_author(name = interaction.user, icon_url = interaction.user.avatar)
            except: embed.set_author(name = interaction.user)
            await channel.send(embed = embed)
            await interaction.response.send_message("Your feedback has been sent succesfully!", ephemeral = True)
        except:
            embed = discord.Embed(title = f"User: {interaction.user}\nServer: {interaction.guild.name}\n{invite}", description = f"**{self.ftitle}**", timestamp = datetime.now())
            embed.add_field(name = "Description", value = self.fdes)
            try: embed.set_author(name = interaction.user, icon_url = interaction.user.avatar)
            except: embed.set_author(name = interaction.user)
            await channel.send(embed = embed)
            await interaction.response.send_message("Your feedback has been sent succesfully!", ephemeral = True)

# Feedback command
@bot.tree.command(name = "feedback", description = "Send your feedback directly to the developers.")
async def feedback(interaction: discord.Interaction):
    global author
    author = interaction.user
    view = feedbackButton()
    embed = discord.Embed(title = "If you had faced any problems or have any suggestions, feel free to send your feedback!")
    await interaction.response.send_message(embed = embed, view = view, ephemeral = True)

# On leave
@bot.event
async def on_guild_remove(guild: discord.Guild):
    # Remove guild from databases
    async with aiosqlite.connect("db/tickets_role.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS roles (role INTEGER, guild ID)")
            await cursor.execute("SELECT role FROM roles WHERE guild = ?", (guild.id,))
            data = await cursor.fetchone()
            if data: await cursor.execute("DELETE FROM roles WHERE guild = ?", (guild.id,))
        await db.commit()
    async with aiosqlite.connect("db/suggestions.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS channels (sugg_channel INTEGER, rev_channel INTEGER, guild ID)")
            await cursor.execute("SELECT sugg_channel AND rev_channel FROM channels WHERE guild = ?", (guild.id,))
            data = await cursor.fetchone()
            if data: await cursor.execute("DELETE FROM channels WHERE guild = ?", (guild.id,))
        await db.commit()
    async with aiosqlite.connect("db/antispam.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS antispam (switch INTEGER, punishment STRING, whitelist STRING, guild ID)")
            await cursor.execute("SELECT switch FROM antispam WHERE guild = ?", (guild.id,))
            data = await cursor.fetchone()
            if data: await cursor.execute("DELETE FROM antispam WHERE guild = ?", (guild.id,))
        await db.commit()
    logs_files_list = ["joins", "leaves", "messages_edits", "messages_deletes", "role_create", "role_delete", "role_updates", "role_given", "role_remove",
                      "channel_create", "channel_delete", "channel_updates", "member_ban", "member_unban", "member_timeout" ,"nickname_change", "server_updates"]
    for log_file in logs_files_list:
        async with aiosqlite.connect(f"db/log_{log_file}.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("DELETE FROM log WHERE guild = ?", (guild.id,))
            await db.commit()

bot.run(os.getenv("BOT_TOKEN"))
