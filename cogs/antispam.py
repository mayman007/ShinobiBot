import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
from datetime import timedelta


# Antispam Class
class Antispam(commands.GroupCog, name = "antispam"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.anti_spam = commands.CooldownMapping.from_cooldown(5, 15, commands.BucketType.member) # Anti-Spam
        self.too_many_violations = commands.CooldownMapping.from_cooldown(4, 60, commands.BucketType.member) # Anti-Spam

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Anti-Spam is online.")

    # Anti-Spam enable command
    @app_commands.command(name = "enable", description = "Enables Anti-Spam System.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def enable(self, interaction: discord.Interaction):
        async with aiosqlite.connect("db/antispam.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS antispam (switch INTEGER, punishment STRING, whitelist STRING, guild ID)")
                await cursor.execute("SELECT switch FROM antispam WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data:
                    await interaction.response.send_message("Your antispam is already enabled.", ephemeral = True)
                else:
                    await cursor.execute("INSERT INTO antispam (switch, punishment, whitelist, guild) VALUES (?, ?, ?, ?)", (1, "none", "0", interaction.guild.id,))
                    embed = discord.Embed(title = "⛔ ┃ Anti-Spam Enable", description = "Anti-Spam is now enabled", color = 0x000000)
                    await interaction.response.send_message(embed = embed)
            await db.commit()

    # Anti-Spam disable command
    @app_commands.command(name = "disable", description = "Disables Anti-Spam System.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def disable(self, interaction: discord.Interaction):
        async with aiosqlite.connect("db/antispam.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS antispam (switch INTEGER, punishment STRING, whitelist STRING, guild ID)")
                await cursor.execute("SELECT switch FROM antispam WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data:
                    await cursor.execute("DELETE FROM antispam WHERE guild = ?", (interaction.guild.id,))
                    embed = discord.Embed(title = "⛔ ┃ Anti-Spam Disable", description = "Anti-Spam is now disabled", color = 0x000000)
                    await interaction.response.send_message(embed = embed)
                else:
                    await interaction.response.send_message("Anti-Spam is already disabled.", ephemeral = True)
            await db.commit()

    # Anti-Spam punishment command
    @app_commands.command(name = "punishment", description = "Sets a punishment for Anti-Spam System.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(punishment = "The punishment.")
    @app_commands.choices(punishment = [app_commands.Choice(name = "none", value = "none"),
                                        app_commands.Choice(name = "mute", value = "mute"),
                                        app_commands.Choice(name = "timeout", value = "timeout"),
                                        app_commands.Choice(name = "warn", value = "warn"),
                                        app_commands.Choice(name = "kick", value = "kick"),
                                        app_commands.Choice(name = "ban", value = "ban")
                                        ])
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def punishment(self, interaction: discord.Interaction, punishment: app_commands.Choice[str]):
        async with aiosqlite.connect("db/antispam.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS antispam (switch INTEGER, punishment STRING, whitelist STRING, guild ID)")
                await cursor.execute("SELECT switch FROM antispam WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE antispam SET punishment = ? WHERE guild = ?", (punishment.value, interaction.guild.id,))
                else: return await interaction.response.send_message("Anti-Spam System is not enabled in this server.", ephemeral = True)
                embed = discord.Embed(title = "⛔ ┃ Anti-Spam Punishment", description = f"Anti-Spam punishment has been updated to {punishment.value}", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()

    # Anti-Spam whitelist command
    @app_commands.command(name = "whitelist", description = "Whitelist a channel.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(channel = "The channel to whitelist.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def whitelist(self, interaction: discord.Interaction, channel: discord.TextChannel):
        async with aiosqlite.connect("db/antispam.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS antispam (switch INTEGER, punishment STRING, whitelist STRING, guild ID)")
                await cursor.execute("SELECT switch FROM antispam WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE antispam SET whitelist = ? WHERE guild = ?", (str(channel.id), interaction.guild.id,))
                else: return await interaction.response.send_message("Anti-Spam System is not enabled in this server.", ephemeral = True)
                embed = discord.Embed(title = "⛔ ┃ Anti-Spam Whitelist", description = f"{channel.mention} is now whitelisted", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()

    # On message events
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot: return # If bot ignore it

        # Anti-Spam Event
        async with aiosqlite.connect("db/antispam.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS antispam (switch INTEGER, punishment STRING, whitelist STRING, guild ID)")
                await cursor.execute("SELECT switch FROM antispam WHERE guild = ?", (message.guild.id,))
                data = await cursor.fetchone()
                if data: # If anti spam is enabled
                    await cursor.execute("SELECT whitelist FROM antispam WHERE guild = ?", (message.guild.id,))
                    data = await cursor.fetchone()
                    if message.channel.id != int(data[0]): # If the channel is not whitelisted
                        if type(message.channel) is not discord.TextChannel or message.author.bot: return
                        bucket = self.anti_spam.get_bucket(message)
                        retry_after = bucket.update_rate_limit()
                        if retry_after:
                            await message.delete()
                            await message.channel.send(f"{message.author.mention}, don't spam!", delete_after = 10)
                            violations = self.too_many_violations.get_bucket(message)
                            check = violations.update_rate_limit()
                            if check:
                                await cursor.execute("SELECT punishment FROM antispam WHERE guild = ?", (message.guild.id,))
                                data = await cursor.fetchone()
                                if data[0] != "none":
                                    if message.guild.me.top_role <= message.author.top_role:
                                        return await message.channel.send(f"> I cann't punish {message.author.mention}. Check my role.")
                                    if data[0] == "mute":
                                        mutedRole = discord.utils.get(message.guild.roles, name = "SB-Muted")
                                        if not mutedRole:
                                            mutedRole = await message.guild.create_role(name = "SB-Muted")
                                            for channel in message.guild.channels: await channel.set_permissions(mutedRole, send_messages = False)
                                        await message.author.add_roles(mutedRole)
                                        await message.author.send("You have been muted for spamming!")
                                    elif data[0] == "timeout":
                                        await message.author.timeout(timedelta(minutes = 10), reason = "Spamming")
                                        await message.author.send("You have been timed out for spamming!")
                                    elif data[0] == "warn":
                                        async with aiosqlite.connect("db/warnings.db") as db:
                                            async with db.cursor() as cursor:
                                                await cursor.execute("CREATE TABLE IF NOT EXISTS warnings (warns INTEGER, member INTEGER, guild ID)")
                                                await cursor.execute("SELECT warns FROM warnings WHERE member = ? AND guild = ?", (message.author.id, message.guild.id,))
                                                data = await cursor.fetchone()
                                                if data: await cursor.execute("UPDATE warnings SET warns = ? WHERE member = ? AND guild = ?", (data[0] + 1, message.author.id, message.guild.id,))
                                                else: await cursor.execute("INSERT INTO warnings (warns, member, guild) VALUES (?, ?, ?)", (1, message.author.id, message.guild.id,))
                                            await db.commit()
                                        await message.author.send("You have been warned for spamming!")
                                    elif data[0] == "kick":
                                        await message.author.kick(reason = "Spamming")
                                        await message.author.send(f"You have been kicked out from {message.guild.name} for spamming!")
                                    elif data[0] == "ban":
                                        await message.author.ban(reason = "Spamming")
                                        await message.author.send(f"You have been banned from {message.guild.name} for spamming!")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Antispam(bot))