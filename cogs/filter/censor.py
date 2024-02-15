import ast
import aiosqlite
import discord
from discord import app_commands
from discord.ext import commands


# Filter Class
class Censor(commands.GroupCog, name = "censor"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #waking
    @commands.Cog.listener()
    async def on_ready(self):
        print("Censor is online.")

    # Censor enable
    @app_commands.command(name = "enable", description = "Enable the Censor System")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def censor_enable(self, interaction: discord.Interaction):
        async with aiosqlite.connect("db/censor.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS censor (guild ID, switch INTEGER, words TEXT, punishment TEXT, whitelist INTEGER, censor_links TEXT, censor_invites TEXT)")
                await cursor.execute("SELECT switch FROM censor WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data:
                    await interaction.response.send_message("Your censor system is already enabled.", ephemeral = True)
                else:
                    await cursor.execute("INSERT INTO censor (guild, switch, words, punishment, whitelist, censor_links, censor_invites) VALUES (?, ?, ?, ?, ?, ?, ?)", (interaction.guild.id, 1, "[]", "none", "0", "disabled", "disabled",))
                    embed = discord.Embed(title = "⛔ ┃ Censor System Enable", description = "Censor System is now enabled", color = 0x000000)
                    await interaction.response.send_message(embed = embed)
            await db.commit()

    # Censor disable
    @app_commands.command(name = "disable", description = "Disable the Censor System")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def censor_disable(self, interaction: discord.Interaction):
        async with aiosqlite.connect("db/censor.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS censor (guild ID, switch INTEGER, words TEXT, punishment TEXT, whitelist INTEGER, censor_links TEXT, censor_invites TEXT)")
                await cursor.execute("SELECT switch FROM censor WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data:
                    await cursor.execute("DELETE FROM censor WHERE guild = ?", (interaction.guild.id,))
                    embed = discord.Embed(title = "⛔ ┃ Censor System Disable", description = "Censor System is now disabled", color = 0x000000)
                    await interaction.response.send_message(embed = embed)
                else:
                    await interaction.response.send_message("Censor System is already disabled.", ephemeral = True)
            await db.commit()

    # Censor words
    @app_commands.command(name = "words", description = "Add or remove words from the Censor System")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(option = "Select option", words = "Use a comma ',' to seperate each things")
    @app_commands.choices(option = [app_commands.Choice(name = "add", value = "add"),
                                    app_commands.Choice(name = "remove", value = "remove")
                                    ])
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def censor_words(self, interaction: discord.Interaction, option: app_commands.Choice[str], words: str):
        async with aiosqlite.connect("db/censor.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS censor (guild ID, switch INTEGER, words TEXT, punishment TEXT, whitelist INTEGER, censor_links TEXT, censor_invites TEXT)")
                await cursor.execute("SELECT * FROM censor WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: # If system is enabled
                    existing_words = ast.literal_eval(data[2])
                    if option.value == "add": # If user is adding words
                        already_added_words = []
                        new_words = []
                        added_words = words.split(",")
                        for word in added_words:
                            word = word.strip()
                            if word in existing_words: # If word is already added
                                already_added_words.append(word)
                            else: # If word is not added yet
                                new_words.append(word)
                                existing_words.append(word)
                        # Add data to db and send to user
                        await cursor.execute("UPDATE censor SET words = ? WHERE guild = ?", (str(existing_words), interaction.guild.id,))
                        embed = discord.Embed(title = "⛔ ┃ Censor System Words", description = f"`{', '.join(new_words)}` had been added to the system", color = 0x000000)
                        if already_added_words != []: embed.set_footer(text=f"Note: {', '.join(already_added_words)} had already been added before. Check /censor display to view all the settings")
                        await interaction.response.send_message(embed = embed)
                    if option.value == "remove": # If user is removing words
                        already_removed_words = []
                        to_remove_words = []
                        removed_words = words.split(",")
                        for word in removed_words:
                            word = word.strip()
                            if word in existing_words: # If word is realy added
                                to_remove_words.append(word)
                                existing_words.remove(word)
                            else: # If word is not added
                                already_removed_words.append(word)
                        # Add data to db and send to user
                        await cursor.execute("UPDATE censor SET words = ? WHERE guild = ?", (str(existing_words), interaction.guild.id,))
                        embed = discord.Embed(title = "⛔ ┃ Censor System Words", description = f"`{', '.join(to_remove_words)}` had been removed from the system", color = 0x000000)
                        if already_removed_words != []: embed.set_footer(text=f"Note: {', '.join(already_removed_words)} are not on the system. Check /censor display to view all the settings")
                        await interaction.response.send_message(embed = embed)
                else:
                    return await interaction.response.send_message("Censor System is not enabled in this server.\nEnable it from /censor enable", ephemeral = True)
            await db.commit()

    # Censor punishment
    @app_commands.command(name = "punishment", description = "Sets a punishment for the Censor System")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(punishment = "The punishment.")
    @app_commands.choices(punishment = [app_commands.Choice(name = "none", value = "none"),
                                        app_commands.Choice(name = "mute", value = "mute"),
                                        app_commands.Choice(name = "timeout", value = "timeout"),
                                        app_commands.Choice(name = "warn", value = "warn"),
                                        app_commands.Choice(name = "kick", value = "kick"),
                                        app_commands.Choice(name = "ban", value = "ban")
                                        ])
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def censor_punishment(self, interaction: discord.Interaction, punishment: app_commands.Choice[str]):
        async with aiosqlite.connect("db/censor.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS censor (guild ID, switch INTEGER, words TEXT, punishment TEXT, whitelist INTEGER, censor_links TEXT, censor_invites TEXT)")
                await cursor.execute("SELECT switch FROM censor WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE censor SET punishment = ? WHERE guild = ?", (punishment.value, interaction.guild.id,))
                else: return await interaction.response.send_message("Censor System is not enabled in this server.\nEnable it from /censor enable", ephemeral = True)
                embed = discord.Embed(title = "⛔ ┃ Censor System Punishment", description = f"Censor System punishment has been updated to `{punishment.value}`", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()

    # Censor whitelist
    @app_commands.command(name = "whitelist", description = "Whitelist channels from the Censor System")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(channel = "The channel to whitelist.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def censor_whitelist(self, interaction: discord.Interaction, channel: discord.TextChannel):
        async with aiosqlite.connect("db/censor.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS censor (guild ID, switch INTEGER, words TEXT, punishment TEXT, whitelist INTEGER, censor_links TEXT, censor_invites TEXT)")
                await cursor.execute("SELECT switch FROM censor WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE censor SET whitelist = ? WHERE guild = ?", (str(channel.id), interaction.guild.id,))
                else: return await interaction.response.send_message("Censor System is not enabled in this server.\nEnable it from /censor enable", ephemeral = True)
                embed = discord.Embed(title = "⛔ ┃ Censor System Whitelist", description = f"{channel.mention} is now whitelisted", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()

    # Censor links
    @app_commands.command(name = "links", description = "Enable/Disable censoring all links")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def censor_links(self, interaction: discord.Interaction):
        async with aiosqlite.connect("db/censor.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS censor (guild ID, switch INTEGER, words TEXT, punishment TEXT, whitelist INTEGER, censor_links TEXT, censor_invites TEXT)")
                await cursor.execute("SELECT * FROM censor WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data:
                    if data[5] == "enabled":
                        await cursor.execute("UPDATE censor SET censor_links = ? WHERE guild = ?", ("disabled", interaction.guild.id,))
                        embed = discord.Embed(title = "⛔ ┃ Censoring Links Disabled", description = f"Censoring all links is now disabled", color = 0x000000)
                        await interaction.response.send_message(embed = embed)
                    elif data[5] == "disabled":
                        await cursor.execute("UPDATE censor SET censor_links = ? WHERE guild = ?", ("enabled", interaction.guild.id,))
                        embed = discord.Embed(title = "⛔ ┃ Censoring Links Enabled", description = f"Censoring all links is now enabled", color = 0x000000)
                        await interaction.response.send_message(embed = embed)
                else: return await interaction.response.send_message("Censor System is not enabled in this server.\nEnable it from /censor enable", ephemeral = True)
            await db.commit()

    # Censor invites
    @app_commands.command(name = "invites", description = "Enable/Disable censoring all invites")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def censor_invites(self, interaction: discord.Interaction):
        async with aiosqlite.connect("db/censor.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS censor (guild ID, switch INTEGER, words TEXT, punishment TEXT, whitelist INTEGER, censor_links TEXT, censor_invites TEXT)")
                await cursor.execute("SELECT * FROM censor WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data:
                    if data[6] == "enabled":
                        await cursor.execute("UPDATE censor SET censor_invites = ? WHERE guild = ?", ("disabled", interaction.guild.id,))
                        embed = discord.Embed(title = "⛔ ┃ Censoring Invites Disabled", description = f"Censoring other server's invites is now disabled", color = 0x000000)
                        await interaction.response.send_message(embed = embed)
                    elif data[6] == "disabled":
                        await cursor.execute("UPDATE censor SET censor_invites = ? WHERE guild = ?", ("enabled", interaction.guild.id,))
                        embed = discord.Embed(title = "⛔ ┃ Censoring Invites Enabled", description = f"Censoring other server's invites is now enabled", color = 0x000000)
                        await interaction.response.send_message(embed = embed)
                else: return await interaction.response.send_message("Censor System is not enabled in this server.\nEnable it from /censor enable", ephemeral = True)
            await db.commit()

    # Censor display
    @app_commands.command(name = "display", description = "Display Censor System settings in this server")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def censor_display(self, interaction: discord.Interaction):
        async with aiosqlite.connect("db/censor.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS censor (guild ID, switch INTEGER, words TEXT, punishment TEXT, whitelist INTEGER, censor_links TEXT, censor_invites TEXT)")
                await cursor.execute("SELECT * FROM censor WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data:
                    if data[1] == 1: status = ":green_circle: Enabled"
                    else: status = ":red_circle: Disabled"
                    if data[2] == "[]": words = "None"
                    else: words = ", ".join(ast.literal_eval(data[2]))
                    punishment = str(data[3]).title()
                    whitelisted = self.bot.get_channel(int(data[4]))
                    if whitelisted: whitelisted = whitelisted.mention
                    censor_links = str(data[5]).title()
                    censor_invites = str(data[6]).title()
                    embed = discord.Embed(title=f"Censor System settings for {interaction.guild.name}", description=f"Status: **{status}**\nCensored Words: **{words}**\nPunishment: **{punishment}**\nWhitelisted Channel: **{whitelisted}**\nCensor Links: **{censor_links}**\nCensor Invites: **{censor_invites}**")
                    await interaction.response.send_message(embed=embed)
                else: await interaction.response.send_message("Censor System is not enabled in this server.\nEnable it from /censor enable", ephemeral = True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Censor(bot))