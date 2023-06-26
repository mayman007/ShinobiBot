import discord
from discord import app_commands
from discord.ext import commands


class Dropdown(discord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label = "Index", description = "Shows the main help page.", emoji = "👋"),
            discord.SelectOption(label = "Tickets", description = "Shows tickets commands", emoji = "📩"),
            discord.SelectOption(label = "Anti-Spam", description = "Shows anti-spam commands", emoji = "⛔"),
            discord.SelectOption(label = "Logging", description = "Shows logging commands", emoji = "📝"),
            discord.SelectOption(label = "Moderation", description = "Shows moderation commands.", emoji = "⚒️"),
            discord.SelectOption(label = "Artificial Intelligence", description = "Shows artificial intelligence commands.", emoji = "🤖"),
            discord.SelectOption(label = "Games", description = "Shows games commands", emoji = "🎮"),
            discord.SelectOption(label = "Utility", description = "Shows utility commands.", emoji = "🔧"),
            discord.SelectOption(label = "Channels Settings", description = "Shows channels settings commands", emoji = "⚙️"),
            discord.SelectOption(label = "Fun", description = "Shows fun commands", emoji = "🎉"),
            discord.SelectOption(label = "Server Information", description = "Shows server information commands", emoji = "ℹ️")
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder = "Select category.", min_values = 1, max_values = 1, options = options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.

        # Check user
        if interaction.user != author: return await interaction.response.send_message("Use your own help command.", ephemeral = True)

        # Index page
        if self.values[0] == "Index":
            em = discord.Embed(title = "**Shinobi Bot Help**",
                           description = "Hello! Welcome to the help page.\n\nUse </feedback:1027218853127794780> to send your feedback directly to the developers.\nUse `/help <category> <command>` for more info on a command.\nUse the dropdown menu below to select a category.\n\n",
                           color = 0x2F3136)
            em.add_field(name = "**Who are you?**", value = "I'm a bot developed by @shinobi7k. I'm a multipurpose bot than can do _almost_ anything. You can get more info using the dropdown menu below.\n\nI'm also open source. You can see my code on [GitHub](https://github.com/Shinobi7k/ShinobiBot)!")
            em.add_field(name = "**Features**", value = "- Advanced Ticket System\n- Anti-Spam System\n- Logging System\n- Suggestions\n- Moderation\n- Games\n- Utility")
            await interaction.message.edit(embed = em)
            await interaction.response.defer()

        # Moderation page
        if self.values[0] == "Moderation":
            embed = discord.Embed(title = "**Moderation**", description = "Moderation commands that helps in moderating the server", color = 0x2F3136)
            embed.add_field(name = "**Commands**", value = "> </kick:1017544215586164819> , </multikick:1025865754790350848> , </mute:1017544215586164823> , </multimute:1025855722308784128> , </unmute:1017544215586164824> , </warn:1020339992851140679> , </multiwarn:1025860023001284608> , </unwarn:1020347964528541726> , </warnings:1020339992851140680> , </ban:1017544215586164820> , </multiban:1025871989627424828> , </unban:1022308950579880046> , </unbanall:1024382428359434260> , </timeout:1020114423026810901> , </multitimeout:1025863838001795133> , </clear:1017544215586164817> , </addrole:1081342436112081019> , </removerole:1081342436112081020>")
            embed.set_footer(text = "Use /help moderation <command> for information on a command.")
            await interaction.message.edit(embed = embed)
            await interaction.response.defer()

        # Utility page
        elif self.values[0] == "Utility":
            embed = discord.Embed(title = "**Utility**", description = "Utility commands contains varies types of commands to use", color = 0x2F3136)
            embed.add_field(name = "**Commands**", value = "> </poll:1093371959825408075> , </ping:1093371959628283945> , </serverlink:1093371959825408072> , </invite:1093371959825408073> , </vote:1093371959825408074> , </timer:1093371959825408071> , </tax:1093371959825408070> , </nick:1093371959628283953> , </embed:1093371959628283952> , </calculator:1093371959628283951> , </giveaway:1093371959628283954> , </translate:1093371959628283950> , </search:1093371959628283949> , </quote:1093371959628283948> , </affirmation:1093371959628283947> , </advice:1093371959628283946>")
            embed.set_footer(text = "Use /help utility <command> for information on a command.")
            await interaction.message.edit(embed = embed)
            await interaction.response.defer()

        # Fun page
        elif self.values[0] == "Fun":
            embed = discord.Embed(title = "**Fun**", description = "Fun commands to have fun", color = 0x2F3136)
            embed.add_field(name = "**Commands**", value = "> </meme:1017544215871373393> , </rate:1017544215871373392> , </f:1017544215871373396> , </coinflip:1017544215871373395> , </reverse:1017544215871373397> , </slot:1017544215871373398> , </choose:1017544215871373394> , </emojify:1020114423026810904> , </wyr:1021052870231085106> , </cat:1021770303979917436> , </dog:1032658220730294313> , </dadjoke:1081342436292427877> , </geekjoke:1081342436112081028>")
            embed.set_footer(text = "Use /help fun <command> for information on a command.")
            await interaction.message.edit(embed = embed)
            await interaction.response.defer()

        # Logs page
        elif self.values[0] == "Logging":
            embed = discord.Embed(title = "**Logging**", description = "Log everything in your server", color = 0x2F3136)
            embed.add_field(name = "**Commands**", value = "> </log joins:1081342436292427878> , </log leaves:1081342436292427878> , </log message deletes:1081342436292427878> , </log message edits:1081342436292427878> , </log channel create:1081342436292427878> , </log channel delete:1081342436292427878> , </log channel updates:1081342436292427878> , </log role create:1081342436292427878> , </log role delete:1081342436292427878> , </log role updates:1081342436292427878> , </log role given:1081342436292427878> , </log role remove:1081342436292427878> , </log member ban:1081342436292427878> , </log member unban:1081342436292427878> , </log member timeout:1081342436292427878> , </log member nickname:1081342436292427878> , </log server_updates:1081342436292427878> , </log show_settings:1081342436292427878>")
            embed.set_footer(text = "Use /help logs <command> for information on a command.")
            await interaction.message.edit(embed = embed)
            await interaction.response.defer()

        # Tickets page
        elif self.values[0] == "Tickets":
            embed = discord.Embed(title = "**Tickets**", description = "Create and moderate tickets", color = 0x2F3136)
            embed.add_field(name = "**Commands**", value = "> </ticket launch:1020114423026810906> , </ticket close:1020114423026810906> , </ticket add:1020114423026810906> , </ticket remove:1020114423026810906> , </ticket role:1020114423026810906> , </ticket transcript:1020114423026810906>")
            embed.set_footer(text = "Use /help tickets <command> for information on a command.")
            await interaction.message.edit(embed = embed)
            await interaction.response.defer()

        # Anti-Spam page
        elif self.values[0] == "Anti-Spam":
            embed = discord.Embed(title = "**Anti-Spam**", description = "Create an Anti-Spam system", color = 0x2F3136)
            embed.add_field(name = "**Commands**", value = "> </antispam enable:1081342436292427879> , </antispam disable:1081342436292427879> , </antispam punishment:1081342436292427879> , </antispam whitelist:1081342436292427879>")
            embed.set_footer(text = "Use /help antispam <command> for information on a command.")
            await interaction.message.edit(embed = embed)
            await interaction.response.defer()

        # Artificial Intelligence page
        elif self.values[0] == "Artificial Intelligence":
            embed = discord.Embed(title = "**Artificial Intelligence**", description = "Use famous AI tools", color = 0x2F3136)
            embed.add_field(name = "**Commands**", value = "> </chatbot:1112553506457526353> , </bard:1090416058382438440> , </bing ask:1088508793110933524> , </bing image_creator:1088508793110933524> , </dalle:1089010855695368253> , </imagine:1122943777326256413>")
            embed.set_footer(text = "Use /help artificial-intelligence <command> for information on a command.")
            await interaction.message.edit(embed = embed)
            await interaction.response.defer()

        # Settings page
        elif self.values[0] == "Channels Settings":
            embed = discord.Embed(title = "**Channels Settings**", description = "Easily control channels settings", color = 0x2F3136)
            embed.add_field(name = "**Commands**", value = "> </lock:1017544215661649935> , </lockall:1025405253966897263> , </unlock:1017544215661649936> , </unlockall:1025414043751690381> , </hide:1017544215661649933> , </hideall:1025419518358597652> , </show:1017544215661649934> , </showall:1025419518358597653> , </suggestions:1029113875783766157> , </prvchannel:1017544215586164822>")
            embed.set_footer(text = "Use /help settings <command> for information on a command.")
            await interaction.message.edit(embed = embed)
            await interaction.response.defer()

        # Games page
        elif self.values[0] == "Games":
            embed = discord.Embed(title = "**Games**", description = "Challange others in games", color = 0x2F3136)
            embed.add_field(name = "**Commands**", value = "> </connect4:1017544216089468943> , </tictactoe:1020114423026810905> , </rps:1020114423169425429>")
            embed.set_footer(text = "Use /help games <command> for information on a command.")
            await interaction.message.edit(embed = embed)
            await interaction.response.defer()

        # Serverinfo page
        elif self.values[0] == "Server Information":
            embed = discord.Embed(title = "**Server Information**", description = "Know more about your server and members", color = 0x2F3136)
            embed.add_field(name = "**Commands**", value = "> </server:1017544215871373400> , </owner:1017544215871373401> , </id:1017544216089468938> , </members:1017544216089468939> , </channels:1081342436112081026> , </user:1017544216089468942> , </icon:1017544216089468941> , </roles:1017544215871373399> , </avatar:1017544215762317326> , </banner:1017544215661649939>")
            embed.set_footer(text = "Use /help serverinformation <command> for information on a command.")
            await interaction.message.edit(embed = embed)
            await interaction.response.defer()

#dropdown class
class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown())

#help class
class Help(commands.GroupCog, name = "help"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Help is online.")

    #help start
    @app_commands.command(name = "start", description = "Shinobi Bot's help command.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def sbhelp(self, interaction: discord.Interaction):
        em = discord.Embed(title = "**Shinobi Bot Help**",
                           description = "Hello! Welcome to the help page.\n\nUse </feedback:1027218853127794780> to send your feedback directly to the developers.\nUse `/help <category> <command>` for more info on a command.\nUse the dropdown menu below to select a category.\n\n",
                           color = 0x2F3136)
        em.add_field(name = "**Who are you?**", value = "I'm a bot developed by @shinobi7k. I'm a multipurpose bot than can do _almost_ anything. You can get more info using the dropdown menu below.\n\nI'm also open source. You can see my code on [GitHub](https://github.com/Shinobi7k/ShinobiBot)!")
        em.add_field(name = "**Features**", value = "- Advanced Ticket System\n- Anti-Spam System\n- Logging System\n- Suggestions\n- Moderation\n- Games\n- Utility")
        global author
        author = interaction.user
        view = DropdownView()
        view.add_item(discord.ui.Button(label = "Invite Shinobi Bot", style = discord.ButtonStyle.link, url = "https://discord.com/oauth2/authorize?client_id=855437723166703616&permissions=8&scope=bot%20applications.commands"))
        view.add_item(discord.ui.Button(label = "Support Server", style = discord.ButtonStyle.link, url = "https://discord.gg/YScaCDY7PN"))
        view.add_item(discord.ui.Button(label = "Vote For Us", style = discord.ButtonStyle.link, url = "https://top.gg/bot/855437723166703616", emoji = "💌"))
        await interaction.response.send_message(embed = em, view = view)

#=====================================================================================================================

    #moderation commands help
    @app_commands.command(name = "moderation", description = "Shinobi Bot's moderation catogery help.")
    @app_commands.describe(command = "Choose a command to get info about it.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.choices(command = [
        app_commands.Choice(name = "mute", value = "mute"),
        app_commands.Choice(name = "multimute", value = "multimute"),
        app_commands.Choice(name = "unmute", value = "unmute"),
        app_commands.Choice(name = "jail", value = "jail"),
        app_commands.Choice(name = "multijail", value = "multijail"),
        app_commands.Choice(name = "unjail", value = "unjail"),
        app_commands.Choice(name = "kick", value = "kick"),
        app_commands.Choice(name = "multikick", value = "multikick"),
        app_commands.Choice(name = "ban", value = "ban"),
        app_commands.Choice(name = "multiban", value = "multiban"),
        app_commands.Choice(name = "unban", value = "unban"),
        app_commands.Choice(name = "unbanall", value = "unbanall"),
        app_commands.Choice(name = "timeout", value = "timeout"),
        app_commands.Choice(name = "multitimeout", value = "multitimeout"),
        app_commands.Choice(name = "clear", value = "clear"),
        app_commands.Choice(name = "addrole", value = "addrole"),
        app_commands.Choice(name = "removerole", value = "removerole"),
        app_commands.Choice(name = "warn", value = "warn"),
        app_commands.Choice(name = "multiwarn", value = "multiwarn"),
        app_commands.Choice(name = "unwarn", value = "unwarn"),
        app_commands.Choice(name = "warnings", value = "warnings")
        ])
    async def moderation(self, interaction: discord.Interaction, command: app_commands.Choice[str]):
        if command.value == "mute":
            em = discord.Embed(title = "__**Mute**__", description = "Mutes a member.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> mute <member> [time] [reason]")
            em.add_field(name = "**Example:**", value = "> `/mute @member 2h breaking the rules`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        if command.value == "multimute":
            em = discord.Embed(title = "__**Multi-Mute**__", description = "Mutes multiple members. (maximum 5 members.)", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> multimute <member1> <member2> [member3] [member4] [member5] [time] [reason]")
            em.add_field(name = "**Example:**", value = "> `/multimute @member1 @member2 @member3 @member4 @member5 2h breaking the rules`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "unmute":
            em = discord.Embed(title = "__**Unmute**__", description = "Unmutes a member.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> unmute <member>")
            em.add_field(name = "**Example:**", value = "> `/unmute @member`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "jail":
            em = discord.Embed(title = "__**Jail**__", description = "Jails a member.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> jail <member> [time] [reason]")
            em.add_field(name = "**Example:**", value = "> `/jail @member 2h breaking the rules`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "multijail":
            em = discord.Embed(title = "__**Multi-Jail**__", description = "Jails multiple members. (maximum 3 members.)", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> multijail <member1> <member2> [member3] [time] [reason]")
            em.add_field(name = "**Example:**", value = "> `/multijail @member1 @member2 @member3 2h breaking the rules`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "unjail":
            em = discord.Embed(title = "__**Unjail**__", description = "Unjail a member.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> Unjail <member>")
            em.add_field(name = "**Example:**", value = "> `/Unjail @member`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "kick":
            em = discord.Embed(title = "__**Kick**__", description = "Kicks a member from the server.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> kick <member> [reason]")
            em.add_field(name = "**Example:**", value = "> `/kick @member breaking the rules`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "multikick":
            em = discord.Embed(title = "__**Multi-Kick**__", description = "Kicks multiple members from the server. (maximum 4 members.)", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> multikick <member1> <member2> [member3] [member4] [reason]")
            em.add_field(name = "**Example:**", value = "> `/multikick @member1 @member2 @member3 @member4 breaking the rules`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "ban":
            em = discord.Embed(title = "__**Ban**__", description = "Bans a member from the server.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> ban <member> [reason]")
            em.add_field(name = "**Example:**", value = "> `/ban @member breaking the rules`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "multiban":
            em = discord.Embed(title = "__**Multi-Ban**__", description = "Bans multiple members from the server. (maximum 4 members.)", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> multiban <member1> <member2> [member3] [member4] [reason]")
            em.add_field(name = "**Example:**", value = "> `/multiban @member1 @member2 @member3 @member4 breaking the rules`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "unban":
            em = discord.Embed(title = "__**Unban**__", description = "Unbans a user.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> unban <user>")
            em.add_field(name = "**Example:**", value = "> `/unban <user's id>`")
            em.add_field(name = "**Note:**", value = "> User's ID must be given.")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "unbanall":
            em = discord.Embed(title = "__**Unbanall**__", description = "Unbans all banned users.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> unbanall")
            em.add_field(name = "**Example:**", value = "> `/unbanall`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "timeout":
            em = discord.Embed(title = "__**Timeout**__", description = "Timeouts a member.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> timeout <member> <time> [reason]")
            em.add_field(name = "**Example:**", value = "> `/timeout @member 2h bad mood`")
            em.add_field(name = "**Note:**", value = "> A time must be given.")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "multitimeout":
            em = discord.Embed(title = "__**Multi-Timeout**__", description = "Timeouts multiple members. (maximum 4 members.)", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> multitimeout <time> <member1> <member2> [member3] [member4] [reason]")
            em.add_field(name = "**Example:**", value = "> `/multitimeout 2h @member1 @member2 @member3 @member4 breaking the rules`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "clear":
            em = discord.Embed(title = "__**Clear**__", description = "Clears messages.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> clear [amount]")
            em.add_field(name = "**Example:**", value = "> clear 5`")
            em.add_field(name = "**Note:**", value = "> Deafult amount is 1.")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "addrole":
            em = discord.Embed(title = "__**Add Role**__", description = "Adds a role to a member.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> addrole <member> <role>")
            em.add_field(name = "**Example:**", value = "> `/addrole @member @Admin`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "removerole":
            em = discord.Embed(title = "__**Remove Role**__", description = "Removes a role from a member.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> removerole <member> <role>")
            em.add_field(name = "**Example:**", value = "> `/removerole @member @Admin`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "warn":
            em = discord.Embed(title = "__**Warn**__", description = "Warns a member.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> warn <member> [reason]")
            em.add_field(name = "**Example:**", value = "> `/warn @member abusing the rules`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "multiwarn":
            em = discord.Embed(title = "__**Multi-Warn**__", description = "Warns multiple members. (maximum 4 members.)", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> multiwarn <member1> <member2> [member3] [member4] [reason]")
            em.add_field(name = "**Example:**", value = "> `/multiwarn @member1 @member2 @member3 @member4 breaking the rules`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "unwarn":
            em = discord.Embed(title = "__**Unwarn**__", description = "Unwarns a member.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> unwarn <member>")
            em.add_field(name = "**Example:**", value = "> `/unwarn @member`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "warnings":
            em = discord.Embed(title = "__**Warnings**__", description = "Gets a list of warnings for a member.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> warnings <member>")
            em.add_field(name = "**Example:**", value = "> `/warnings @member`")
            em.add_field(name = "**Note:**", value = "> Warnings for users are synced across all servers.")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)

    #utility commands help
    @app_commands.command(name = "utility", description = "Shinobi Bot's utility catogery help.")
    @app_commands.describe(command = "Choose a command to get info about it.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.choices(command = [
        app_commands.Choice(name = "poll", value = "poll"),
        app_commands.Choice(name = "invite", value = "invite"),
        app_commands.Choice(name = "serverlink", value = "serverlink"),
        app_commands.Choice(name = "vote", value = "vote"),
        app_commands.Choice(name = "calculator", value = "calculator"),
        app_commands.Choice(name = "tax", value = "tax"),
        app_commands.Choice(name = "nick", value = "nick"),
        app_commands.Choice(name = "search", value = "search"),
        app_commands.Choice(name = "translate", value = "translate"),
        app_commands.Choice(name = "giveaway", value = "giveaway"),
        app_commands.Choice(name = "embed", value = "embed"),
        app_commands.Choice(name = "timer", value = "timer"),
        app_commands.Choice(name = "ping", value = "ping"),
        app_commands.Choice(name = "quote", value = "quote"),
        app_commands.Choice(name = "affirmation", value = "affirmation"),
        app_commands.Choice(name = "advice", value = "advice"),
        app_commands.Choice(name = "chatgpt", value = "chatgpt"),
        app_commands.Choice(name = "bing", value = "bing"),
        app_commands.Choice(name = "dalle", value = "dalle"),
        app_commands.Choice(name = "bard", value = "bard"),
        ])
    async def utility(self, interaction: discord.Interaction, command: app_commands.Choice[str]):
        if command.value == "poll":
            em = discord.Embed(title = "__**Poll**__", description = "Makes a poll.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> poll <content>")
            em.add_field(name = "**Example:**", value = "> `/poll about the new role...`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "invite":
            em = discord.Embed(title = "__**Invite**__", description = "Sends Shinobi Bot's invite link.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> invite")
            em.add_field(name = "**Example:**", value = "> `/invite`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "serverlink":
            em = discord.Embed(title = "__**Server link**__", description = "Creates an instant invite link for the server.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> serverlink")
            em.add_field(name = "**Example:**", value = "> `/serverlink`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "vote":
            em = discord.Embed(title = "__**Vote**__", description = "Sends Shinobi Bot's vote link.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> vote")
            em.add_field(name = "**Example:**", value = "> `/vote`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "calculator":
            em = discord.Embed(title = "__**Calculator**__", description = "Calculates for you.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> calculator <first number> <operator> <second number>")
            em.add_field(name = "**Example:**", value = "> `/calculator 20 + 15`")
            em.add_field(name = "**Note:**", value = "> Make sure to put a space between the numbers and the operator.")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "tax":
            em = discord.Embed(title = "__**Tax**__", description = "Calculates ProBot tax.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> tax <amount>")
            em.add_field(name = "**Example:**", value = "> `/tax 10000`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "nick":
            em = discord.Embed(title = "__**Nick**__", description = "Changes member's nickname.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> nick <member> <nickname>")
            em.add_field(name = "**Example:**", value = "> `/nick @member tester`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "search":
            em = discord.Embed(title = "__**Search**__", description = "Searches wikipedia for you.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> search <your search>")
            em.add_field(name = "**Example:**", value = "> `/search python programming`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "translate":
            em = discord.Embed(title = "__**Translate**__", description = "A translator.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> translate <language to translate> <words>")
            em.add_field(name = "**Example:**", value = "> `/translate english prueba`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "giveaway":
            em = discord.Embed(title = "__**Giveaway**__", description = "Starts a giveaway.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> giveaway <time> <prize>")
            em.add_field(name = "**Example:**", value = "> `/giveaway 6h credits`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "embed":
            em = discord.Embed(title = "__**Embed**__", description = "Converts your text into an embed.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> embed <title> <description> [footer] [color] [thumbnail]")
            em.add_field(name = "**Example:**", value = "> `/embed title description footer red yes`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "timer":
            em = discord.Embed(title = "__**Timer**__", description = "Starts a timer.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> timer <timer>")
            em.add_field(name = "**Example:**", value = "> `/timer 20m`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "ping":
            em = discord.Embed(title = "__**Ping**__", description = "Shows bot's latency.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> ping")
            em.add_field(name = "**Example:**", value = "> `/ping`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "quote":
            em = discord.Embed(title = "__**Quote**__", description = "Gets a random quote from an anime.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> quote [title or character]")
            em.add_field(name = "**Example:**", value = "> `/quote sasuke`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "affirmation":
            em = discord.Embed(title = "__**Affirmation**__", description = "Gets a random affirmation.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> affirmation")
            em.add_field(name = "**Example:**", value = "> `/affirmation`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "advice":
            em = discord.Embed(title = "__**Advice**__", description = "Gets a random advice.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> advice")
            em.add_field(name = "**Example:**", value = "> `/advice`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "chatgpt":
            em = discord.Embed(title = "__**ChatGPT**__", description = "Ask ChatGPT.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> chatgpt <prompt>")
            em.add_field(name = "**Example:**", value = "> `/chatgpt hello`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "bing":
            em = discord.Embed(title = "__**Bing**__", description = "Ask Bing AI.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> bing <prompt>")
            em.add_field(name = "**Example:**", value = "> `/bing hello`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "dalle":
            em = discord.Embed(title = "__**Dall-E**__", description = "Create an image using Dall-E AI.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> dalle <prompt>")
            em.add_field(name = "**Example:**", value = "> `/dalle a white cat`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "bard":
            em = discord.Embed(title = "__**Bard**__", description = "Ask Bard.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> bard <prompt>")
            em.add_field(name = "**Example:**", value = "> `/bard hello`")
            em.set_footer(text = "<> means requird, [] means optional")

    # AI commands help
    @app_commands.command(name = "artificial-intelligence", description = "Shinobi Bot's artificial intelligence catogery help.")
    @app_commands.describe(command = "Choose a command to get info about it.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.choices(command = [
        app_commands.Choice(name = "chatbot", value = "chatbot"),
        app_commands.Choice(name = "bing ask", value = "bing ask"),
        app_commands.Choice(name = "bard", value = "bard"),
        app_commands.Choice(name = "dalle", value = "dalle"),
        app_commands.Choice(name = "imagine", value = "imagine"),
        app_commands.Choice(name = "bing image_creator", value = "bing image_creator")
        ])
    async def utility(self, interaction: discord.Interaction, command: app_commands.Choice[str]):
        if command.value == "chatbot":
            em = discord.Embed(title = "__**Chatbot**__", description = "Chat with powerful AI models.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> Chatbot <prompt> <model>")
            em.add_field(name = "**Example:**", value = "> `/chatgpt hello gpt-3.5-turbo`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "bing ask":
            em = discord.Embed(title = "__**Bing Ask**__", description = "Ask Bing AI.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> bing ask <prompt> [conversation_style]")
            em.add_field(name = "**Example:**", value = "> `/bing ask hello creative`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "bard":
            em = discord.Embed(title = "__**Bard**__", description = "Ask Bard.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> bard <prompt>")
            em.add_field(name = "**Example:**", value = "> `/bard hello`")
            em.set_footer(text = "<> means requird, [] means optional")
        elif command.value == "dalle":
            em = discord.Embed(title = "__**Dall-E**__", description = "Create an image using Dall-E AI.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> dalle <prompt> [number_of_images] [size]")
            em.add_field(name = "**Example:**", value = "> `/dalle a white cat 5 512x512`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "imagine":
            em = discord.Embed(title = "__**Imagine**__", description = "Create images using powerful Stable Diffusion models.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> imagine <prompt> <model> <style> <ratio> <negative> <cfg>")
            em.add_field(name = "**Example:**", value = "> `/imagine white cat Creative Cyberpunk 16x9`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "bing image_creator":
            em = discord.Embed(title = "__**Bing Image Creator**__", description = "Create an image using Bing Image Creator.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> bing image_creator <prompt>")
            em.add_field(name = "**Example:**", value = "> `/bing image_creator a white cow`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)

    #logs commands help
    @app_commands.command(name = "logs", description = "Shinobi Bot's logs catogery help.")
    @app_commands.describe(command = "Choose a command to get info about it.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.choices(command = [
        app_commands.Choice(name = "show_settings", value = "show_settings"),
        app_commands.Choice(name = "joins", value = "joins"),
        app_commands.Choice(name = "leaves", value = "leaves"),
        app_commands.Choice(name = "message deletes", value = "message_deletes"),
        app_commands.Choice(name = "message edits", value = "message_edits"),
        app_commands.Choice(name = "role create", value = "role create"),
        app_commands.Choice(name = "role delete", value = "role delete"),
        app_commands.Choice(name = "role updates", value = "role updates"),
        app_commands.Choice(name = "role given", value = "role given"),
        app_commands.Choice(name = "role remove", value = "role remove"),
        app_commands.Choice(name = "channel create", value = "channel create"),
        app_commands.Choice(name = "channel delete", value = "channel delete"),
        app_commands.Choice(name = "channel updates", value = "channel updates"),
        app_commands.Choice(name = "member ban", value = "member ban"),
        app_commands.Choice(name = "member unban", value = "member unban"),
        app_commands.Choice(name = "member timeout", value = "member timeout"),
        app_commands.Choice(name = "member nickname", value = "member nickname"),
        app_commands.Choice(name = "server_updates", value = "server_updates")
        ])
    async def logs(self, interaction: discord.Interaction, command: app_commands.Choice[str]):
        if command.value == "show_settings":
            em = discord.Embed(title = "__**Log Show Settings**__", description = "Show current settings for all logs commands.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> log show_settings")
            em.add_field(name = "**Example:**", value = "> `/log show_settings`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "joins":
            em = discord.Embed(title = "__**Log Joins**__", description = "Log members's joins and send them to a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> log joins <switch> <channel>")
            em.add_field(name = "**Example:**", value = "> `/log joins enable #channel`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "leaves":
            em = discord.Embed(title = "__**Log Leaves**__", description = "Log members's leaves and send them to a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> log leaves <switch> <channel>")
            em.add_field(name = "**Example:**", value = "> `/log leaves enable #channel`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "message_deletes":
            em = discord.Embed(title = "__**Log Message Deletes**__", description = "Log deleted messages and send them to a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> log message deletes <switch> <channel>")
            em.add_field(name = "**Example:**", value = "> `/log message deletes enable #channel`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "message_edits":
            em = discord.Embed(title = "__**Log Message Edits**__", description = "Log edited messages and send them to a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> log message edits <switch> <channel>")
            em.add_field(name = "**Example:**", value = "> `/log message edits enable #channel`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "role create":
            em = discord.Embed(title = "__**Log Role Create**__", description = "Log roles creation and send them to a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> log role create <switch> <channel>")
            em.add_field(name = "**Example:**", value = "> `/log role create enable #channel`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "role delete":
            em = discord.Embed(title = "__**Log Role Delete**__", description = "Log roles deletion and send them to a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> log role delete <switch> <channel>")
            em.add_field(name = "**Example:**", value = "> `/log role delete enable #channel`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "role updates":
            em = discord.Embed(title = "__**Log Role Updates**__", description = "Log roles updates and send them to a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> log role updates <switch> <channel>")
            em.add_field(name = "**Example:**", value = "> `/log role updates enable #channel`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "role given":
            em = discord.Embed(title = "__**Log Role Given**__", description = "Log given roles and send them to a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> log role given <switch> <channel>")
            em.add_field(name = "**Example:**", value = "> `/log role given enable #channel`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "role remove":
            em = discord.Embed(title = "__**Log Role Remove**__", description = "Log removed roles and send them to a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> log role remove <switch> <channel>")
            em.add_field(name = "**Example:**", value = "> `/log role remove enable #channel`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "channel create":
            em = discord.Embed(title = "__**Log Channel Create**__", description = "Log channels creation and send them to a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> log channel create <switch> <channel>")
            em.add_field(name = "**Example:**", value = "> `/log channel create enable #channel`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "channel delete":
            em = discord.Embed(title = "__**Log Channel Delete**__", description = "Log channels deletion and send them to a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> log channel delete <switch> <channel>")
            em.add_field(name = "**Example:**", value = "> `/log channel delete enable #channel`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "channel updates":
            em = discord.Embed(title = "__**Log Channel Updates**__", description = "Log channels updates and send them to a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> log channel updates <switch> <channel>")
            em.add_field(name = "**Example:**", value = "> `/log channel updates enable #channel`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "member ban":
            em = discord.Embed(title = "__**Log Member Ban**__", description = "Log banned members and send them to a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> log member ban <switch> <channel>")
            em.add_field(name = "**Example:**", value = "> `/log member ban enable #channel`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "member unban":
            em = discord.Embed(title = "__**Log Member Unban**__", description = "Log unbanned members and send them to a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> log member unban <switch> <channel>")
            em.add_field(name = "**Example:**", value = "> `/log member unban enable #channel`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "member timeout":
            em = discord.Embed(title = "__**Log Member Timout**__", description = "Log timeouted members and send them to a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> log member timeout <switch> <channel>")
            em.add_field(name = "**Example:**", value = "> `/log member timeout enable #channel`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "member nickname":
            em = discord.Embed(title = "__**Log Nickname Change**__", description = "Log nickname changes and send them to a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> log member nickname <switch> <channel>")
            em.add_field(name = "**Example:**", value = "> `/log member nickname enable #channel`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "server_updates":
            em = discord.Embed(title = "__**Log Server Updates**__", description = "Log server updates and send them to a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> log server_updates <switch> <channel>")
            em.add_field(name = "**Example:**", value = "> `/log server_updates enable #channel`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)

    #ticket commands help
    @app_commands.command(name = "tickets", description = "Shinobi Bot's ticket catogery help.")
    @app_commands.describe(command = "Choose a command to get info about it.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.choices(command = [
        app_commands.Choice(name = "launch", value = "launch"),
        app_commands.Choice(name = "close", value = "close"),
        app_commands.Choice(name = "add", value = "add"),
        app_commands.Choice(name = "remove", value = "remove"),
        app_commands.Choice(name = "role", value = "role"),
        app_commands.Choice(name = "transcript", value = "transcript")
        ])
    async def tickets(self, interaction: discord.Interaction, command: app_commands.Choice[str]):
        if command.value == "launch":
            em = discord.Embed(title = "__**Ticket Launch**__", description = "Launches the tickets system.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> ticket launch")
            em.add_field(name = "**Example:**", value = "> `/ticket launch`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "close":
            em = discord.Embed(title = "__**Ticket Close**__", description = "Closes a ticket.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> ticket close")
            em.add_field(name = "**Example:**", value = "> `/ticket close`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "add":
            em = discord.Embed(title = "__**Ticket Add**__", description = "Adds a member to the ticket.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> ticket add <member>")
            em.add_field(name = "**Example:**", value = "> `/ticket add @member`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "remove":
            em = discord.Embed(title = "__**Ticket Remove**__", description = "Removes a member from the ticket.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> ticket remove <member>")
            em.add_field(name = "**Example:**", value = "> `/ticket remove @member`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "role":
            em = discord.Embed(title = "__**Ticket Role**__", description = "Adds a role to view tickets.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> ticket role <role>")
            em.add_field(name = "**Example:**", value = "> `/ticket role @role`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "transcript":
            em = discord.Embed(title = "__**Ticket Transcript**__", description = "Generate a transcript for the ticket.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> transcript")
            em.add_field(name = "**Example:**", value = "> `/ticket transcript`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)

    #antispam commands help
    @app_commands.command(name = "antispam", description = "Shinobi Bot's anti-spam catogery help.")
    @app_commands.describe(command = "Choose a command to get info about it.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.choices(command = [
        app_commands.Choice(name = "enable", value = "enable"),
        app_commands.Choice(name = "disable", value = "disable"),
        app_commands.Choice(name = "punishment", value = "punishment"),
        app_commands.Choice(name = "whitelist", value = "whitelist")
        ])
    async def settings(self, interaction: discord.Interaction, command: app_commands.Choice[str]):
        if command.value == "enable":
            em = discord.Embed(title = "__**Anti-Spam Enable**__", description = "Enables Anti-Spam System.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> antispam enable")
            em.add_field(name = "**Example:**", value = "> `/antispam enable`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "disable":
            em = discord.Embed(title = "__**Anti-Spam Disable**__", description = "Disables Anti-Spam System.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> antispam disable")
            em.add_field(name = "**Example:**", value = "> `/antispam disable`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "punishment":
            em = discord.Embed(title = "__**Anti-Spam Punishment**__", description = "Sets a punishment for Anti-Spam System.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> antispam punishment <punishment>")
            em.add_field(name = "**Example:**", value = "> `/antispam punishment timeout`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "whitelist":
            em = discord.Embed(title = "__**Anti-Spam Whitelist**__", description = "Whitelist a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> antispam whitelist <channel>")
            em.add_field(name = "**Example:**", value = "> `/antispam whitelist #channel`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)

    #settings commands help
    @app_commands.command(name = "settings", description = "Shinobi Bot's settings catogery help.")
    @app_commands.describe(command = "Choose a command to get info about it.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.choices(command = [
        app_commands.Choice(name = "lock", value = "lock"),
        app_commands.Choice(name = "lockall", value = "lockall"),
        app_commands.Choice(name = "unlock", value = "unlock"),
        app_commands.Choice(name = "unlockall", value = "unlockall"),
        app_commands.Choice(name = "hide", value = "hide"),
        app_commands.Choice(name = "hideall", value = "hideall"),
        app_commands.Choice(name = "show", value = "show"),
        app_commands.Choice(name = "showall", value = "showall"),
        app_commands.Choice(name = "suggestions", value = "suggestions"),
        app_commands.Choice(name = "prvchannel", value = "prvchannel")
        ])
    async def settings(self, interaction: discord.Interaction, command: app_commands.Choice[str]):
        if command.value == "lock":
            em = discord.Embed(title = "__**Lock**__", description = "Locks a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> lock [channel]")
            em.add_field(name = "**Example:**", value = "> `/lock #channel`")
            em.add_field(name = "**Note:**", value = "> If no channel is mentioned, deafult is message's channel.")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "lockall":
            em = discord.Embed(title = "__**Lock All**__", description = "Locks all channels in the server.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> lockall")
            em.add_field(name = "**Example:**", value = "> `/lockall`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "unlock":
            em = discord.Embed(title = "__**Unlock**__", description = "Unlocks a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> unlock [channel]")
            em.add_field(name = "**Example:**", value = "> `/unlock #channel`")
            em.add_field(name = "**Note:**", value = "> If no channel is mentioned, deafult is message's channel.")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "unlockall":
            em = discord.Embed(title = "__**Unlockall**__", description = "Unlocks all channels in the server.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> unlockall")
            em.add_field(name = "**Example:**", value = "> `/unlockall`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "hide":
            em = discord.Embed(title = "__**Hide**__", description = "Hides a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> hide [channel]")
            em.add_field(name = "**Example:**", value = "> `/hide #channel`")
            em.add_field(name = "**Note:**", value = "> If no channel is mentioned, deafult is message's channel.")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "hideall":
            em = discord.Embed(title = "__**Hide All**__", description = "Hides all channels in the server.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> hideall")
            em.add_field(name = "**Example:**", value = "> `/hideall`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "show":
            em = discord.Embed(title = "__**Show**__", description = "Shows a channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> show [channel]")
            em.add_field(name = "**Example:**", value = "> `/show #channel`")
            em.add_field(name = "**Note:**", value = "> If no channel is mentioned, deafult is message's channel.")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "showall":
            em = discord.Embed(title = "__**Show All**__", description = "Shows all channels in the server.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> showall")
            em.add_field(name = "**Example:**", value = "> `/showall`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "prvchannel":
            em = discord.Embed(title = "__**Prvchannel**__", description = "Creates a temprory private channel.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> prvchannel <time> <channel name>")
            em.add_field(name = "**Example:**", value = "> `/prvchannel 3h discussion`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "suggestions":
            em = discord.Embed(title = "__**Suggestions**__", description = "Set channels for suggestions.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> suggestions <switch> <suggestions channel> <suggestions' review channel>")
            em.add_field(name = "**Example:**", value = "> `/suggestions enable #suggestions #suggestions-review`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)

    #fun commands help
    @app_commands.command(name = "fun", description = "Shinobi Bot's fun catogery help.")
    @app_commands.describe(command = "Choose a command to get info about it.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.choices(command = [
        app_commands.Choice(name = "meme", value = "meme"),
        app_commands.Choice(name = "rate", value = "rate"),
        app_commands.Choice(name = "f", value = "f"),
        app_commands.Choice(name = "coinflip", value = "coinflip"),
        app_commands.Choice(name ="reverse", value = "reverse"),
        app_commands.Choice(name = "slot", value = "slot"),
        app_commands.Choice(name = "choose", value = "choose"),
        app_commands.Choice(name = "emojify", value = "emojify"),
        app_commands.Choice(name = "wyr", value = "wyr"),
        app_commands.Choice(name = "cat", value = "cat"),
        app_commands.Choice(name = "dog", value = "dog"),
        app_commands.Choice(name = "dadjoke", value = "dadjoke")
        ])
    async def fun(self, interaction: discord.Interaction, command: app_commands.Choice[str]):
        if command.value == "meme":
            em = discord.Embed(title = "__**Meme**__", description = "Gets a nice meme.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> meme")
            em.add_field(name = "**Example:**", value = "> `/meme`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "rate":
            em = discord.Embed(title = "__**Rate**__", description = "Rates.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> rate")
            em.add_field(name = "**Example:**", value = "> `/rate`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "f":
            em = discord.Embed(title = "__**F**__", description = "Press f to pay respect.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> f")
            em.add_field(name = "**Example:**", value = "> `/f`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "coinflip":
            em = discord.Embed(title = "__**Coinflip**__", description = "Flips a coin.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> coinflip")
            em.add_field(name = "**Example:**", value = "> `/coinflip`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "reverse":
            em = discord.Embed(title = "__**Reverse**__", description = "Reverses anything you type.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> reverse <words>")
            em.add_field(name = "**Example:**", value = "> `/reverse this will be reversed`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "slot":
            em = discord.Embed(title = "__**Slot**__", description = "Slot machine.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> slot")
            em.add_field(name = "**Example:**", value = "> `/slot`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "choose":
            em = discord.Embed(title = "__**Choose**__", description = "Makes the choosing easier.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> choose <choice 1> <choice 2> [choice 3] [choice 4] [choice 5]")
            em.add_field(name = "**Example:**", value = "> `/choose aot kny sao naruto conan`")
            em.add_field(name = "**Note:**", value = "> You must include at least 2 choices and maximum 5")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "emojify":
            em = discord.Embed(title = "__**Emojify**__", description = "Converts any word to emojis.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> emojify <words>")
            em.add_field(name = "**Example:**", value = "> `/emojify Hello World`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "wyr":
            em = discord.Embed(title = "__**WYR**__", description = "Would you rather...", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> wyr")
            em.add_field(name = "**Example:**", value = "> `/wyr`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "cat":
            em = discord.Embed(title = "__**Cat**__", description = "Gets a random cat image.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> cat")
            em.add_field(name = "**Example:**", value = "> `/cat`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "dog":
            em = discord.Embed(title = "__**Dog**__", description = "Gets a random dog image.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> dog")
            em.add_field(name = "**Example:**", value = "> `/dog`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "dadjoke":
            em = discord.Embed(title = "__**Dadjoke**__", description = "Gets a random dad joke.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> dadjoke")
            em.add_field(name = "**Example:**", value = "> `/dadjoke`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "geekjoke":
            em = discord.Embed(title = "__**Geekjoke**__", description = "Gets a random geek joke.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> geekjoke")
            em.add_field(name = "**Example:**", value = "> `/geekjoke`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)

    #games commands help
    @app_commands.command(name = "games", description = "Shinobi Bot's games catogery help.")
    @app_commands.describe(command = "Choose a command to get info about it.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.choices(command = [
        app_commands.Choice(name = "connect4", value = "connect4"),
        app_commands.Choice(name = "tictactoe", value = "tictactoe"),
        app_commands.Choice(name = "rps", value = "rps")
        ])
    async def games(self, interaction: discord.Interaction, command: app_commands.Choice[str]):
        if command.value == "connect4":
            em = discord.Embed(title = "__**Connect4**__", description = "Challenge others in connect 4!", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> connect4 <player 2>")
            em.add_field(name = "**Example:**", value = "> `/connect4 @member`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "tictactoe":
            em = discord.Embed(title = "__**TicTacTie**__", description = "Challenge others in tictactoe!", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> tictactoe <player 2>")
            em.add_field(name = "**Example:**", value = "> `/tictactoe @member`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "rps":
            em = discord.Embed(title = "__**RPS**__", description = "Challenge others in rock paper scissors!", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> rps [player 2]")
            em.add_field(name = "**Example:**", value = "> `/rps @member`")
            em.add_field(name = "**Note:**", value = "> You can challenge the bot itself.")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)

    #serverinformation commands help
    @app_commands.command(name = "serverinformation", description = "Shinobi Bot's server information catogery help.")
    @app_commands.describe(command = "Choose a command to get info about it.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.choices(command = [
        app_commands.Choice(name = "server", value = "server"),
        app_commands.Choice(name = "owner", value = "owner"),
        app_commands.Choice(name = "id", value = "id"), 
        app_commands.Choice(name = "members", value ="members"),
        app_commands.Choice(name = "channels", value = "channels"),
        app_commands.Choice(name = "user", value = "user"),
        app_commands.Choice(name = "icon", value = "icon"),
        app_commands.Choice(name = "roles", value = "roles"),
        app_commands.Choice(name = "avatar", value = "avatar"),
        app_commands.Choice(name = "banner", value = "banner")
        ])
    async def serverinformation(self, interaction: discord.Interaction, command: app_commands.Choice[str]):
        if command.value == "server":
            em = discord.Embed(title = "__**Server**__", description = "All information about the server.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> server")
            em.add_field(name = "**Example:**", value = "> `/server`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "owner":
            em = discord.Embed(title = "__**Owner**__", description = "Shows the owner of the server.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> owner")
            em.add_field(name = "**Example:**", value = "> `/owner`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "id":
            em = discord.Embed(title = "__**ID**__", description = "Shows the ID of the server.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> id")
            em.add_field(name = "**Example:**", value = "> `/id`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "members":
            em = discord.Embed(title = "__**Members**__", description = "Shows the members' count of the server.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> memebrs")
            em.add_field(name = "**Example:**", value = "> `/members`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "channels":
            em = discord.Embed(title = "__**channels Count**__", description = "Shows server's channels' count.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> channels")
            em.add_field(name = "**Example:**", value = "> `/channels`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "user":
            em = discord.Embed(title = "__**User**__", description = "All information about the user.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> user [member]")
            em.add_field(name = "**Example:**", value = "> `/user`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "icon":
            em = discord.Embed(title = "__**Icon**__", description = "Shows server's icon/avatar.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> icon")
            em.add_field(name = "**Example:**", value = "> `/icon`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "roles":
            em = discord.Embed(title = "__**Roles**__", description = "Gets a list of all the roles in the server.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> roles")
            em.add_field(name = "**Example:**", value = "> `/roles`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "avatar":
            em = discord.Embed(title = "__**Avatar**__", description = "Get's member's avatar.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> avatar [member]")
            em.add_field(name = "**Example:**", value = "> `/avatar @member`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)
        elif command.value == "banner":
            em = discord.Embed(title = "__**Banner**__", description = "Get's member's banner.", color = 0x2F3136)
            em.add_field(name = "**Syntax:**", value = "> banner [member]")
            em.add_field(name = "**Example:**", value = "> `/banner @member`")
            em.set_footer(text = "<> means requird, [] means optional")
            await interaction.response.send_message(embed = em)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Help(bot))
