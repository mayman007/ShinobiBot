import discord
from discord import app_commands
from discord.ext import commands


#hide all confirm
class hideallConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def hideall_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("> This is not for you!", ephemeral = True)
        await interaction.response.defer()
        for channel in interaction.guild.channels:
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.read_messages = False
            await channel.set_permissions(interaction.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f":closed_lock_with_key: ┃ All Channels Hid! ┃ :closed_lock_with_key:", description = f"> {interaction.user.mention} had hid all channels in the server.")
        await interaction.followup.send(embed = emb)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def hideall_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user:
            return await interaction.response.send_message("> This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("> Process Canceled.")

#show all confirm
class showallConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def showall_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("> This is not for you!", ephemeral = True)
        await interaction.response.defer()
        for channel in interaction.guild.channels:
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.read_messages = True
            await channel.set_permissions(interaction.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f"👁️ ┃ Channels Showed! ┃ 👁️", description = f"> {interaction.user.mention} had unhid all channels in the server.")
        await interaction.followup.send(embed = emb)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def showall_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user:
            return await interaction.response.send_message("> This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("> Process Canceled.")

# Hide Class
class Hide(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Hide is online.")

    #hide
    @app_commands.command(name = "hide", description = "Hide a channel.")
    @app_commands.describe(channel = "Channel to hide (default is current channel).")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def hidechat(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        channel = channel or interaction.channel
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        if overwrite.read_messages == False:
            await interaction.response.send_message("> The channel is already hidden!", ephemeral = True)
            return
        overwrite.read_messages = False
        await channel.set_permissions(interaction.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f":closed_lock_with_key: ┃ Channel Hid!", description = f"> **{channel.mention}** has been hidden.", color = 0x2F3136)
        await interaction.response.send_message(embed = emb)

    #hide all
    @app_commands.command(name = "hideall", description = "Hide all channels in the server.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def hideall(self, interaction: discord.Interaction):
        hideall_em = discord.Embed(title = "Confirm", description = "Are you sure that you want to hide all your channels?")
        view = hideallConfirm()
        await interaction.response.send_message(embed = hideall_em, view = view)

    #show
    @app_commands.command(name = "show", description = "Show a hidden channel.")
    @app_commands.describe(channel = "Channel to unhide (default is current channel).")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def showchat(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        channel = channel or interaction.channel
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        if overwrite.read_messages == True:
            return await interaction.response.send_message("> The channel is already shown!", ephemeral = True)
        overwrite.read_messages = True
        await channel.set_permissions(interaction.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f"👁️ ┃ Channel Showed!", description = f"> **{channel.mention}** has been shown.", color = 0x2F3136)
        await interaction.response.send_message(embed = emb)

    #show all
    @app_commands.command(name = "showall", description = "Unhide all channels in the server.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def showall(self, interaction: discord.Interaction):
        hideall_em = discord.Embed(title = "Confirm", description = "Are you sure that you want to unhide all your channels?")
        view = showallConfirm()
        await interaction.response.send_message(embed = hideall_em, view = view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Hide(bot))