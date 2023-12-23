import discord
from discord import app_commands
from discord.ext import commands


# ModKick Class
class ModKick(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("ModKick is online.")

    #kick command
    @app_commands.command(name = "kick", description = "Kicks a member.")
    @app_commands.describe(member = "Member to kick.", reason = "Reason to kick.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
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
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
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


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ModKick(bot))