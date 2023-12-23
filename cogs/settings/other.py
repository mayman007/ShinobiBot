import discord
from discord import app_commands
from discord.ext import commands
import asyncio


# SettingsOther Class
class SettingsOther(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("SettingsOther is online.")

    #private channel
    @app_commands.command(name = "prvchannel", description = "Makes a temprory private channel.")
    @app_commands.describe(time = "Time of the channel before it gets deleted.", channel_name = "Channel's name.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def prvchannel(self, interaction: discord.Interaction, time: str, channel_name: str):
        guild = interaction.guild
        category = discord.utils.get(interaction.guild.categories)
        overwrites = {
                        guild.default_role: discord.PermissionOverwrite(read_messages = False),
                        guild.me: discord.PermissionOverwrite(read_messages = True)
                    }
        if time:
            get_time = {
            "s": 1, "m": 60, "h": 3600, "d": 86400,
            "w": 604800, "mo": 2592000, "y": 31104000 }
            timer = time
            a = time[-1]
            b = get_time.get(a)
            c = time[:-1]
            try: int(c)
            except: return await interaction.response.send_message("> Type time and time unit [s,m,h,d,w,mo,y] correctly.", ephemeral = True)
            try: sleep = int(b) * int(c)
            except: return await interaction.response.send_message("> Type time and time unit [s,m,h,d,w,mo,y] correctly.", ephemeral = True)
        channel = await guild.create_text_channel(name = channel_name , overwrites = overwrites , category = category)
        emb = discord.Embed(title = "Channel Created! ✅",
                            description = f"> Private Channel **{channel_name}** has been created for **{timer}**",
                            color = 0x2F3136)
        await interaction.response.send_message(embed = emb)
        await asyncio.sleep(int(sleep))
        await channel.delete()
        emb = discord.Embed(title = "Channel Deleted!", description = f"> Private Channel **{channel_name}** has been deleted after **{timer}**", color = 0x2F3136)
        await interaction.response.send_message(embed = emb)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SettingsOther(bot))
