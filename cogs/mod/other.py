import discord
from discord import app_commands
from discord.ext import commands


# ModOther Class
class ModOther(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("ModOther is online.")

    #clear command
    @app_commands.command(name = "clear", description = "Clears messages.")
    @app_commands.describe(amount = "Number of messages to clear (default amount is 1).")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(manage_messages = True)
    async def clear(self, interaction: discord.Interaction, amount: int = 1):
        await interaction.response.send_message(f"Deleted {amount} message(s)", ephemeral = True)
        await interaction.channel.purge(limit = amount)

    #role command
    @app_commands.command(name = "addrole", description = "Adds a role to a member.")
    @app_commands.describe(member = "Memebr to give the role.", role = "The role to give.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
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
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
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
    await bot.add_cog(ModOther(bot))