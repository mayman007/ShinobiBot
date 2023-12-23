import discord
from discord import app_commands
from discord.ext import commands


#lock all confirm
class lockallConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def lockall_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("> This is not for you!", ephemeral = True)
        await interaction.response.defer()
        for channel in interaction.guild.channels:
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.send_messages = False
            await channel.set_permissions(interaction.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f"🔒 ┃ All Channels Locked! ┃ 🔒", description = f"{interaction.user.mention} had locked all channels in the server.")
        await interaction.followup.send(embed = emb)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def lockall_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user:
            return await interaction.response.send_message("> This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("> Process Canceled.")

#unlock all confirm
class unlockallConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def unlockall_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("> This is not for you!", ephemeral = True)
        await interaction.response.defer()
        for channel in interaction.guild.channels:
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.send_messages = True
            await channel.set_permissions(interaction.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f"🔓 ┃ All Channels Unlocked! ┃ 🔓", description = f"{interaction.user.mention} had unlocked all channels in the server.")
        await interaction.followup.send(embed = emb)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def unlockall_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user:
            return await interaction.response.send_message("> This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("> Process Canceled.")

# Lock Class
class Lock(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Lock is online.")

    #lock
    @app_commands.command(name = "lock", description = "Lockes a channel.")
    @app_commands.describe(channel = "Channel to lock (default is current channel).")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def lock(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        channel = channel or interaction.channel
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        if overwrite.send_messages == False:
            return await interaction.response.send_message("> The channel is already locked", ephemeral = True)
        overwrite.send_messages = False
        await channel.set_permissions(interaction.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f"🔒 ┃ Channel Locked!", description = f"> **{channel.mention}** has been locked.", color = 0x2F3136)
        await interaction.response.send_message(embed = emb)

    #lock all
    @app_commands.command(name = "lockall", description = "Lockes all the channels.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def lockall(self, interaction: discord.Interaction):
        lockall_em = discord.Embed(title = "Confirm", description = "Are you sure that you want to lock all your channels?")
        view = lockallConfirm()
        await interaction.response.send_message(embed = lockall_em, view = view)

    #unlock
    @app_commands.command(name = "unlock", description = "Unlocks a locked channel.")
    @app_commands.describe(channel = "Channel to unlock (default is current channel).")
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def unlock(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        channel = channel or interaction.channel
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        if overwrite.send_messages == True:
            return await interaction.response.send_message("> The channel is already unlocked", ephemeral = True)
        overwrite.send_messages = True
        await channel.set_permissions(interaction.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f"🔓 ┃ Channel Unlocked!", description = f"> **{channel.mention}** has been unlocked.", color = 0x2F3136)
        await interaction.response.send_message(embed = emb)

    #unlock all
    @app_commands.command(name = "unlockall", description = "unlockes all the channels.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def unlockall(self, interaction: discord.Interaction):
        unlockall_em = discord.Embed(title = "Confirm", description = "Are you sure that you want to unlock all your channels?")
        view = unlockallConfirm()
        await interaction.response.send_message(embed = unlockall_em, view = view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Lock(bot))