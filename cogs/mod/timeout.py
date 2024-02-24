import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from datetime import timedelta


# ModTimeout Class
class ModTimeout(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("ModTimeout is online.")

    #timeout command
    @app_commands.command(name = "timeout", description = "Timeouts members. (maximum 5 members.)")
    @app_commands.describe(member = "Member to timeout.", time = "Time of the timeout.", reason = "Reason to timeout.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
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
        await interaction.followup.send(embed = timeout_embed)

    #Multi-Timeout
    @app_commands.command(name = "multitimeout", description = "Timeouts multiple members. (maximum 5 members.)")
    @app_commands.describe(time = "Time of timeout.", member1 = "First Member to timeout.", member2 = "Second Member to timeout.", member3 = "Third Member to timeout.", member4 = "Fourth Member to timeout.", reason = "Reason of timeout.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
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


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ModTimeout(bot))