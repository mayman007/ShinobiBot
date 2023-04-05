import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from datetime import timedelta
from discord.ext.commands import guild_only
import aiosqlite


#unban all confirm
class unbanallConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def unbanall_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        for ban_entry in bans:
            await interaction.guild.unban(user = ban_entry.user)
        unbanall_embed = discord.Embed(title = "✅ ┃ Unban All! ┃ ✅", description = f"{author.mention} has unbanned all banned users! (total {len(bans)})", colour = discord.Colour.green())
        await interaction.followup.send(embed = unbanall_embed)

# Moderation Class
class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation is online.")

    #clear command
    @app_commands.command(name = "clear", description = "Clears messages.")
    @app_commands.describe(amount = "Number of messages to clear (default amount is 1).")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(manage_messages = True)
    async def clear(self, interaction: discord.Interaction, amount: int = 1):
        await interaction.response.send_message(f"Deleted {amount} message(s)", ephemeral = True)
        await interaction.channel.purge(limit = amount)

    #warn commands
    @app_commands.command(name = "warn", description = "Warn a member.")
    @app_commands.describe(member = "Member to warn.", reason = "Reason of warn.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(moderate_members = True)
    async def warn(self, interaction: discord.Interaction, member : discord.Member, reason: str = None):
        #check author role
        if interaction.user.top_role <= member.top_role:
            return await interaction.response.send_message(f"Your role must be higher than {member.mention}.", ephemeral = True)
        #check bot role
        if interaction.guild.me.top_role <= member.top_role:
            return await interaction.response.send_message(f"My role must be higher than {member.mention}.", ephemeral = True)
        if reason == None: reason = ""
        else: reason = f"\nReason: {reason}"
        # add warn to database
        async with aiosqlite.connect("db/warnings.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS warnings (warns INTEGER, member INTEGER, guild ID)")
                await cursor.execute("SELECT warns FROM warnings WHERE member = ? AND guild = ?", (member.id, interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE warnings SET warns = ? WHERE member = ? AND guild = ?", (data[0] + 1, member.id, interaction.guild.id,))
                else: await cursor.execute("INSERT INTO warnings (warns, member, guild) VALUES (?, ?, ?)", (1, member.id, interaction.guild.id,))
            await db.commit()
        warn_embed = discord.Embed(title = "⚠️ ┃ Warn!", description = f"{member.mention} has been warned by {interaction.user.mention}{reason}", colour = discord.Colour.red())
        await interaction.response.send_message(embed = warn_embed)

    #Multi-Warn
    @app_commands.command(name = "multiwarn", description = "Warns multiple members. (maximum 5 members.)")
    @app_commands.describe(member1 = "First Member to warn.", member2 = "Second Member to warn.", member3 = "Third Member to warn.", member4 = "Fourth Member to warn.", reason = "Reason of warn.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(moderate_members = True)
    async def multiwarn(self, interaction: discord.Interaction, member1: discord.Member, member2: discord.Member, member3: discord.Member = None, member4: discord.Member = None, reason: str = None):
        await interaction.response.defer()
        if member3 == None:
            members = [member1,member2]
            memberstext = f"{member1.mention} and {member2.mention}"
        elif member4 == None:
            members = [member1,member2,member3]
            memberstext = f"{member1.mention}, {member2.mention} and {member3.mention}"
        else:
            members = [member1,member2,member3,member4]
            memberstext = f"{member1.mention}, {member2.mention}, {member3.mention} and {member4.mention}"
        for member in members:
            #check author role
            if interaction.user.top_role <= member.top_role:
                return await interaction.response.send_message(f"Your role must be higher than {member.mention}.", ephemeral = True)
            #check bot role
            if interaction.guild.me.top_role <= member.top_role:
                return await interaction.response.send_message(f"My role must be higher than {member.mention}.", ephemeral = True)
        #add warning to database
        for member in members:
            async with aiosqlite.connect("db/warnings.db") as db: # Open the db
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS warnings (warns INTEGER, member INTEGER, guild ID)")
                    await cursor.execute("SELECT warns FROM warnings WHERE member = ? AND guild = ?", (member.id, interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data: await cursor.execute("UPDATE warnings SET warns = ? WHERE member = ? AND guild = ?", (data[0]+1, member.id, interaction.guild.id,))
                    else: await cursor.execute("INSERT INTO warnings (warns, member, guild) VALUES (?, ?, ?)", (1, member.id, interaction.guild.id,))
                await db.commit()
        if reason == None: reason = ""
        else: reason = f"\nReason: {reason}"
        warn_embed = discord.Embed(title = "⚠️ ┃ Multi-Warn! ┃ ⚠️", description = f"{memberstext} have been warned by {interaction.user.mention}{reason}", colour = discord.Colour.red())
        await interaction.followup.send(embed = warn_embed)

    #unwarn commands
    @app_commands.command(name = "unwarn", description = "Unwarn a member.")
    @app_commands.describe(member = "Member to unwarn.", amount = "Number of warnings to remove (default is 1 warn).")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(moderate_members = True)
    async def unwarn(self, interaction: discord.Interaction, member: discord.Member, amount: int = None):
        #check if member = author
        if interaction.user == member:
            return await interaction.response.send_message("> You can not unwarn yourself!", ephemeral = True)
        #check author role
        if interaction.user.top_role <= member.top_role:
            return await interaction.response.send_message(f"> Your role must be higher than {member.mention}!", ephemeral = True)
        #check bot role
        if interaction.guild.me.top_role <= member.top_role:
            return await interaction.response.send_message(f"> My role must be higher than {member.mention}!", ephemeral = True)
        if amount == None: amount = 1
        #remove warning from database
        async with aiosqlite.connect("db/warnings.db") as db: # Open the db
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS warnings (warns INTEGER, member INTEGER, guild ID)")
                    await cursor.execute("SELECT warns FROM warnings WHERE member = ? AND guild = ?", (member.id, interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data:
                        warns = data[0]
                        if warns - amount < 0: return await interaction.response.send_message(f"{member.mention} has **{warns}** warnings only.", ephemeral = True)
                        elif warns - amount == 0: await cursor.execute("DELETE FROM warnings WHERE member = ? AND guild = ?", (member.id, interaction.guild.id,))
                        else: await cursor.execute("UPDATE warnings SET warns = ? WHERE member = ? AND guild = ?", (warns - amount, member.id, interaction.guild.id,))
                    else: return await interaction.response.send_message(f"{member.mention} doesn't have any warnings.", ephemeral = True)
                await db.commit()
                warn_embed = discord.Embed(title = "✅ ┃ Unwarn!", description = f"**{amount}** warnings has been removed from {member.mention} by {interaction.user.mention}", colour = discord.Colour.green())
                await interaction.response.send_message(embed = warn_embed)

    #warnings list commands
    @app_commands.command(name = "warnings", description = "Get list of warnings for the user.")
    @app_commands.describe(member = "Member to view their warnings.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(moderate_members = True)
    async def warnings(self, interaction: discord.Interaction, member: discord.Member):
        async with aiosqlite.connect("db/warnings.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS warnings (warns INTEGER, member INTEGER, guild ID)")
                await cursor.execute("SELECT warns FROM warnings WHERE member = ? AND guild = ?", (member.id, interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await interaction.response.send_message(f"{member.mention} has **{data[0]}** warnings.")
                else: await interaction.response.send_message(f"{member.mention} doesn't have any warnings.", ephemeral = True)

    #timeout command
    @app_commands.command(name = "timeout", description = "Timeouts members. (maximum 5 members.)")
    @app_commands.describe(member = "Member to timeout.", time = "Time of the timeout.", reason = "Reason to timeout.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(moderate_members = True)
    async def timeout(self, interaction: discord.Interaction, member : discord.Member, time: str, reason: str = None):
        #check author role
        if interaction.user.top_role <= member.top_role:
            return await interaction.response.send_message(f"Your role must be higher than {member.mention}.", ephemeral = True)
        #check bot role
        if interaction.guild.me.top_role <= member.top_role:
            return await interaction.response.send_message(f"My role must be higher than {member.mention}.", ephemeral = True)
        #time stuff
        if time == None:
            time_string = ""
        else:
            time_string = f"\nTime: {time}"
            get_time = {
            "s": 1, "m": 60, "h": 3600, "d": 86400,
            "w": 604800, "mo": 2592000, "y": 31104000 }
            a = time[-1]
            b = get_time.get(a)
            c = time[:-1]
            try: int(c)
            except: return await interaction.response.send_message("Type time and time unit (s,m,h,d,w,mo,y) correctly.", ephemeral = True)
            try: sleep = int(b) * int(c)
            except: return await interaction.response.send_message("Type time and time unit (s,m,h,d,w,mo,y) correctly.", ephemeral = True)
        #timing out
        await member.timeout(timedelta(seconds = sleep), reason = reason)
        #check reason
        if reason == None: reason = ""
        else: reason = f"\nReason: {reason}"
        timeout_embed = discord.Embed(title = "Timeout!", description = f"{member.mention} has been timed out by {interaction.user.mention}{time_string}{reason}", colour = discord.Colour.red())
        await interaction.response.send_message(embed = timeout_embed)
        #timeout over message
        await asyncio.sleep(int(sleep))
        timeout_embed = discord.Embed(title = "Timeout over!", description = f"{member.mention}'s timeout is over", colour = discord.Colour.green())
        await interaction.response.send_message(embed = timeout_embed)

    #Multi-Timeout
    @app_commands.command(name = "multitimeout", description = "Timeouts multiple members. (maximum 5 members.)")
    @app_commands.describe(time = "Time of timeout.", member1 = "First Member to timeout.", member2 = "Second Member to timeout.", member3 = "Third Member to timeout.", member4 = "Fourth Member to timeout.", reason = "Reason of timeout.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(moderate_members = True)
    async def multitimeout(self, interaction: discord.Interaction, time: str, member1: discord.Member, member2: discord.Member, member3: discord.Member = None, member4: discord.Member = None, reason: str = None):
        await interaction.response.defer()
        if member3 == None:
            members = [member1,member2]
            memberstext = f"{member1.mention} and {member2.mention}"
        elif member4 == None:
            members = [member1,member2,member3]
            memberstext = f"{member1.mention}, {member2.mention} and {member3.mention}"
        else:
            members = [member1,member2,member3,member4]
            memberstext = f"{member1.mention}, {member2.mention}, {member3.mention} and {member4.mention}"
        for member in members:
            #check author role
            if interaction.user.top_role <= member.top_role:
                return await interaction.response.send_message(f"Your role must be higher than {member.mention}.", ephemeral = True)
            #check bot role
            if interaction.guild.me.top_role <= member.top_role:
                return await interaction.response.send_message(f"My role must be higher than {member.mention}.", ephemeral = True)
        #time stuff
        if time == None:
            time_string = ""
        else:
            time_string = f"\nTime: {time}"
            get_time = {
            "s": 1, "m": 60, "h": 3600, "d": 86400,
            "w": 604800, "mo": 2592000, "y": 31104000 }
            a = time[-1]
            b = get_time.get(a)
            c = time[:-1]
            try: int(c)
            except: return await interaction.response.send_message("Type time and time unit (s,m,h,d,w,mo,y) correctly.", ephemeral = True)
            try: sleep = int(b) * int(c)
            except: return await interaction.response.send_message("Type time and time unit (s,m,h,d,w,mo,y) correctly.", ephemeral = True)
        #timing out
        for member in members: await member.timeout(timedelta(seconds = sleep), reason = reason)
        #check reason
        if reason == None: reason = ""
        else: reason = f"\nReason: {reason}"
        timeout_embed = discord.Embed(title = "Multi-Time out!", description = f"{memberstext} have been timed out by {interaction.user.mention}{time_string}{reason}", colour = discord.Colour.red())
        await interaction.followup.send(embed = timeout_embed)
        #timeout over message
        await asyncio.sleep(int(sleep))
        untimeout_embed = discord.Embed(title = "Multi-Timeout over!",
        description = f"{memberstext}'s timeout is over",
        colour = discord.Colour.green())
        await interaction.followup.send(embed = untimeout_embed)

    #kick command
    @app_commands.command(name = "kick", description = "Kicks a member.")
    @app_commands.describe(member = "Member to kick.", reason = "Reason to kick.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(kick_members = True)
    async def kick(self, interaction: discord.Interaction, member : discord.Member, reason: str = None):
        #check author role
        if interaction.user.top_role <= member.top_role:
            return await interaction.response.send_message(f"Your role must be higher than **{member.mention}**.", ephemeral = True)
        #check bot role
        if interaction.guild.me.top_role <= member.top_role:
            return await interaction.response.send_message(f"My role must be higher than **{member.mention}**.", ephemeral = True)
        if reason == None: reason = ""
        else: reason = f"\nReason: {reason}"
        await member.kick(reason = reason)
        kick_embed = discord.Embed(title = "🦵 ┃ Kick!", description = f"{member.mention} has been kicked by {interaction.user.mention}{reason}", colour = discord.Colour.red())
        await interaction.response.send_message(embed = kick_embed)
        await member.send(f"You have been kicked from **{interaction.guild.name}**{reason}")

    #Multi-Kick
    @app_commands.command(name = "multikick", description = "Kicks multiple members. (maximum 5 members.)")
    @app_commands.describe(member1 = "First Member to kick.", member2 = "Second Member to kick.", member3 = "Third Member to kick.", member4 = "Fourth Member to kick.", reason = "Reason of kick.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(moderate_members = True)
    async def multikick(self, interaction: discord.Interaction, member1: discord.Member, member2: discord.Member, member3: discord.Member = None, member4: discord.Member = None, reason: str = None):
        await interaction.response.defer()
        if member3 == None:
            members = [member1,member2]
            memberstext = f"{member1.mention} and {member2.mention}"
        elif member4 == None:
            members = [member1,member2,member3]
            memberstext = f"{member1.mention}, {member2.mention} and {member3.mention}"
        else:
            members = [member1,member2,member3,member4]
            memberstext = f"{member1.mention}, {member2.mention}, {member3.mention} and {member4.mention}"
        for member in members:
            #check author role
            if interaction.user.top_role <= member.top_role:
                return await interaction.response.send_message(f"Your role must be higher than **{member.mention}**.", ephemeral = True)
            #check bot role
            if interaction.guild.me.top_role <= member.top_role:
                return await interaction.response.send_message(f"My role must be higher than **{member.mention}**.", ephemeral = True)
        for member in members:
            await member.kick(reason = reason)
            await member.send(f"You have been kicked from **{interaction.guild.name}**{reason}")
        if reason == None: reason = ""
        else: reason = f"\nReason: {reason}"
        kick_embed = discord.Embed(title = "🦵 ┃ Multi-Kick! ┃ 🦵", description = f"**{memberstext}** have been kicked by {interaction.user.mention}{reason}", colour = discord.Colour.red())
        await interaction.followup.send(embed = kick_embed)

    #ban command
    @app_commands.command(name = "ban", description = "Bans a member.")
    @app_commands.describe(member = "Member to ban.", reason = "Reason to ban.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(ban_members = True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        #check author role
        if interaction.user.top_role <= member.top_role:
            return await interaction.response.send_message(f"Your role must be higher than **{member.mention}**.", ephemeral = True)
        #check bot role
        if interaction.guild.me.top_role <= member.top_role:
            return await interaction.response.send_message(f"Your role must be higher than **{member.mention}**.", ephemeral = True)
        await member.ban(reason = reason)
        if reason == None: reason = ""
        else: reason = f"\nReason: {reason}"
        ban_embed = discord.Embed(title = "🚫 ┃ Ban!", description = f"{member.mention} has been banned by {interaction.user.mention}{reason}", colour = discord.Colour.red())
        await interaction.response.send_message(embed = ban_embed)
        await member.send(f"You have been banned from **{interaction.guild.name}**{reason}")

    #Multi-Ban
    @app_commands.command(name = "multiban", description = "Bans multiple members. (maximum 5 members.)")
    @app_commands.describe(member1 = "First Member to ban.", member2 = "Second Member to ban.", member3 = "Third Member to ban.", member4 = "Fourth Member to ban.", reason = "Reason of ban.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(moderate_members = True)
    async def multiban(self, interaction: discord.Interaction, member1: discord.Member, member2: discord.Member, member3: discord.Member = None, member4: discord.Member = None, reason: str = None):
        await interaction.response.defer()
        if member3 == None:
            members = [member1,member2]
            memberstext = f"{member1.mention} and {member2.mention}"
        elif member4 == None:
            members = [member1,member2,member3]
            memberstext = f"{member1.mention}, {member2.mention} and {member3.mention}"
        else:
            members = [member1,member2,member3,member4]
            memberstext = f"{member1.mention}, {member2.mention}, {member3.mention} and {member4.mention}"
        for member in members:
            #check author role
            if interaction.user.top_role <= member.top_role:
                return await interaction.response.send_message(f"Your role must be higher than **{member.mention}**.", ephemeral = True)
            #check bot role
            if interaction.guild.me.top_role <= member.top_role:
                return await interaction.response.send_message(f"My role must be higher than **{member.mention}**.", ephemeral = True)
        for member in members:
            await member.ban(reason = reason)
            if not member.bot: await member.send(f"You have been banned from **{interaction.guild.name}**{reason}")
        if reason == None: reason = ""
        else: reason = f"\nReason: {reason}"
        ban_embed = discord.Embed(title = "🚫 ┃ Multi-Ban! ┃ 🚫", description = f"{memberstext} have been banned by {interaction.user.mention}{reason}", colour = discord.Colour.red())
        await interaction.followup.send(embed = ban_embed)

    #unban all command
    @app_commands.command(name = "unbanall", description = "Unban all banned users.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(ban_members = True)
    @guild_only()  # Might not need ()
    async def unbanall(self, interaction: discord.Interaction):
        await interaction.response.defer()
        global author
        global bans
        author = interaction.user
        bans = [ban_entry async for ban_entry in interaction.guild.bans()]   # list of discord.BanEntry
        for ban_entry in bans:
            await interaction.guild.unban(user = ban_entry.user)
        unbanall_embed = discord.Embed(title = "Confirm", description = "Are you sure that you want to unban all banned users?")
        view = unbanallConfirm()
        await interaction.followup.send(embed = unbanall_embed, view = view, ephemeral = True)

    #unban command
    @app_commands.command(name = "unban", description = "Unban banned member.")
    @app_commands.describe(id = "ID of the banned member.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(ban_members = True)
    @guild_only()  # Might not need ()
    async def unban(self, interaction: discord.Interaction, id: int):
        try:
            user = await self.bot.fetch_user(id)
            try: await interaction.guild.unban(user)
            except: return await interaction.response.send_message(f"{user.mention} is not banned", ephemeral = True)
        except:
            return await interaction.response.send_message("Enter a valid id.", ephemeral = True)
        unban_embed = discord.Embed(title = "✅ ┃ Unban!", description = f"{user} has been unbanned by {interaction.user.mention}", colour = discord.Colour.green())
        await interaction.response.send_message(embed = unban_embed)

    #TIMED MUTE!!!!!
    @app_commands.command(name = "mute", description = "Mutes a member.")
    @app_commands.describe(member = "Member to mute.", time = "Time of the mute.", reason = "Reason to mute.")
    @commands.guild_only()
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(manage_roles = True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, time: str = None , reason: str = None):
        if interaction.user.top_role <= member.top_role: # Check user role
            return await interaction.response.send_message(f"Your role must be higher than {member.mention}.", ephemeral = True)
        elif interaction.guild.me.top_role <= member.top_role: # Check bot role
            return await interaction.response.send_message(f"My role must be higher than {member.mention}.", ephemeral = True)
        mutedRole = discord.utils.find(lambda r: r.name == "SB-Muted", interaction.guild.roles) # Get role
        if not mutedRole: # Check if the role is in the guild
            mutedRole = await interaction.guild.create_role(name = "SB-Muted") # If not, make it
            for channel in interaction.guild.channels: await channel.set_permissions(mutedRole, send_messages = False) # Apply the permissions in all channels
        elif mutedRole in member.roles: return await interaction.response.send_message(f"{member.mention} is already muted.", ephemeral = True) # Check if muted
        # Check if reason
        if reason == None: reason = ""
        else: reason = "\nReason: " + reason
        # Check if time stuff
        if time == None: time_string = ""
        else: # Time stuff
            time_string = "\nTime: " + time
            get_time = {
            "s": 1, "m": 60, "h": 3600, "d": 86400,
            "w": 604800, "mo": 2592000, "y": 31104000 }
            a = time[-1]
            b = get_time.get(a)
            c = time[:-1]
            try: int(c)
            except: return await interaction.response.send_message("Type time and time unit (s,m,h,d,w,mo,y) correctly.", ephemeral = True)
            try: sleep = int(b) * int(c)
            except: return await interaction.response.send_message("Type time and time unit (s,m,h,d,w,mo,y) correctly.", ephemeral = True)
        await member.add_roles(mutedRole) # Add role
        mute_embed = discord.Embed(title = "🔇 ┃ Mute!", description = f"{member.mention} has been muted by {interaction.user.mention}{time_string}{reason}", colour = discord.Colour.red())
        await interaction.response.send_message(embed = mute_embed) # Send embed
        if time: # If time
            await asyncio.sleep(sleep) # Wait for the time
            await member.remove_roles(mutedRole) # Remove role
            unmute_embed = discord.Embed(title = "🔊 ┃ Mute over!", description = f"{member.mention}'s mute is over", colour = discord.Colour.green())
            await interaction.followup.send(embed = unmute_embed) # Send embed

    #Multi-Mute
    @app_commands.command(name = "multimute", description = "Mutes multiple members. (maximum 5 members.)")
    @app_commands.describe(member1 = "First Member to mute.", member2 = "Second Member to mute.", member3 = "Third Member to mute.", member4 = "Fourth Member to mute.", time = "Time of mute.", reason = "Reason of mute.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(moderate_members = True)
    async def multimute(self, interaction: discord.Interaction, member1: discord.Member, member2: discord.Member, member3: discord.Member = None, member4: discord.Member = None, time: str = None, reason: str = None):
        await interaction.response.defer() # Cause it will take time looping through all members
        if member3 == None:
            members = [member1,member2]
            memberstext = f"{member1.mention} and {member2.mention}"
        elif member4 == None:
            members = [member1,member2,member3]
            memberstext = f"{member1.mention}, {member2.mention} and {member3.mention}"
        else:
            members = [member1,member2,member3,member4]
            memberstext = f"{member1.mention}, {member2.mention}, {member3.mention} and {member4.mention}"
        mutedRole = discord.utils.find(lambda r: r.name == "SB-Muted", interaction.guild.roles) # Get role
        if not mutedRole: # Check if role is in the guild
            mutedRole = await interaction.guild.create_role(name = "SB-Muted") # If not, make it
            for channel in interaction.guild.channels: await channel.set_permissions(mutedRole, send_messages = False) # Apply the permissions in all channels
        for member in members:
            if interaction.user.top_role <= member.top_role: # Check user role
                return await interaction.response.send_message(f"Your role must be higher than {member.mention}.", ephemeral = True)
            elif interaction.guild.me.top_role <= member.top_role: # Check bot role
                return await interaction.response.send_message(f"My role must be higher than {member.mention}.", ephemeral = True)
            elif mutedRole in member.roles: # Check if muted
                return await interaction.response.send_message(f"{member.mention} is already muted.", ephemeral = True)
        # Check reason
        if reason == None: reason = ""
        else: reason = f"\nReason: {reason}"
        # Check time
        if time == None:
            time_string = ""
        else: # Time stuff
            time_string = f"\nTime: {time}"
            get_time = {
            "s": 1, "m": 60, "h": 3600, "d": 86400,
            "w": 604800, "mo": 2592000, "y": 31104000 }
            a = time[-1]
            b = get_time.get(a)
            c = time[:-1]
            try: int(c)
            except: return await interaction.response.send_message("Type time and time unit (s,m,h,d,w,mo,y) correctly.", ephemeral = True)
            try: sleep = int(b) * int(c)
            except: return await interaction.response.send_message("Type time and time unit (s,m,h,d,w,mo,y) correctly.", ephemeral = True)
        for member in members: await member.add_roles(mutedRole) # Add the role to all the members
        mute_embed = discord.Embed(title = "🔇 ┃ Multi-Mute! ┃ 🔇", description = f"{memberstext} have been muted by {interaction.user.mention}{time_string}{reason}", colour = discord.Colour.red())
        await interaction.followup.send(embed = mute_embed) # Send the embed
        if time: # If time
            await asyncio.sleep(sleep) # Wait for the time
            for member in members: await member.remove_roles(mutedRole) # Remove the roles from all the members
            unmute_embed = discord.Embed(title = "🔊 ┃ Multi-Mute over! ┃ 🔊", description = f"{memberstext}'s mute is over", colour = discord.Colour.green())
            await interaction.followup.send(embed = unmute_embed) # Send the embed

    #unmute command
    @app_commands.command(name = "unmute", description = "Unmutes a member.")
    @app_commands.describe(member = "Member to unmute.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(manage_roles = True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        mutedRole = discord.utils.find(lambda r: r.name == "SB-Muted", interaction.guild.roles) # Get role
        if not mutedRole in member.roles: return await interaction.response.send_message(f"{member.mention} is not muted.", ephemeral = True) # Check if not muted
        if interaction.user == member: return await interaction.response.send_message("You can not unmute yourself.", ephemeral = True) # Check if unmuting themselves
        if interaction.user.top_role <= member.top_role: return await interaction.response.send_message(f"Your role must be higher than {member.mention}!") # Check user role
        if interaction.guild.me.top_role <= member.top_role: return await interaction.response.send_message(f"My role must be higher than {member.mention}!", ephemeral = True) # Check bot role
        await member.remove_roles(mutedRole) # Remove the role
        if not member.bot: await member.send(f"You have been unmuted from **{interaction.guild.name}**.") # DM the member if not bot
        embed = discord.Embed(title = "🔊 ┃ Unmute!", description = f"{member.mention} has been unmuted", colour = discord.Colour.green())
        await interaction.response.send_message(embed = embed) # Send the embed

    # #JAIL COMMAND!!!!!
    # @app_commands.command(name = "jail", description = "Jails a member.")
    # @app_commands.describe(member = "Member to jail.", time = "Time of the jail.", reason = "Reason to jail.")
    # @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    # @app_commands.checks.has_permissions(manage_roles = True)
    # async def jail(self, interaction: discord.Interaction, member: discord.Member, time: str = None, reason: str = None):
    #     #check author role
    #     if interaction.user.top_role <= member.top_role:
    #         return await interaction.response.send_message(f"> Your role must be higher than {member.mention}!", ephemeral = True)
    #     #check bot role
    #     if interaction.guild.me.top_role <= member.top_role:
    #         return await interaction.response.send_message(f"> My role must be higher than {member.mention}!", ephemeral = True)
    #     #check if member is muted
    #     role = discord.utils.find(lambda r: r.name == 'SB-Jailed', interaction.guild.roles)
    #     if role in member.roles:
    #         return await interaction.response.send_message(f"> **{member.mention}** is already muted!", ephemeral = True)
    #     #check reason
    #     if reason == None: reason = ""
    #     else: reason = " for " + reason
    #     #time stuff
    #     if time == None: timer = ""
    #     else:
    #         get_time = {
    #         "s": 1, "m": 60, "h": 3600, "d": 86400,
    #         "w": 604800, "mo": 2592000, "y": 31104000 }
    #         timer = " to " + time
    #         a = time[-1]
    #         b = get_time.get(a)
    #         c = time[:-1]
    #         try: int(c)
    #         except: return await interaction.response.send_message("> Type time and time unit [s,m,h,d,w,mo,y] correctly.", ephemeral = True)
    #         try: sleep = int(b) * int(c)
    #         except: return await interaction.response.send_message("> Type time and time unit [s,m,h,d,w,mo,y] correctly.", ephemeral = True)
    #     #get role
    #     guild = interaction.guild
    #     jailedRole = discord.utils.get(guild.roles, name = "SB-Jailed")
    #     #To make the role if it is not in the server
    #     if not jailedRole:
    #         jailedRole = await guild.create_role(name = "SB-Jailed")
    #         for channel in guild.channels:
    #             await channel.set_permissions(jailedRole, speak = False, send_messages = False,
    #                                         read_message_history = True, read_messages = False)
    #     #create jail channel
    #     category = discord.utils.get(guild.categories, name='jails')
    #     if category is None: #If there's no category matching with the `name`
    #         category = await guild.create_category('jails') #Creates the category
    #     overwrites = {
    #                 jailedRole: discord.PermissionOverwrite(read_messages = True),
    #                 guild.default_role: discord.PermissionOverwrite(read_messages = False),
    #                 guild.me: discord.PermissionOverwrite(read_messages = True)
    #             }
    #     #create jail channel
    #     channel = await guild.create_text_channel(name = f"jail-{member.name}-{member.id}", overwrites = overwrites, category = category)
    #     channel_id = channel.id
    #     channel_really = self.bot.get_channel(int(channel_id))
    #     await channel_really.edit(slowmode_delay = 10)
    #     #add jail to json
    #     # with open("jsons/jails.json", "r", encoding = "utf8") as f:
    #     #     user = json.load(f)
    #     # with open("jsons/jails.json", "w", encoding = "utf8") as f:
    #     #     user[str(member.id)] = channel_id
    #     #     json.dump(user, f, sort_keys = True, indent = 4, ensure_ascii = False)
    #     #Jail starts message
    #     await member.add_roles(jailedRole)
    #     mute_embed = discord.Embed(title = "⛓️ ┃ Jail!",
    #     description = f"{member.mention} has been jailed by {interaction.user.mention}{reason}{timer}",
    #     colour = discord.Colour.red())
    #     await interaction.response.send_message(embed = mute_embed)
    #     await channel_really.send(f"{member.mention} You have been jailed{reason}{timer}.")
    #     #Jail over message
    #     await asyncio.sleep(int(sleep))
    #     await member.remove_roles(jailedRole)
    #     await channel_really.delete()
    #     unmute_embed = discord.Embed(title = "🧑‍⚖️ ┃ Jail over!",
    #     description = f"{member.mention} jail {timer} {reason} is over",
    #     colour = discord.Colour.green())
    #     await interaction.response.send_message(embed = unmute_embed)

    # #UNJAIL command
    # @app_commands.command(name = "unjail", description = "Unjails a member.")
    # @app_commands.describe(member = "Member to unjail.")
    # @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    # @app_commands.checks.has_permissions(manage_roles = True)
    # async def unjail(self, interaction: discord.Interaction, member: discord.Member):
    #     # channel = discord.utils.get(ctx.guild.channels, name=f"jail-{member.name}-{member.discriminator}") # doesn't work
    #     jailedRole = discord.utils.get(member.roles, name = "SB-Jailed")
    #     #check if member is muted
    #     if jailedRole in member.roles: pass
    #     else: return await interaction.response.send_message(f"> {member.mention} is not jailed!", ephemeral = True)
    #     if interaction.user == member:
    #         return await interaction.response.send_message("> You can not unjail yourself!", ephemeral = True)
    #     if interaction.user.top_role <= member.top_role:
    #         return await interaction.response.send_message(f"> Your role must be higher than **{member.mention}**!", ephemeral = True)
    #     await member.remove_roles(jailedRole)
    #     #remove jail from json
    #     # with open("jsons/jails.json", "r", encoding = "utf8") as f:
    #     #     user = json.load(f)
    #     #     channel_id = user[str(member.id)]
    #     # user.pop(str(member.id))
    #     # with open("jsons/jails.json", "w", encoding = "utf8") as f:
    #     #     json.dump(user, f, sort_keys = True, indent = 4, ensure_ascii = False)
    #     jailedChannel = discord.utils.get(interaction.guild.channels, name = f"jail-{member.name}-{member.id}")
    #     await jailedChannel.delete()
    #     await member.send(f"> you have been unjailed from **{interaction.guild.name}**")
    #     embed = discord.Embed(title = "🧑‍⚖️ ┃ Unjail!",
    #     description = f"{member.mention} has been unjailed",
    #     colour = discord.Colour.green())
    #     await interaction.response.send_message(embed = embed)

    #role command
    @app_commands.command(name = "addrole", description = "Adds a role to a member.")
    @app_commands.describe(member = "Memebr to give the role.", role = "The role to give.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(manage_roles = True)
    async def role(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        #check author role
        if interaction.user.top_role <= member.top_role:
            return await interaction.response.send_message(f"Your role must be higher than {member.mention}.", ephemeral = True)
        #check bot role
        if interaction.guild.me.top_role <= member.top_role:
            return await interaction.response.send_message(f"My role must be higher than {member.mention}.", ephemeral = True)
        #check if member has the role
        if role in member.roles:
            return await interaction.response.send_message(f"{member.mention} already has that role.", ephemeral = True)
        #add the role
        await member.add_roles(role)
        addrole_embed = discord.Embed(title = "Role added!", description = f"{member.mention} has been given the role {role.mention}", colour = discord.Colour.green())
        await interaction.response.send_message(embed = addrole_embed)

    #remove role command
    @app_commands.command(name = "removerole", description = "Removes a role from a member.")
    @app_commands.describe(member = "Memebr to remove the role from.", role = "The role to remove.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(manage_roles = True)
    async def delrole(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        #check author role
        if interaction.user.top_role <= member.top_role:
            await interaction.response.send_message(f"Your role must be higher than {member.mention}.", ephemeral = True)
            return
        #check bot role
        if interaction.guild.me.top_role <= member.top_role:
            return await interaction.response.send_message(f"My role must be higher than {member.mention}.", ephemeral = True)
        #check if member has the role
        if not role in member.roles:
            return await interaction.response.send_message(f"{member.mention} doesn't have that role.", ephemeral = True)
        #add the role
        await member.remove_roles(role)
        addrole_embed = discord.Embed(title = "Role removed!", description = f"{member.mention} no longer has the role {role.mention}", colour = discord.Colour.red())
        await interaction.response.send_message(embed = addrole_embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))