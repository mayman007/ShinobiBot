import discord
from discord import app_commands
from discord.ext import commands
import random
import praw
import os


# Next button on meme button
class nextMeme(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Next Meme", style = discord.ButtonStyle.green)
    async def next_meme(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("> This is not your meme!", ephemeral = True)
        reddit = praw.Reddit(
                    client_id = os.getenv("REDDIT_CLIENT_ID"),
                    client_secret = os.getenv("REDDIT_CLIENT_SECRET"),
                    user_agent = "ShinobiBot",
                    check_for_async = False
                    )
        subreddit = reddit.subreddit("Animemes")
        all_subs = []
        hot = subreddit.hot(limit = 50)
        for submission in hot:
            all_subs.append(submission)
            random_sub = random.choice(all_subs)
            name = random_sub.title
            url = random_sub.url
            if ".gif" in url or ".mp4" in url: continue
            em = discord.Embed(title = name)
            em.set_image(url = url)
        await interaction.message.edit(embed = em)
        await interaction.response.defer()

# Meme Class
class Meme(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Meme is online.")

    #meme reddit
    @app_commands.command(name = "meme", description = "Memes.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def meme(self, interaction: discord.Interaction):
        reddit = praw.Reddit(
                    client_id = os.getenv("REDDIT_CLIENT_ID"),
                    client_secret = os.getenv("REDDIT_CLIENT_SECRET"),
                    user_agent = "ShinobiBot",
                    check_for_async = False
                    )
        subreddit = reddit.subreddit("Animemes")
        all_subs = []
        hot = subreddit.hot(limit=50)
        for submission in hot:
            all_subs.append(submission)
            random_sub = random.choice(all_subs)
            name = random_sub.title
            url = random_sub.url
            if ".gif" in url or ".mp4" in url: continue
            em = discord.Embed(title = name, colour = 0x2F3136)
            em.set_image(url = url)
        view=nextMeme()
        await interaction.response.send_message(embed = em, view = view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Meme(bot))