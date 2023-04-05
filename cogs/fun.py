import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio
import praw
import aiohttp
from bs4 import BeautifulSoup
import os

# Next button on meme button
class nextMeme(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Next Meme", style = discord.ButtonStyle.green)
    async def next_meme(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author: return await interaction.response.send_message("> This is not your meme!", ephemeral = True)
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

# Fun Class
class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun is online.")

    # geekjoke
    @app_commands.command(name = "geekjoke", description = "Get a random geek joke.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def geekjoke(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://geek-jokes.sameerkumar.website/api?format=json") as response:
                data = await response.json()
                joke = data["joke"]
            await interaction.response.send_message(joke)

    # dadjoke
    @app_commands.command(name = "dadjoke", description = "Get a random dad joke.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def dadjoke(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://icanhazdadjoke.com/slack") as response:
                data = await response.json()
                joke = data["attachments"][0]["text"]
            await interaction.response.send_message(joke)

    # dog api
    @app_commands.command(name = "dog", description = "Get a random dog image.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def dog(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            while True:
                async with session.get("https://random.dog/woof.json") as response:
                    data = await response.json()
                    dog_url = data["url"]
                    if ".mp4" in dog_url: continue
                    em = discord.Embed(colour = 0x2F3136)
                    em.set_image(url = dog_url)
                await interaction.response.send_message(embed = em)
                break

    # cat api
    @app_commands.command(name = "cat", description = "Get a random cat image.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def cat(self, interaction: discord.Interaction):
        cat_tags = ["cute", "says/hello", "cute/says/hello"]
        tag = random.choice(cat_tags)
        em = discord.Embed(colour = 0x2F3136)
        em.set_image(url = f"https://cataas.com/cat/{tag}")
        await interaction.response.send_message(embed = em)

    #wyr command
    @app_commands.command(name = "wyr", description = "Would you rather...")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def wyr(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get("http://either.io/") as r:
                text = await r.text()
        soup = BeautifulSoup(text, "lxml")
        l = []
        for choice in soup.find_all("span", {"class":"option-text"}):
            l.append(choice.text)
        e = discord.Embed(colour = 0x2F3136)
        e.set_author(name = "Would you rather...", url = "http://either.io/", icon_url = self.bot.user.avatar.url)
        e.add_field(name = "EITHER...", value = f":regional_indicator_a: {l[0]}", inline = False)
        e.add_field(name = "OR...", value = f":regional_indicator_b: {l[1]}")
        msg = await interaction.channel.send(embed = e)
        await msg.add_reaction("🇦")
        await msg.add_reaction("🇧")
        await interaction.response.send_message("Embed sent.", ephemeral = True)

    #emojify
    @app_commands.command(name = "emojify", description = "Convert your words to emojis!")
    @app_commands.describe(text = "Text you want to transform into emojis.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def emojify(self, interaction: discord.Interaction, text: str):
        emojis = []
        for s in text.lower():
            if s.isdecimal():
                num2emo = {"0":"zero" , "1":"one" , "2":"two" , "3":"three" , "4":"four" ,
                          "5":"five" , "6":"six" , "7":"seven" , "8":"eight" , "9":"nine"}
                emojis.append(f":{num2emo.get(s)}:")
            elif s.isalpha():
                emojis.append(f":regional_indicator_{s}:")
            else:
                emojis.append(s)
        await interaction.response.send_message(" ".join(emojis))

    #rate command
    @app_commands.command(name = "rate", description = "Rates.")
    @app_commands.describe(someone = "Someone to rate.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def rate(self, interaction: discord.Interaction, someone: discord.Member = None):
        if someone == None: text = "Your"
        else: text = someone.mention
        # async with interaction.typing(): await asyncio.sleep(5)
        thing = ["handsome" , "beauty" , "luck" , "success" , "happiness" , "sadness" , "intelligence" , "cringe" , "gay"]
        emoji = ["🙂" , "😆" , "🤣" , "😉" , "😘" , "😏" , "😶" , "😱" , "🤯" , "🥳" , "🤥" , "😳" , "😮" , "😯" , "<:kek:959474451584524308>"]
        await interaction.response.send_message(f">>> {text} **{random.choice(thing)}** rate is **{random.randint(0, 100)}%!** {random.choice(emoji)}")

    #meme reddit
    @app_commands.command(name = "meme", description = "Memes.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
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
        global author
        author = interaction.user
        view=nextMeme()
        await interaction.response.send_message(embed = em, view = view)

    #choose command
    @app_commands.command(name = "choose", description = "Chooses. (maximum 5 choices.)")
    @app_commands.describe(choice1 = "Choice 1.", choice2 = "Choice 2.", choice3 = "Choice 3.", choice4 = "Choice 4.", choice5 = "Choice 5.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def choose(self, interaction: discord.Interaction, choice1: str, choice2: str, choice3: str = None, choice4: str = None, choice5: str = None):
        if choice3 == None:
            opt = [choice1,choice2]
            optext = f"{choice1} and {choice2}"
        elif choice4 == None:
            opt = [choice1,choice2,choice3]
            optext = f"{choice1}, {choice2} and {choice3}"
        elif choice5 == None:
            opt = [choice1,choice2,choice3,choice4]
            optext = f"{choice1}, {choice2}, {choice3} and {choice4}"
        else:
            opt = [choice1, choice2, choice3, choice4, choice5]
            optext = f"{choice1}, {choice2}, {choice3}, {choice4} and {choice5}"
        await interaction.response.send_message(f"Choosing from: {optext}.")
        await asyncio.sleep(0.5)
        await interaction.edit_original_response(content = f"Choosing from: {optext}..")
        await asyncio.sleep(0.5)
        await interaction.edit_original_response(content = f"Choosing from: {optext}...")
        await asyncio.sleep(0.5)
        await interaction.edit_original_response(content = f"Choosing from: {optext}.")
        await asyncio.sleep(0.5)
        await interaction.edit_original_response(content = f"Choosing from: {optext}..")
        await asyncio.sleep(0.5)
        await interaction.edit_original_response(content = f"Choosing from: {optext}...")
        await asyncio.sleep(0.5)
        await interaction.followup.send(content = f"{random.choice(opt)}")

    #coinflip
    @app_commands.command(name = "coinflip", description = "Flip a coin.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def coinflip(self, interaction: discord.Interaction):
        """ Coinflip! """
        coinsides = ["Heads", "Tails"]
        await interaction.response.send_message(f"**{interaction.user.name}** flipped a coin and got **{random.choice(coinsides)}**!")

    #f
    @app_commands.command(name = "f", description = "Press f to pay respect.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def f(self, interaction: discord.Interaction, someone_or_something: str = None):
        """ Press F to pay respect """
        hearts = ["❤", "💛", "💚", "💙", "💜"]
        reason = f"for **{someone_or_something}** " if someone_or_something else ""
        await interaction.response.send_message(f"**{interaction.user.name}** has paid their respect {reason}{random.choice(hearts)}")

    #reverse
    @app_commands.command(name = "reverse", description = "Reverses your words.")
    @app_commands.describe(your_words = "Words to reverse.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def reverse(self, interaction: discord.Interaction, your_words: str):
        t_rev = your_words[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await interaction.response.send_message(f"🔁 {t_rev}")

    #slot
    @app_commands.command(name = "slot", description = "A slot game.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def slot(self, interaction: discord.Interaction):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a, b, c = [random.choice(emojis) for g in range(3)]
        slotmachine = f"**[ {a} {b} {c} ]\n{interaction.user.name}**,"
        if (a == b == c): await interaction.response.send_message(f">>> {slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c): await interaction.response.send_message(f">>> {slotmachine} 2 in a row, you won! 🎉")
        else: await interaction.response.send_message(f">>> {slotmachine} No match, you lost 😢")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))