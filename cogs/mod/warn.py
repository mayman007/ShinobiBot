import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite


# ModWarn Class
class ModWarn(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("ModWarn is online.")

    #warn commands
    @app_commands.command(name = "warn", description = "Warn a member.")
    @app_commands.describe(member = "Member to warn.", reason = "Reason of warn.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(moderate_members = True)
    async def warn(self, interaction: discord.Interaction, member : discord.Member, reason: str = None):
        #check author role
        if interaction.user.top_role <= member.top_role:
            return await interaction.response.send_message(f"Your role must be higher than {member.mention}.", ephemeral = True)
        #check bot role
        if interaction.guild.me.top_role <= member.top_role:
            return await interaction.response.send_message(f"My role must be higher than {member.mention}.", ephemeral = True)
        if reason == None: reason = ""
        else: reason = f"\nReason: {reason}"
        # add warn to database
        async with aiosqlite.connect("db/warnings.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS warnings (warns INTEGER, member INTEGER, guild ID)")
                await cursor.execute("SELECT warns FROM warnings WHERE member = ? AND guild = ?", (member.id, interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE warnings SET warns = ? WHERE member = ? AND guild = ?", (data[0] + 1, member.id, interaction.guild.id,))
                else: await cursor.execute("INSERT INTO warnings (warns, member, guild) VALUES (?, ?, ?)", (1, member.id, interaction.guild.id,))
            await db.commit()
        warn_embed = discord.Embed(title = "⚠️ ┃ Warn!", description = f"{member.mention} has been warned by {interaction.user.mention}{reason}", colour = discord.Colour.red())
        await interaction.response.send_message(embed = warn_embed)

    #Multi-Warn
    @app_commands.command(name = "multiwarn", description = "Warns multiple members. (maximum 5 members.)")
    @app_commands.describe(member1 = "First Member to warn.", member2 = "Second Member to warn.", member3 = "Third Member to warn.", member4 = "Fourth Member to warn.", reason = "Reason of warn.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(moderate_members = True)
    async def multiwarn(self, interaction: discord.Interaction, member1: discord.Member, member2: discord.Member, member3: discord.Member = None, member4: discord.Member = None, reason: str = None):
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
                return await interaction.response.send_message(f"Your role must be higher than {member.mention}.", ephemeral = True)
            #check bot role
            if interaction.guild.me.top_role <= member.top_role:
                return await interaction.response.send_message(f"My role must be higher than {member.mention}.", ephemeral = True)
        #add warning to database
        for member in members:
            async with aiosqlite.connect("db/warnings.db") as db: # Open the db
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS warnings (warns INTEGER, member INTEGER, guild ID)")
                    await cursor.execute("SELECT warns FROM warnings WHERE member = ? AND guild = ?", (member.id, interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data: await cursor.execute("UPDATE warnings SET warns = ? WHERE member = ? AND guild = ?", (data[0]+1, member.id, interaction.guild.id,))
                    else: await cursor.execute("INSERT INTO warnings (warns, member, guild) VALUES (?, ?, ?)", (1, member.id, interaction.guild.id,))
                await db.commit()
        if reason == None: reason = ""
        else: reason = f"\nReason: {reason}"
        warn_embed = discord.Embed(title = "⚠️ ┃ Multi-Warn! ┃ ⚠️", description = f"{memberstext} have been warned by {interaction.user.mention}{reason}", colour = discord.Colour.red())
        await interaction.followup.send(embed = warn_embed)

    #unwarn commands
    @app_commands.command(name = "unwarn", description = "Unwarn a member.")
    @app_commands.describe(member = "Member to unwarn.", amount = "Number of warnings to remove (default is 1 warn).")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(moderate_members = True)
    async def unwarn(self, interaction: discord.Interaction, member: discord.Member, amount: int = None):
        #check if member = author
        if interaction.user == member:
            return await interaction.response.send_message("> You can not unwarn yourself!", ephemeral = True)
        #check author role
        if interaction.user.top_role <= member.top_role:
            return await interaction.response.send_message(f"> Your role must be higher than {member.mention}!", ephemeral = True)
        #check bot role
        if interaction.guild.me.top_role <= member.top_role:
            return await interaction.response.send_message(f"> My role must be higher than {member.mention}!", ephemeral = True)
        if amount == None: amount = 1
        #remove warning from database
        async with aiosqlite.connect("db/warnings.db") as db: # Open the db
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS warnings (warns INTEGER, member INTEGER, guild ID)")
                    await cursor.execute("SELECT warns FROM warnings WHERE member = ? AND guild = ?", (member.id, interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data:
                        warns = data[0]
                        if warns - amount < 0: return await interaction.response.send_message(f"{member.mention} has **{warns}** warnings only.", ephemeral = True)
                        elif warns - amount == 0: await cursor.execute("DELETE FROM warnings WHERE member = ? AND guild = ?", (member.id, interaction.guild.id,))
                        else: await cursor.execute("UPDATE warnings SET warns = ? WHERE member = ? AND guild = ?", (warns - amount, member.id, interaction.guild.id,))
                    else: return await interaction.response.send_message(f"{member.mention} doesn't have any warnings.", ephemeral = True)
                await db.commit()
                warn_embed = discord.Embed(title = "✅ ┃ Unwarn!", description = f"**{amount}** warnings has been removed from {member.mention} by {interaction.user.mention}", colour = discord.Colour.green())
                await interaction.response.send_message(embed = warn_embed)

    #warnings list commands
    @app_commands.command(name = "warnings", description = "Get list of warnings for the user.")
    @app_commands.describe(member = "Member to view their warnings.")
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(moderate_members = True)
    async def warnings(self, interaction: discord.Interaction, member: discord.Member):
        async with aiosqlite.connect("db/warnings.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS warnings (warns INTEGER, member INTEGER, guild ID)")
                await cursor.execute("SELECT warns FROM warnings WHERE member = ? AND guild = ?", (member.id, interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await interaction.response.send_message(f"{member.mention} has **{data[0]}** warnings.")
                else: await interaction.response.send_message(f"{member.mention} doesn't have any warnings.", ephemeral = True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ModWarn(bot))