import discord
from discord import app_commands
from discord.ext import commands


class Disavatar(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Server's Profile Avatar", style = discord.ButtonStyle.green)
    async def display_avatar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user:
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
        try: e.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar.url)
        except: e.set_footer(text = f"Requested by {interaction.user}")
        view=Avatar()
        await interaction.message.edit(embed = e, view = view)
        await interaction.response.defer()

class Avatar(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Main Avatar", style = discord.ButtonStyle.blurple)
    async def main_avatar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user:
            return await interaction.response.send_message("This avatar is not for you!", ephemeral = True)
        userAvatar = user.avatar.url
        e = discord.Embed(title = "Avatar Link", url = userAvatar, color = 0x000000)
        e.set_author(name = user.name, icon_url = userAvatar)
        e.set_image(url = userAvatar)
        try: e.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar.url)
        except: e.set_footer(text = f"Requested by {interaction.user}")
        view=Disavatar()
        await interaction.message.edit(embed = e, view = view)
        await interaction.response.defer()

# UserInfo Class
class UserInfo(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name="User Info",
            callback=self.user_info_context_menu,
        )
        self.bot.tree.add_command(self.ctx_menu)

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("UserInfo is online.")

    #userinfo context menu
    async def user_info_context_menu(self, interaction: discord.Interaction, member: discord.Member):
        if member is None: member = interaction.user
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(description = member.mention, color = 0x2F3136)
        try: embed.set_author(name = str(member), icon_url = member.avatar.url)
        except: embed.set_author(name = str(member))
        try: embed.set_thumbnail(url = member.avatar.url)
        except: pass
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

    #userinfo command
    @app_commands.command(name = "user", description = "Shows information about you or another user.")
    @app_commands.describe(member = "A member to show their info.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def user_info(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None: member = interaction.user
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(description = member.mention, color = 0x2F3136)
        try: embed.set_author(name = str(member), icon_url = member.avatar.url)
        except: embed.set_author(name = str(member))
        try: embed.set_thumbnail(url = member.avatar.url)
        except: pass
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

    #avatar
    @app_commands.command(name = "avatar", description = "Shows member's avatar.")
    @app_commands.describe(member = "Member you want to show their avatar.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        if not member: member = interaction.user
        try: userAvatar = member.avatar.url
        except: return await interaction.response.send_message(f"{member.mention} doesn't have an avatar.", ephemeral = True)
        e = discord.Embed(title = "Avatar Link ", url = userAvatar,color = 0x2F3136)
        e.set_author(name = member.name, icon_url = userAvatar)
        e.set_image(url = userAvatar)
        try: e.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar.url)
        except: e.set_footer(text = f"Requested by {interaction.user}")
        global user
        user = member
        view = Disavatar()
        await interaction.response.send_message(embed = e, view = view)

    #banner command
    @app_commands.command(name = "banner", description = "Shows member's banner.")
    @app_commands.describe(member = "Member you want to show their banner.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def banner(self, interaction: discord.Interaction, member: discord.Member = None):
        if member == None: member = interaction.user
        #check if user has a banner and fetch it
        try:
            user = await self.bot.fetch_user(member.id)
            banner_url = user.banner.url # The URL of the banner
        except:
            await interaction.response.send_message("> The user doesn't have a banner.", ephemeral = True)
        #sending the banner
        e = discord.Embed(title = "Banner Link", url = banner_url, color = 0x2F3136)
        try: e.set_author(name = member.name, icon_url = member.avatar.url)
        except: e.set_author(name = member.name)
        e.set_image(url = banner_url)
        try: e.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar.url)
        except: e.set_footer(text = f"Requested by {interaction.user}")
        await interaction.response.send_message(embed = e)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UserInfo(bot))