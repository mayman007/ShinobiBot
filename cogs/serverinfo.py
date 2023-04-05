import discord
from discord import app_commands
from discord.ext import commands

class Disavatar(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Server's Profile Avatar", style = discord.ButtonStyle.green)
    async def display_avatar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author:
            return await interaction.response.send_message("This avatar is not for you!", ephemeral = True)
        displayAvatar = user.display_avatar.url
        userAvatar = user.avatar.url
        if displayAvatar == userAvatar:
            button.style=discord.ButtonStyle.gray
            await interaction.response.send_message("This user doesn't have a server's avatar.", ephemeral = True)
            return await interaction.message.edit(view = self)
        e = discord.Embed(title = "Server's Profile Avatar Link", url = displayAvatar, color = 0x000000)
        e.set_author(name = user.name, icon_url = userAvatar)
        e.set_image(url = displayAvatar)
        e.set_footer(text = f"requested by {interaction.user}", icon_url = interaction.user.avatar.url)
        view=Avatar()
        await interaction.message.edit(embed = e, view = view)
        await interaction.response.defer()

class Avatar(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Main Avatar", style = discord.ButtonStyle.blurple)
    async def main_avatar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author:
            return await interaction.response.send_message("This avatar is not for you!", ephemeral = True)
        userAvatar = user.avatar.url
        e = discord.Embed(title = "Avatar Link", url = userAvatar, color = 0x000000)
        e.set_author(name = user.name, icon_url = userAvatar)
        e.set_image(url = userAvatar)
        e.set_footer(text = f"requested by {interaction.user}", icon_url = interaction.user.avatar.url)
        view=Disavatar()
        await interaction.message.edit(embed = e, view = view)
        await interaction.response.defer()

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
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def roles(self, interaction: discord.Interaction):
        roles = ', '.join([str(r.name) for r in interaction.guild.roles])
        embed = discord.Embed(title=f"{interaction.guild.name}", color = 0x00000)
        embed.add_field(name="Roles", value=f"{roles}", inline = True)
        await interaction.response.send_message(embed = embed)

    #server info command
    @app_commands.command(name = "server", description = "Shows information about the server.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def server(self, interaction: discord.Interaction):
        embed = discord.Embed(color = 0x2F3136)
        embed.add_field(name = '**🆔Server ID**', value = f"> {interaction.guild.id}", inline = True)
        embed.add_field(name = '**📆Created On**', value = f"> {interaction.guild.created_at.strftime('%b %d %Y')}", inline = True)
        embed.add_field(name = '**👑Owner**', value = f"> {interaction.guild.owner}", inline = True)
        embed.add_field(name = '**👥Members**', value = f'> {interaction.guild.member_count} Members | {sum(member.status != discord.Status.offline and not member.bot for member in interaction.guild.members)} Online', inline = True)
        embed.add_field(name = '**💬Channels**', value = f'> {len(interaction.guild.text_channels)} Text | {len(interaction.guild.voice_channels)} Voice', inline = True)
        embed.set_thumbnail(url = interaction.guild.icon.url)
        embed.set_footer(text = "Server Information")
        embed.set_author(name = f'{interaction.guild.name}', icon_url = interaction.guild.icon.url)
        await interaction.response.send_message(embed = embed)

    #owner info
    @app_commands.command(name = "owner", description = "Shows server's owner.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def owner(self, interaction: discord.Interaction):
        owner = str(interaction.guild.owner)
        name = str(interaction.guild.name)
        icon = str(interaction.guild.icon.url)
        embed = discord.Embed(title = name, color = 0x2F3136)
        embed.set_thumbnail(url = icon)
        embed.add_field(name = "**👑Owner**", value = f"**{owner}**", inline = True)
        await interaction.response.send_message(embed = embed)

    #id info
    @app_commands.command(name = "id", description = "Shows server's id.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def id(self, interaction: discord.Interaction):
        id = str(interaction.guild.id)
        name = str(interaction.guild.name)
        icon = str(interaction.guild.icon.url)
        embed = discord.Embed(title = name, color = 0x2F3136)
        embed.set_thumbnail(url = icon)
        embed.add_field(name = "**🆔Server ID**", value = f"**{id}**", inline = True)
        await interaction.response.send_message(embed = embed)

    #member count info
    @app_commands.command(name = "members", description = "Shows member's count.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def members(self, interaction: discord.Interaction):
        memberCount = str(interaction.guild.member_count)
        onlineCount = sum(member.status != discord.Status.offline and not member.bot for member in interaction.guild.members)
        name = str(interaction.guild.name)
        icon = str(interaction.guild.icon.url)
        embed = discord.Embed(title = name, color = 0x2F3136)
        embed.set_thumbnail(url = icon)
        embed.add_field(name = "**👥Members**", value = f"> {memberCount} Members | {onlineCount} Online", inline = True)
        await interaction.response.send_message(embed = embed)

    #channels count info
    @app_commands.command(name = "channels", description = "Shows channel's count.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def channelscount(self, interaction: discord.Interaction):
        name = str(interaction.guild.name)
        icon = str(interaction.guild.icon.url)
        embed = discord.Embed(title = name, color = 0x2F3136)
        embed.set_thumbnail(url = icon)
        embed.add_field(name = "**💬Channels**", value = f"> {len(interaction.guild.text_channels)} Text | {len(interaction.guild.voice_channels)} Voice", inline = True)
        await interaction.response.send_message(embed = embed)

    #server icon
    @app_commands.command(name = "icon", description = "Shows server's icon.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def icon(self, interaction: discord.Interaction):
        icon = str(interaction.guild.icon.url)
        e = discord.Embed(title = "Icon Link", url=f"{icon}", color = 0x2F3136)
        e.set_author(name = f"{interaction.user.name}", icon_url = f"{interaction.user.avatar.url}")
        e.set_image(url = f"{icon}")
        e.set_footer(text = f"requested by {interaction.user}", icon_url = interaction.user.avatar.url)
        await interaction.response.send_message(embed = e)

    #userinfo command
    @app_commands.command(name = "user", description = "Shows information about you or another user.")
    @app_commands.describe(member = "A member to show their info.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def user(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None: member = interaction.user
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(description = member.mention, color = 0x2F3136)
        embed.set_author(name = str(member), icon_url = member.avatar.url)
        embed.set_thumbnail(url = member.avatar.url)
        embed.add_field(name = "**Joined**", value = f"> {member.joined_at.strftime(date_format)}")
        members = sorted(interaction.guild.members, key = lambda m: m.joined_at)
        embed.add_field(name = "**Join position**", value = f"> {str(members.index(member)+1)}")
        embed.add_field(name = "**Registered**", value = f"> {member.created_at.strftime(date_format)}")
        if len(member.roles) > 1:
            role_string = ' '.join([r.mention for r in member.roles][1:])
            embed.add_field(name = "**Roles [{}]**".format(len(member.roles)-1), value = f"> {role_string}", inline = False)
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in member.guild_permissions if p[1]])
        embed.add_field(name = "**Guild permissions**", value = f"> {perm_string}", inline = False)
        embed.set_footer(text = 'ID: ' + str(member.id))
        await interaction.response.send_message(embed = embed)

    #banner command
    @app_commands.command(name = "banner", description = "Shows member's banner.")
    @app_commands.describe(member = "Member you want to show their banner.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def banner(self, interaction: discord.Interaction, member: discord.Member = None):
        if member == None: member = interaction.user
        #check if user has a banner and fetch it
        try:
            user = await self.bot.fetch_user(member.id)
            banner_url = user.banner.url # The URL of the banner
        except:
            await interaction.response.send_message("> The user doesn't have a banner.", ephemeral = True)
        #sending the banner
        userAvatar = member.avatar.url
        e = discord.Embed(title = "Banner Link", url = banner_url, color = 0x2F3136)
        e.set_author(name = member.name, icon_url = userAvatar)
        e.set_image(url = banner_url)
        e.set_footer(text = f"requested by {interaction.user}", icon_url = interaction.user.avatar.url)
        await interaction.response.send_message(embed = e)

    #avatar
    @app_commands.command(name = "avatar", description = "Shows member's avatar.")
    @app_commands.describe(member = "Member you want to show their avatar.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        if not member: member = interaction.user
        userAvatar = member.avatar.url
        e = discord.Embed(title = "Avatar Link ", url = userAvatar,color = 0x2F3136)
        e.set_author(name = member.name, icon_url = userAvatar)
        e.set_image(url = userAvatar)
        e.set_footer(text = f"requested by {interaction.user}", icon_url = interaction.user.avatar.url)
        global user
        global author
        user = member
        author = interaction.user
        view = Disavatar()
        await interaction.response.send_message(embed = e, view = view)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Serverinfo(bot))