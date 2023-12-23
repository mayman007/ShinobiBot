import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import guild_only


#unban all confirm
class unbanallConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def unbanall_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        for ban_entry in bans:
            await interaction.guild.unban(user = ban_entry.user)
        unbanall_embed = discord.Embed(title = "✅ ┃ Unban All! ┃ ✅", description = f"{interaction.message.interaction.user.mention} has unbanned all banned users! (total {len(bans)})", colour = discord.Colour.green())
        await interaction.followup.send(embed = unbanall_embed)

# ModBan Class
class ModBan(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("ModBan is online.")

    #ban command
    @app_commands.command(name = "ban", description = "Bans a member.")
    @app_commands.describe(member = "Member to ban.", reason = "Reason to ban.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
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
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
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
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(ban_members = True)
    @guild_only()  # Might not need ()
    async def unbanall(self, interaction: discord.Interaction):
        await interaction.response.defer()
        global bans
        bans = [ban_entry async for ban_entry in interaction.guild.bans()]   # list of discord.BanEntry
        for ban_entry in bans:
            await interaction.guild.unban(user = ban_entry.user)
        unbanall_embed = discord.Embed(title = "Confirm", description = "Are you sure that you want to unban all banned users?")
        view = unbanallConfirm()
        await interaction.followup.send(embed = unbanall_embed, view = view, ephemeral = True)

    #unban command
    @app_commands.command(name = "unban", description = "Unban banned member.")
    @app_commands.describe(id = "ID of the banned member.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
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


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ModBan(bot))