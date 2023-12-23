import discord
from discord import app_commands
from discord.ext import commands


# Serverinfo Class
class Serverinfo(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Serverinfo is online.")

    #roles list
    @app_commands.command(name = "roles", description = "A list of roles.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def roles(self, interaction: discord.Interaction):
        roles = ', '.join([str(r.name) for r in interaction.guild.roles])
        embed = discord.Embed(title = interaction.guild.name, color = 0x00000)
        embed.add_field(name = "Roles", value = roles)
        await interaction.response.send_message(embed = embed)

    #server info command
    @app_commands.command(name = "server", description = "Shows information about the server.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def server(self, interaction: discord.Interaction):
        embed = discord.Embed(color = 0x2F3136)
        embed.add_field(name = "**🆔 Server ID**", value = interaction.guild.id)
        embed.add_field(name = "**📆 Created On**", value = interaction.guild.created_at.strftime('%b %d %Y'))
        embed.add_field(name = "**👑 Owner**", value = interaction.guild.owner.mention)
        embed.add_field(name = "**👥 Members**", value = f"**{interaction.guild.member_count}**")
        embed.add_field(name = f"**💬 Channels ({len(interaction.guild.text_channels) + len(interaction.guild.voice_channels)})**", value = f"**{len(interaction.guild.text_channels)}** Text | **{len(interaction.guild.voice_channels)}** Voice")
        embed.add_field(name = f"**:closed_lock_with_key: Roles ({len(interaction.guild.roles)})**", value = f"To see a list with all roles use </roles:1017544215871373399>", inline = False)
        try: embed.set_thumbnail(url = interaction.guild.icon.url)
        except: pass
        try: embed.set_author(name = interaction.guild.name, icon_url = interaction.guild.icon.url)
        except: embed.set_author(name = interaction.guild.name)
        await interaction.response.send_message(embed = embed)

    #owner info
    @app_commands.command(name = "owner", description = "Shows server's owner.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def owner(self, interaction: discord.Interaction):
        owner = str(interaction.guild.owner)
        name = str(interaction.guild.name)
        embed = discord.Embed(title = name, color = 0x2F3136)
        try: embed.set_thumbnail(url = interaction.guild.icon.url)
        except: pass
        embed.add_field(name = "**👑Owner**", value = f"**{owner}**", inline = True)
        await interaction.response.send_message(embed = embed)

    #id info
    @app_commands.command(name = "id", description = "Shows server's id.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def id(self, interaction: discord.Interaction):
        id = str(interaction.guild.id)
        name = str(interaction.guild.name)
        embed = discord.Embed(title = name, color = 0x2F3136)
        try: embed.set_thumbnail(url = interaction.guild.icon.url)
        except: pass
        embed.add_field(name = "**🆔Server ID**", value = f"**{id}**", inline = True)
        await interaction.response.send_message(embed = embed)

    #member count info
    @app_commands.command(name = "members", description = "Shows member's count.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def members(self, interaction: discord.Interaction):
        memberCount = str(interaction.guild.member_count)
        onlineCount = sum(member.status != discord.Status.offline and not member.bot for member in interaction.guild.members)
        name = str(interaction.guild.name)
        embed = discord.Embed(title = name, color = 0x2F3136)
        try: embed.set_thumbnail(url = interaction.guild.icon.url)
        except: pass
        embed.add_field(name = "**👥Members**", value = f"> {memberCount} Members | {onlineCount} Online", inline = True)
        await interaction.response.send_message(embed = embed)

    #channels count info
    @app_commands.command(name = "channels", description = "Shows channel's count.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def channelscount(self, interaction: discord.Interaction):
        name = str(interaction.guild.name)
        embed = discord.Embed(title = name, color = 0x2F3136)
        try: embed.set_thumbnail(url = interaction.guild.icon.url)
        except: pass
        embed.add_field(name = "**💬Channels**", value = f"> {len(interaction.guild.text_channels)} Text | {len(interaction.guild.voice_channels)} Voice", inline = True)
        await interaction.response.send_message(embed = embed)

    #server icon
    @app_commands.command(name = "icon", description = "Shows server's icon.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def icon(self, interaction: discord.Interaction):
        try: icon = str(interaction.guild.icon.url)
        except: return await interaction.response.send_message("Server has no icon.")
        e = discord.Embed(title = "Icon Link", url=f"{icon}", color = 0x2F3136)
        try: e.set_author(name = f"{interaction.user.name}", icon_url = f"{interaction.user.avatar.url}")
        except: e.set_author(name = f"{interaction.user.name}")
        e.set_image(url = f"{icon}")
        try: e.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar.url)
        except: e.set_footer(text = f"Requested by {interaction.user}")
        await interaction.response.send_message(embed = e)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Serverinfo(bot))
