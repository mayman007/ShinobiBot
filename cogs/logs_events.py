import discord
from discord.ext import commands
from datetime import datetime
import aiosqlite


# Logs Events Class
class logs_events(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Logs Events is online.")

    # Role updated (name, permission added/removed)
    @commands.Cog.listener()
    async def on_guild_role_update(self, role_before: discord.Role, role_after: discord.Role):
        async with aiosqlite.connect("db/log_role_updates.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)") # Create the table if not exists
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (role_after.guild.id,))
                data = await cursor.fetchone()
                if data:
                    log_channel = data[0]
                    if role_before.name != role_after.name: # Check role's name
                        embed = discord.Embed(title = f":family: Role Name Updated", color = 0x000000, timestamp = datetime.now())
                        embed.set_author(name = role_after.guild.name, icon_url = role_after.guild.icon.url)
                        embed.add_field(name = "Old:", value = role_before)
                        embed.add_field(name = "New:", value = role_after)
                        embed.set_footer(text = role_after.guild.name)
                        channel = self.bot.get_channel(log_channel)
                        await channel.send(embed = embed)
                    elif role_before.permissions != role_after.permissions: # Checl role's permissions
                        diff = set(role_before.permissions).symmetric_difference(set(role_after.permissions))
                        permission = list(diff)[0][0]
                        permission = permission.replace("_", " ").title()
                        if list(diff)[0][1] == True:
                            in_title = "Removed"
                            in_des = "removed from"
                        else:
                            in_title = "Added"
                            in_des = "added to"
                        embed = discord.Embed(color = 0x000000, timestamp = datetime.now())
                        embed.set_author(name = role_after.guild.name, icon_url = role_after.guild.icon.url)
                        embed.add_field(name = f":family: Role Permission {in_title}", value = f"{permission} {in_des} {role_after.mention}")
                        embed.set_footer(text = role_after.guild.name)
                        channel = self.bot.get_channel(log_channel)
                        await channel.send(embed = embed)


    # Role deleted
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        async with aiosqlite.connect("db/log_role_delete.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)") # Create the table if not exists
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (role.guild.id,))
                data = await cursor.fetchone()
                if data:
                    log_channel = data[0]
                    embed = discord.Embed(color = 0x000000, timestamp = datetime.now())
                    embed.set_author(name = role.guild.name, icon_url = role.guild.icon.url)
                    embed.add_field(name = ":family: Role Deleted", value = role)
                    embed.set_footer(text = role.guild.name)
                    channel = self.bot.get_channel(log_channel)
                    await channel.send(embed = embed)

    # Role created
    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        async with aiosqlite.connect("db/log_role_create.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)") # Create the table if not exists
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (role.guild.id,))
                data = await cursor.fetchone()
                if data:
                    log_channel = data[0]
                    embed = discord.Embed(color = 0x000000, timestamp = datetime.now())
                    embed.set_author(name = role.guild.name, icon_url = role.guild.icon.url)
                    embed.add_field(name = ":family: Role Created", value = role)
                    embed.set_footer(text = role.guild.name)
                    channel = self.bot.get_channel(log_channel)
                    await channel.send(embed = embed)

    # Member unbanned
    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.Member):
        async with aiosqlite.connect("db/log_member_unban.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)") # Create the table if not exists
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (guild.id,))
                data = await cursor.fetchone()
                if data:
                    log_channel = data[0]
                    embed = discord.Embed(color = 0x000000, timestamp = datetime.now())
                    embed.set_author(name = user.name, icon_url = user.avatar.url)
                    embed.add_field(name = ":airplane: Member Unbanned", value = user)
                    embed.set_thumbnail(url = user.avatar.url)
                    embed.set_footer(text = guild.name)
                    channel = self.bot.get_channel(log_channel)
                    await channel.send(embed = embed)

    # Member banned
    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.Member):
        async with aiosqlite.connect("db/log_member_ban.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)") # Create the table if not exists
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (guild.id,))
                data = await cursor.fetchone()
                if data:
                    log_channel = data[0]
                    embed = discord.Embed(color = 0x000000, timestamp = datetime.now())
                    embed.set_author(name = user.name, icon_url = user.avatar.url)
                    embed.add_field(name = ":airplane: Member Banned", value = user)
                    embed.set_thumbnail(url = user.avatar.url)
                    embed.set_footer(text = guild.name)
                    channel = self.bot.get_channel(log_channel)
                    await channel.send(embed = embed)

    # Member updated (nickname, role, display avatar, timeout)
    @commands.Cog.listener()
    async def on_member_update(self, member_before: discord.Member, member_after: discord.Member):
                if member_before.nick != member_after.nick: # Check member's nickname
                    async with aiosqlite.connect("db/log_nickname_change.db") as db: # Open the db
                        async with db.cursor() as cursor:
                            await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)") # Create the table if not exists
                            await cursor.execute("SELECT channel FROM log WHERE guild = ?", (member_after.guild.id,))
                            data = await cursor.fetchone()
                            if data:
                                log_channel = data[0]
                                embed = discord.Embed(color = 0x000000, timestamp = datetime.now())
                                embed.set_author(name = member_after.name, icon_url = member_after.avatar.url)
                                embed.add_field(name = ":house: Member's Nickname Updated", value = member_after)
                                embed.add_field(name = "**Old Nickname:**", value = member_before.nick)
                                embed.add_field(name = "**New Nickname:**", value = member_after.nick)
                                embed.set_thumbnail(url = member_after.avatar.url)
                                embed.set_footer(text = member_after.guild.name)
                                channel = self.bot.get_channel(log_channel)
                                await channel.send(embed = embed)
                elif member_before.roles != member_after.roles: # Check member's roles
                    diff = str(set(member_before.roles).symmetric_difference(set(member_after.roles))).replace("{", "").replace("}", "")
                    diff_id = diff.split("id=")[1].split(" name")[0]
                    diff_role = discord.utils.find(lambda r: r.id == int(diff_id), member_after.guild.roles)
                    if diff_role in member_before.roles:
                        async with aiosqlite.connect("db/log_role_remove.db") as db: # Open the db
                            async with db.cursor() as cursor:
                                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)") # Create the table if not exists
                                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (member_after.guild.id,))
                                data = await cursor.fetchone()
                                if data:
                                    log_channel = data[0]
                                    in_des = "removed from"
                                else: return
                    elif diff_role in member_after.roles:
                        async with aiosqlite.connect("db/log_role_given.db") as db: # Open the db
                            async with db.cursor() as cursor:
                                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)") # Create the table if not exists
                                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (member_after.guild.id,))
                                data = await cursor.fetchone()
                                if data:
                                    log_channel = data[0]
                                    in_des = "added to"
                                else: return
                    embed = discord.Embed(color = 0x000000, timestamp = datetime.now())
                    embed.set_author(name = member_after.name, icon_url = member_after.avatar.url)
                    embed.add_field(name = ":house: Member's Roles Updated", value = f"The role {diff_role.mention} has been {in_des} {member_after.mention}")
                    embed.set_thumbnail(url = member_after.avatar.url)
                    embed.set_footer(text = member_after.guild.name)
                    channel = self.bot.get_channel(log_channel)
                    await channel.send(embed = embed)
                elif member_after.is_timed_out() == True: # Check if member got timeout
                    async with aiosqlite.connect("db/log_member_timeout.db") as db: # Open the db
                        async with db.cursor() as cursor:
                            await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)") # Create the table if not exists
                            await cursor.execute("SELECT channel FROM log WHERE guild = ?", (member_after.guild.id,))
                            data = await cursor.fetchone()
                            if data:
                                log_channel = data[0]
                                embed = discord.Embed(color = 0x000000, timestamp = datetime.now())
                                embed.set_author(name = member_after.name, icon_url = member_after.avatar.url)
                                embed.add_field(name = ":house: Member's Timeout", value = f"{member_after.mention} got timeout")
                                embed.set_thumbnail(url = member_after.display_avatar.url)
                                embed.set_footer(text = member_after.guild.name)
                                channel = self.bot.get_channel(log_channel)
                                await channel.send(embed = embed)
                # elif member_before.display_avatar.url != member_after.display_avatar.url: # Check member's display avatar
                #     embed = discord.Embed(color = 0x000000, timestamp = datetime.now())
                #     embed.set_author(name = member_after.name, icon_url = member_after.avatar.url)
                #     embed.add_field(name = ":house: Member's Server Avatar Updated", value = member_after)
                #     embed.set_thumbnail(url = member_after.display_avatar.url)
                #     embed.set_footer(text = member_after.guild.name)
                #     channel = self.bot.get_channel(log_channel)
                #     await channel.send(embed = embed)

    # Channel updated (name, permission)
    @commands.Cog.listener()
    async def on_guild_channel_update(self, channel_before: discord.abc.GuildChannel, channel_after: discord.abc.GuildChannel):
        async with aiosqlite.connect("db/log_channel_updates.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)") # Create the table if not exists
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (channel_after.guild.id,))
                data = await cursor.fetchone()
                if data:
                    log_channel = data[0]
                    if channel_before.name != channel_after.name: # Check channel's name
                        embed = discord.Embed(title = ":house: Channel Name Updated:",color = 0x000000, timestamp = datetime.now())
                        embed.set_author(name = channel_after.guild.name, icon_url = channel_after.guild.icon.url)
                        embed.add_field(name = "Old:", value = channel_before.name)
                        embed.add_field(name = "New:", value = channel_after.name)
                        embed.set_footer(text = channel_after.guild.name)
                        channel = self.bot.get_channel(log_channel)
                        await channel.send(embed = embed)
                    else: # Check channel's permissions
                        for role in channel_after.guild.roles:
                            if channel_before.permissions_for(role) != channel_after.permissions_for(role):
                                is_role = True
                                in_des = role.mention
                                break
                            else:
                                is_role = False
                        if not is_role:
                            for member in channel_after.guild.members:
                                if channel_before.permissions_for(member) != channel_after.permissions_for(member):
                                    is_member = True
                                    in_des = member.mention
                                    break
                                else:
                                    is_member = False
                        if is_role or is_member:
                            embed = discord.Embed(color = 0x000000, timestamp = datetime.now())
                            embed.set_author(name = channel_after.guild.name, icon_url = channel_after.guild.icon.url)
                            embed.add_field(name = ":house: Channel Permissions Updated", value = f"Permissions for {in_des} has been updated in {channel_after.mention}")
                            embed.set_footer(text = channel_after.guild.name)
                            channel = self.bot.get_channel(log_channel)
                            await channel.send(embed = embed)

    # Private channel updated
    @commands.Cog.listener()
    async def on_private_channel_update(self, channel_before: discord.abc.PrivateChannel, channel_after: discord.abc.PrivateChannel):
        async with aiosqlite.connect("db/log_channel_updates.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)") # Create the table if not exists
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (channel_after.guild.id,))
                data = await cursor.fetchone()
                if data:
                    log_channel = data[0]
                    if channel_before.name != channel_after.name: # Check channel's name
                        embed = discord.Embed(title = ":house: Channel Name Updated:",color = 0x000000, timestamp = datetime.now())
                        embed.set_author(name = channel_after.guild.name, icon_url = channel_after.guild.icon.url)
                        embed.add_field(name = "Old:", value = channel_before.name)
                        embed.add_field(name = "New:", value = channel_after.name)
                        embed.set_footer(text = channel_after.guild.name)
                        channel = self.bot.get_channel(log_channel)
                        await channel.send(embed = embed)
                    else: # Check channel's permissions
                        for role in channel_after.guild.roles:
                            if channel_before.permissions_for(role) != channel_after.permissions_for(role):
                                is_role = True
                                in_des = role.mention
                                break
                            else:
                                is_role = False
                        if not is_role:
                            for member in channel_after.guild.members:
                                if channel_before.permissions_for(member) != channel_after.permissions_for(member):
                                    is_member = True
                                    in_des = member.mention
                                    break
                                else:
                                    is_member = False
                        if is_role or is_member:
                            embed = discord.Embed(color = 0x000000, timestamp = datetime.now())
                            embed.set_author(name = channel_after.guild.name, icon_url = channel_after.guild.icon.url)
                            embed.add_field(name = ":house: Channel Permissions Updated", value = f"Permissions for {in_des} has been updated in {channel_after.mention}")
                            embed.set_footer(text = channel_after.guild.name)
                            channel = self.bot.get_channel(log_channel)
                            await channel.send(embed = embed)

    # Channel deleted
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        async with aiosqlite.connect("db/log_channel_delete.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)") # Create the table if not exists
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (channel.guild.id,))
                data = await cursor.fetchone()
                if data:
                    log_channel = data[0]
                    embed = discord.Embed(color = 0x000000, timestamp = datetime.now())
                    embed.set_author(name = channel.guild.name, icon_url = channel.guild.icon.url)
                    embed.add_field(name = ":house: Channel Deleted", value = channel.name)
                    embed.set_footer(text = channel.guild.name)
                    channel = self.bot.get_channel(log_channel)
                    await channel.send(embed = embed)

    # Channel created
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        async with aiosqlite.connect("db/log_channel_create.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)") # Create the table if not exists
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (channel.guild.id,))
                data = await cursor.fetchone()
                if data:
                    log_channel = data[0]
                    embed = discord.Embed(color = 0x000000, timestamp = datetime.now())
                    embed.set_author(name = channel.guild.name, icon_url = channel.guild.icon.url)
                    embed.add_field(name = ":house: Channel Created", value = channel.name)
                    embed.set_footer(text = channel.guild.name)
                    channel = self.bot.get_channel(log_channel)
                    await channel.send(embed = embed)

    # Message deleted
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        async with aiosqlite.connect("db/log_messages_deletes.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)") # Create the table if not exists
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (message.guild.id,))
                data = await cursor.fetchone()
                if data:
                    log_channel = data[0]
                    embed = discord.Embed(description = f"**:wastebasket: Message sent by {message.author.mention} deleted in {message.channel.mention}**",
                                        color = 0x000000, timestamp = datetime.now())
                    embed.set_author(name = message.author, icon_url = message.author.avatar.url)
                    embed.add_field(name = "Message:", value = f"```{message.content}```")
                    embed.set_footer(text = message.guild.name)
                    channel = self.bot.get_channel(log_channel)
                    await channel.send(embed = embed)

    # Message edited
    @commands.Cog.listener()
    async def on_message_edit(self, message_before: discord.Message, message_after: discord.Message):
        if message_before.author.bot: return
        async with aiosqlite.connect("db/log_messages_edits.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)") # Create the table if not exists
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (message_after.guild.id,))
                data = await cursor.fetchone()
                if data:
                    log_channel = data[0]
                    embed = discord.Embed(description = f"**:pencil2: Message sent by {message_after.author.mention} edited in {message_after.channel.mention}. [Jump to Message]({message_after.jump_url})**",
                                        color = 0x000000, timestamp = datetime.now())
                    embed.set_author(name = message_after.author, icon_url = message_after.author.avatar.url)
                    embed.add_field(name = "Old:", value = f"```{message_before.content}```")
                    embed.add_field(name = "New:", value = f"```{message_after.content}```")
                    embed.set_footer(text = message_after.guild.name)
                    channel=self.bot.get_channel(log_channel)
                    await channel.send(embed = embed)

    # Member joined
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        async with aiosqlite.connect("db/log_joins.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)") # Create the table if not exists
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (member.guild.id,))
                data = await cursor.fetchone()
                if data:
                    log_channel = data[0]
                    date_format = "%d/%m/%Y %H:%M"
                    channel = self.bot.get_channel(log_channel)
                    e = discord.Embed(title = f"{member.name} joined!", description = f"{member.mention} joined the server.", color = 0x000000, timestamp = datetime.now())
                    e.set_author(name = member.name, icon_url = member.avatar.url)
                    e.set_thumbnail(url = member.avatar.url)
                    e.add_field(name = "Age of Account:", value = f"`{member.created_at.strftime(date_format)}`")
                    e.set_footer(text = member.guild.name)
                    await channel.send(embed = e)

    # Member left
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        async with aiosqlite.connect("db/log_leaves.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)") # Create the table if not exists
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (member.guild.id,))
                data = await cursor.fetchone()
                if data:
                    log_channel = data[0]
                    date_format = "%d/%m/%Y"
                    channel = self.bot.get_channel(log_channel)
                    e = discord.Embed(title = f"{member.name} has left!", description = f"{member.mention} left the server.", color = 0x000000, timestamp = datetime.now())
                    e.set_author(name = member.name, icon_url = member.avatar.url)
                    e.set_thumbnail(url = member.avatar.url)
                    e.add_field(name = "Age of Account:", value = f"`{member.created_at.strftime(date_format)}`")
                    e.add_field(name = "Member from:", value = f"`{member.joined_at.strftime(date_format)}`")
                    e.set_footer(text = member.guild.name)
                    await channel.send(embed = e)

    # Guild updated (name, icon)
    @commands.Cog.listener()
    async def on_guild_update(self, guild_before: discord.Guild, guild_after: discord.Guild):
        async with aiosqlite.connect("db/log_server_updates.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)") # Create the table if not exists
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (guild_after.id,))
                data = await cursor.fetchone()
                if data:
                    log_channel = data[0]
                    if guild_before.name != guild_after.name:
                        embed = discord.Embed(title = ":house: Server Name Updated", color = 0x000000, timestamp = datetime.now())
                        embed.set_author(name = guild_after.name, icon_url = guild_after.icon.url)
                        embed.add_field(name = "Old:", value = guild_before.name)
                        embed.add_field(name = "New:", value = guild_after.name)
                        embed.set_footer(text = guild_after.name)
                        channel = self.bot.get_channel(log_channel)
                        await channel.send(embed = embed)
                    elif guild_before.icon.url != guild_after.icon.url:
                        embed = discord.Embed(color = 0x000000, timestamp = datetime.now())
                        embed.set_author(name = guild_after.name, icon_url = guild_after.icon.url)
                        embed.add_field(name = ":house: Server Icon Updated", value = guild_after)
                        embed.set_thumbnail(url = guild_after.icon.url)
                        embed.set_footer(text = guild_after.name)
                        channel = self.bot.get_channel(log_channel)
                        await channel.send(embed = embed)

    # # Guild emojis updated
    # @commands.Cog.listener()
    # async def on_guild_emojis_update(self, guild: discord.Guild, before, after):
    # pass

    # # Guild stickers updated
    # @commands.Cog.listener()
    # async def on_guild_stickers_update(self, guild: discord.Guild, before, after):
    # pass

    # #on private channel pins update
    # @commands.Cog.listener()
    # async def on_private_channel_pins_update(self, channel: discord.abc.PrivateChannel, last_pin):
    # pass

    # #on channel pins update
    # @commands.Cog.listener()
    # async def on_guild_channel_pins_update(self, channel: discord.abc.GuildChannel, last_pin):
    # pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(logs_events(bot))