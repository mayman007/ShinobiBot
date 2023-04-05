import discord
from discord.ext import commands
from discord import app_commands, utils
import os
from datetime import datetime
import aiosqlite


class ticket_launcher(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 600, commands.BucketType.member)

    @discord.ui.button(label = "Create a Ticket", style = discord.ButtonStyle.blurple, custom_id = "ticket_button", emoji = "📩")
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticket = utils.get(interaction.guild.text_channels, name = f"ticket-for-{interaction.user.name.lower().replace(' ', '-')}-{interaction.user.discriminator}")
        if ticket is not None: await interaction.response.send_message(f"You already have a ticket open at {ticket.mention}!", ephemeral = True)
        else:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                interaction.user: discord.PermissionOverwrite(view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True)
            }
            async with aiosqlite.connect("db/tickets_role.db") as db:
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS roles (role INTEGER, guild ID)") # Create the table if not exists
                    await cursor.execute("SELECT role FROM roles WHERE guild = ?", (interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data: ticket_role = data[0]
                    else: ticket_role = None
            if not ticket_role == None:
                ticket_role = interaction.guild.get_role(ticket_role)
                overwrites[ticket_role] = discord.PermissionOverwrite(view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True)
                ticket_sentence = f"{ticket_role.mention}, {interaction.user.mention} created a ticket!"
            else:
                ticket_sentence = f"{interaction.user.mention} created a ticket!"
            guild = interaction.guild
            category = discord.utils.get(guild.categories, name = "tickets")
            if category is None: #If there's no category matching with the `name`
                category = await guild.create_category("tickets") #Creates the category
            try:
                channel = await interaction.guild.create_text_channel(name = f"ticket-for-{interaction.user.name}-{interaction.user.discriminator}", overwrites = overwrites, reason = f"Ticket for {interaction.user}", category = category)
            except: return await interaction.response.send_message("Ticket creation failed! Make sure I have `Manage Channels` permissions!", ephemeral = True)
            await channel.send(ticket_sentence, view = main())
            await interaction.response.send_message(f"I've opened a ticket for you at {channel.mention}!", ephemeral = True)

class confirm(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.red, custom_id = "confirm")
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try: await interaction.channel.delete()
        except: await interaction.response.send_message("Channel deletion failed! Make sure I have `Manage Channels` permissions!", ephemeral = True)

class main(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)
    @discord.ui.button(label = "Close Ticket", style = discord.ButtonStyle.red, custom_id = "close")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title = "Are you sure you want to close this ticket?", color = discord.Colour.blurple())
        await interaction.response.send_message(embed = embed, view = confirm(), ephemeral = True)

class transcript(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)
    @discord.ui.button(label = "Transcript", style = discord.ButtonStyle.blurple, custom_id = "transcript")
    async def transcript(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if os.path.exists(f"{interaction.channel.id}.md"):
            return await interaction.followup.send(f"A transcript is already being generated!", ephemeral = True)
        with open(f"{interaction.channel.id}.md", 'a') as f:
            f.write(f"# Transcript of {interaction.channel.name}:\n\n")
            async for message in interaction.channel.history(limit = None, oldest_first = True):
                created = datetime.strftime(message.created_at, "%m/%d/%Y at %H:%M:%S")
                if message.edited_at:
                    edited = datetime.strftime(message.edited_at, "%m/%d/%Y at %H:%M:%S")
                    f.write(f"{message.author} on {created}: {message.clean_content} (Edited at {edited})\n")
                else:
                    f.write(f"{message.author} on {created}: {message.clean_content}\n")
            generated = datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
            f.write(f"\n*Generated at {generated} by {selfbot}*\n*Date Formatting: MM/DD/YY*\n*Time Zone: UTC*")
        with open(f"{interaction.channel.id}.md", 'rb') as f:
            await interaction.followup.send(file = discord.File(f, f"{interaction.channel.name}.md"))
        os.remove(f"{interaction.channel.id}.md")


# Ticket Class
class Ticket(commands.GroupCog, name = "ticket"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        global selfbot
        selfbot = self.bot.user
        print("Ticket is online.")

    #create ticket command
    @app_commands.command(name = "launch", description = "Launches the tickets system.")
    @app_commands.default_permissions(manage_guild = True)
    @app_commands.checks.cooldown(3, 60, key = lambda i: (i.guild_id))
    @app_commands.checks.has_permissions(manage_channels = True)
    async def launch(self, interaction: discord.Interaction):
        embed = discord.Embed(title = "Ticket!", description = "If you need support, click the button below and create a ticket!", color = discord.Colour.blue())
        await interaction.response.send_message(embed = embed, view = ticket_launcher())

    #close ticket
    @app_commands.command(name = "close", description = "Closes the ticket.")
    @app_commands.checks.has_permissions(manage_channels = True)
    async def close(self, interaction: discord.Interaction):
        if "ticket-for-" in interaction.channel.name:
            embed = discord.Embed(title = "> Are you sure that you want to close this ticket?", color = discord.Colour.blurple())
            await interaction.response.send_message(embed = embed, view = confirm(), ephemeral = True)
        else:
            await interaction.response.send_message("> This isn't a ticket!", ephemeral = True)

    #add a member to ticket
    @app_commands.command(name = "add", description = "Adds a member to the ticket.")
    @app_commands.describe(member = "The member you want to add to the ticket.")
    @app_commands.default_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(manage_channels = True)
    async def add(self, interaction: discord.Interaction, member: discord.Member):
        if "ticket-for-" in interaction.channel.name:
            await interaction.channel.set_permissions(member, view_channel = True, send_messages = True, attach_files = True, embed_links = True)
            await interaction.response.send_message(f"{member.mention} has been added to the ticket by {interaction.user.mention}.")
        else:
            await interaction.response.send_message("> This isn't a ticket!", ephemeral = True)

    #remove a member from ticket
    @app_commands.command(name = "remove", description = "Removes a member from the ticket.")
    @app_commands.describe(member = "The member you want to remove from the ticket.")
    @app_commands.default_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(manage_channels = True)
    async def remove(self, interaction: discord.Interaction, member: discord.Member):
        async with aiosqlite.connect("db/tickets_role.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS roles (role INTEGER, guild ID)") # Create the table if not exists
                await cursor.execute("SELECT role FROM roles WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: ticket_role = data[0]
                else: ticket_role = None
        if "ticket-for-" in interaction.channel.name:
            if not ticket_role == None:
                ticket_role = interaction.guild.get_role(ticket_role)
                if ticket_role not in interaction.user.roles and not interaction.user.guild_permissions.administrator:
                    return await interaction.response.send_message("You aren't authorized to do this!", ephemeral = True)
                elif ticket_role in member.roles or member.guild_permissions.administrator:
                    return await interaction.response.send_message(f"{member.mention} is a moderator!", ephemeral = True)
                else:
                    await interaction.channel.set_permissions(member, overwrite = None)
                    await interaction.response.send_message(f"{member.mention} has been removed from the ticket by {interaction.user.mention}.")
            else:
                if not interaction.user.guild_permissions.administrator:
                    return await interaction.response.send_message("You aren't authorized to do this!", ephemeral = True)
                elif member.guild_permissions.administrator:
                    return await interaction.response.send_message(f"{member.mention} is a moderator!", ephemeral = True)
                else:
                    await interaction.channel.set_permissions(member, overwrite = None)
                    await interaction.response.send_message(f"{member.mention} has been removed from the ticket by {interaction.user.mention}.")
        else:
            await interaction.response.send_message("This isn't a ticket!", ephemeral = True)

    # add/remove ticket role to sqlite db
    @app_commands.command(name = "role", description = "Adds/Removes a role from the tickets.")
    @app_commands.describe(action = "Do you want to add or remove a current role?", role = "The role you want to add.")
    @app_commands.choices(action = [app_commands.Choice(name = "add role", value = "add"), app_commands.Choice(name = "remove current role", value = "remove")])
    @app_commands.default_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(manage_channels = True)
    async def ticketrole(self, interaction: discord.Interaction, action: app_commands.Choice[str], role: discord.Role = None):
        async with aiosqlite.connect("db/tickets_role.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS roles (role INTEGER, guild ID)") # Create the table if not exists
                if action.value == "add": # Add data
                    if role == None: return await interaction.response.send_message("You have to select a role to add it.", ephemeral = True)
                    await cursor.execute("SELECT role FROM roles WHERE guild = ?", (interaction.guild.id,)) # Select role from the same row that has guild.id
                    data = await cursor.fetchone() # Fetch that row
                    if data: # If the row has data (already has a role id)
                        await cursor.execute("UPDATE roles SET role = ? WHERE guild = ?", (role.id, interaction.guild.id,)) # Update it
                    else: # If not
                        await cursor.execute("INSERT INTO roles (role, guild) VALUES (?, ?)", (role.id, interaction.guild.id,)) # Insert it
                    role_embed = discord.Embed(title = "Ticket Role Updated!", description = f"The role **{role}** has been addded to tickets", colour = discord.Colour.blue())
                    await interaction.response.send_message(embed = role_embed)
                else: # Remove data
                    await cursor.execute("SELECT role FROM roles WHERE guild = ?", (interaction.guild.id,)) # Select role from the same row that has guild.id
                    data = await cursor.fetchone() # Fetch that row
                    if data: # If the row has data (already has a role id)
                        await cursor.execute("DELETE FROM roles WHERE guild = ?", (interaction.guild.id,)) # Delete it
                        role_embed = discord.Embed(title = "Ticket Role Removed!", description = f"The ticket role has been removed.", colour = discord.Colour.blue())
                        await interaction.response.send_message(embed = role_embed)
                    else: # If not
                        await interaction.response.send_message("I didn't find a ticket role for this server.", ephemeral = True)
            await db.commit()

    # transcript
    @app_commands.command(name = "transcript", description = "Generates a transcript for a ticket.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def transcript(self, interaction: discord.Interaction): 
        if "ticket-for-" in interaction.channel.name:
            await interaction.response.defer()
            with open(f"{interaction.channel.id}.md", 'a') as f:
                f.write(f"# Transcript of {interaction.channel.name}:\n\n")
                async for message in interaction.channel.history(limit = None, oldest_first = True):
                    created = datetime.strftime(message.created_at, "%m/%d/%Y at %H:%M:%S")
                    if message.edited_at:
                        edited = datetime.strftime(message.edited_at, "%m/%d/%Y at %H:%M:%S")
                        f.write(f"{message.author} on {created}: {message.clean_content} (Edited at {edited})\n")
                    else:
                        f.write(f"{message.author} on {created}: {message.clean_content}\n")
                generated = datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
                f.write(f"\n*Generated at {generated} by {self.bot.user}*\n*Date Formatting: MM/DD/YY*\n*Time Zone: UTC*")
            with open(f"{interaction.channel.id}.md", 'rb') as f:
                await interaction.followup.send(file = discord.File(f, f"{interaction.channel.name}.md"))
            os.remove(f"{interaction.channel.id}.md") # Gives permission error because it is being used by another operation
        else: await interaction.response.send_message("This isn't a ticket!", ephemeral = True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ticket(bot))