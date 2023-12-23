import discord
from discord import app_commands, ui
from discord.ext import commands
from datetime import datetime
import os

# Feedback button
class feedbackButton(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 600, commands.BucketType.member)
    @discord.ui.button(label = "Send Feedback", style = discord.ButtonStyle.blurple)
    async def feedback_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("> This is not for you!", ephemeral = True)
        retry = self.cooldown.get_bucket(interaction.message).update_rate_limit()
        if retry: return await interaction.response.send_message(f"Slow down! Try again in {round(retry, 1)} seconds!", ephemeral = True)
        await interaction.response.send_modal(feedbackModal())

# Feedback modal
class feedbackModal(ui.Modal, title = "Send Your Feedback"):
    ftitle = ui.TextInput(label = "Title", style = discord.TextStyle.short, placeholder = "Write a title for the issue/suggestion.", required = True, max_length = 50)
    fdes = ui.TextInput(label = "Long Description", style = discord.TextStyle.short, placeholder = "Descripe the issue/suggestion.", required = True, max_length = 1000)
    fsol = ui.TextInput(label = "Solution (optional)", style = discord.TextStyle.short, placeholder = "Write a solution for the issue.", required = False, max_length = 1000)
    async def on_submit(self, interaction: discord.Interaction):
        global feedback_channel
        invite = await interaction.channel.create_invite(max_age = 300)
        try:
            embed = discord.Embed(title = f"User: {interaction.user}\nServer: {interaction.guild.name}\n{invite}", description = f"**{self.ftitle}**", timestamp = datetime.now())
            embed.add_field(name = "Description", value = self.fdes)
            embed.add_field(name = "Solution", value = self.fsol)
            try: embed.set_author(name = interaction.user, icon_url = interaction.user.avatar)
            except: embed.set_author(name = interaction.user)
            await feedback_channel.send(embed = embed)
            await interaction.response.send_message("Your feedback has been sent succesfully!", ephemeral = True)
        except:
            embed = discord.Embed(title = f"User: {interaction.user}\nServer: {interaction.guild.name}\n{invite}", description = f"**{self.ftitle}**", timestamp = datetime.now())
            embed.add_field(name = "Description", value = self.fdes)
            try: embed.set_author(name = interaction.user, icon_url = interaction.user.avatar)
            except: embed.set_author(name = interaction.user)
            await feedback_channel.send(embed = embed)
            await interaction.response.send_message("Your feedback has been sent succesfully!", ephemeral = True)

# Feedback Class
class Feedback(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Feedback is online.")

    # Feedback command
    @app_commands.command(name = "feedback", description = "Send your feedback directly to the developers.")
    async def feedback(self, interaction: discord.Interaction):
        global feedback_channel
        feedback_channel = self.bot.get_channel(int(os.getenv("FEEDBACK_CHANNEL_ID")))
        view = feedbackButton()
        embed = discord.Embed(title = "If you had faced any problems or have any suggestions, feel free to send your feedback!")
        await interaction.response.send_message(embed = embed, view = view, ephemeral = True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Feedback(bot))