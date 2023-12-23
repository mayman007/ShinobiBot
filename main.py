import discord
from discord import app_commands
import aiohttp
from discord.ext import commands
from cogs.ticket.ticket import ticket_launcher, main
from cogs.settings.suggestions import suggVotes
from cogs.misc.giveaway import giveawayButton
from cogs.misc.poll import pollButtons
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
        # Adding cogs
        cogs = []
        for root, dirs, files in os.walk("cogs"):
            if "__pycache__" in root:
                continue
            folder_name = os.path.basename(root)
            for file_name in files:
                if file_name.endswith(".py"):
                    if folder_name == "cogs":
                        cogs.append(f"cogs.{file_name[:-3]}")
                    else:
                        cogs.append(f"cogs.{folder_name}.{file_name[:-3]}")
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