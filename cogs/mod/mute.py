import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from datetime import timedelta
from discord.ext.commands import guild_only
import aiosqlite


# ModMute Class
class ModMute(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("ModMute is online.")

    #TIMED MUTE!!!!!
    @app_commands.command(name = "mute", description = "Mutes a member.")
    @app_commands.describe(member = "Member to mute.", time = "Time of the mute.", reason = "Reason to mute.")
    @commands.guild_only()
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
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
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
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
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
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


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ModMute(bot))