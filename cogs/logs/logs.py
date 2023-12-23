import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite


#edits confirm button
class editsConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def edits_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/log_messages_edits.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE log SET channel = ? WHERE guild = ?", (edits_log_channel, interaction.guild.id,))
                else: await cursor.execute("INSERT INTO log (channel, guild) VALUES (?, ?)", (edits_log_channel, interaction.guild.id,))
                embed = discord.Embed(title = "📝 ┃ Edited Messages Log", description = "Your edited messages log channel has been updated succesfully!", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def edits_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Process Canceled.")

#deletes confirm button
class deletesConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def deletes_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/log_messages_deletes.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE log SET channel = ? WHERE guild = ?", (deletes_log_channel, interaction.guild.id,))
                else: await cursor.execute("INSERT INTO log (channel, guild) VALUES (?, ?)", (deletes_log_channel, interaction.guild.id,))
                embed = discord.Embed(title = "📝 ┃ Deleted Messages Log", description = "Your deleted messages log channel has been updated succesfully!", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def deletes_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Process Canceled.")

#joins confirm button
class joinsConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def joins_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/log_joins.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE log SET channel = ? WHERE guild = ?", (joins_channel, interaction.guild.id,))
                else: await cursor.execute("INSERT INTO log (channel, guild) VALUES (?, ?)", (joins_channel, interaction.guild.id,))
                embed = discord.Embed(title = "📝 ┃ Joins Log", description = "Your members' joins log channel has been updated succesfully!", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def joins_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Process Canceled.")

#leaves confirm button
class leavesConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def leaves_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/log_leaves.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE log SET channel = ? WHERE guild = ?", (leaves_channel, interaction.guild.id,))
                else: await cursor.execute("INSERT INTO log (channel, guild) VALUES (?, ?)", (leaves_channel, interaction.guild.id,))
                embed = discord.Embed(title = "📝 ┃ Leaves Log", description = "Your members' leaves log channel has been updated succesfully!", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def leaves_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Process Canceled.")

# role create confirm button
class roleCreateConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def role_create_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/log_role_create.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE log SET channel = ? WHERE guild = ?", (roles_create_channel, interaction.guild.id,))
                else: await cursor.execute("INSERT INTO log (channel, guild) VALUES (?, ?)", (roles_create_channel, interaction.guild.id,))
                embed = discord.Embed(title = "📝 ┃ Role Create Log", description = "Your role create log channel has been updated succesfully!", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def role_create_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Process Canceled.")

# role delete confirm button
class roleDeleteConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def role_delete_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/log_role_delete.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE log SET channel = ? WHERE guild = ?", (roles_delete_channel, interaction.guild.id,))
                else: await cursor.execute("INSERT INTO log (channel, guild) VALUES (?, ?)", (roles_delete_channel, interaction.guild.id,))
                embed = discord.Embed(title = "📝 ┃ Role Delete Log", description = "Your role delete log channel has been updated succesfully!", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def role_delete_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Process Canceled.")

# role update confirm button
class roleUpdatesConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def role_update_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/log_role_updates.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE log SET channel = ? WHERE guild = ?", (roles_updates_channel, interaction.guild.id,))
                else: await cursor.execute("INSERT INTO log (channel, guild) VALUES (?, ?)", (roles_updates_channel, interaction.guild.id,))
                embed = discord.Embed(title = "📝 ┃ Role Updates Log", description = "Your role updates log channel has been updated succesfully!", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def role_update_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Process Canceled.")

# role given confirm button
class roleGivenConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def role_given_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/log_role_given.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE log SET channel = ? WHERE guild = ?", (roles_given_channel, interaction.guild.id,))
                else: await cursor.execute("INSERT INTO log (channel, guild) VALUES (?, ?)", (roles_given_channel, interaction.guild.id,))
                embed = discord.Embed(title = "📝 ┃ Role Given Log", description = "Your role given log channel has been updated succesfully!", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def role_given_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Process Canceled.")

# role remove confirm button
class roleRemoveConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def role_leave_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/log_role_remove.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE log SET channel = ? WHERE guild = ?", (roles_removed_channel, interaction.guild.id,))
                else: await cursor.execute("INSERT INTO log (channel, guild) VALUES (?, ?)", (roles_removed_channel, interaction.guild.id,))
                embed = discord.Embed(title = "📝 ┃ Role Remove Log", description = "Your role remove log channel has been updated succesfully!", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def role_remove_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Process Canceled.")

# member ban confirm button
class memberBanConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def member_ban_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/log_member_ban.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE log SET channel = ? WHERE guild = ?", (member_ban_channel, interaction.guild.id,))
                else: await cursor.execute("INSERT INTO log (channel, guild) VALUES (?, ?)", (member_ban_channel, interaction.guild.id,))
                embed = discord.Embed(title = "📝 ┃ Member Ban Log", description = "Your member ban log channel has been updated succesfully!", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def member_ban_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Process Canceled.")

# member unban confirm button
class memberUnbanConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def member_unban_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/log_member_unban.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE log SET channel = ? WHERE guild = ?", (member_unban_channel, interaction.guild.id,))
                else: await cursor.execute("INSERT INTO log (channel, guild) VALUES (?, ?)", (member_unban_channel, interaction.guild.id,))
                embed = discord.Embed(title = "📝 ┃ Member Unban Log", description = "Your member unban log channel has been updated succesfully!", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def member_unban_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Process Canceled.")

# member timeout confirm button
class memberTimeoutConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def member_timeout_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/log_member_timeout.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE log SET channel = ? WHERE guild = ?", (member_timeout_channel, interaction.guild.id,))
                else: await cursor.execute("INSERT INTO log (channel, guild) VALUES (?, ?)", (member_timeout_channel, interaction.guild.id,))
                embed = discord.Embed(title = "📝 ┃ Member Timeout Log", description = "Your member timeout log channel has been updated succesfully!", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def member_timeout_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Process Canceled.")

# nickname change confirm button
class nicknameChangeConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def nickname_change_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/log_nickname_change.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE log SET channel = ? WHERE guild = ?", (nickname_change_channel, interaction.guild.id,))
                else: await cursor.execute("INSERT INTO log (channel, guild) VALUES (?, ?)", (nickname_change_channel, interaction.guild.id,))
                embed = discord.Embed(title = "📝 ┃ Nickname Change Log", description = "Your nickname change log channel has been updated succesfully!", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def nickname_change_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Process Canceled.")

# channel create confirm button
class channelCreateConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def channel_create_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/log_channel_create.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE log SET channel = ? WHERE guild = ?", (channel_create_channel, interaction.guild.id,))
                else: await cursor.execute("INSERT INTO log (channel, guild) VALUES (?, ?)", (channel_create_channel, interaction.guild.id,))
                embed = discord.Embed(title = "📝 ┃ Channel Create Log", description = "Your channel create log channel has been updated succesfully!", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def channel_create_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Process Canceled.")

# channel delete confirm button
class channelDeleteConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def channel_delete_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/log_channel_delete.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE log SET channel = ? WHERE guild = ?", (channel_delete_channel, interaction.guild.id,))
                else: await cursor.execute("INSERT INTO log (channel, guild) VALUES (?, ?)", (channel_delete_channel, interaction.guild.id,))
                embed = discord.Embed(title = "📝 ┃ Channel Delete Log", description = "Your channel delete log channel has been updated succesfully!", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def channel_delete_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Process Canceled.")

# channel updates confirm button
class channelUpdatesConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def channel_updates_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/log_channel_updates.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE log SET channel = ? WHERE guild = ?", (channel_updates_channel, interaction.guild.id,))
                else: await cursor.execute("INSERT INTO log (channel, guild) VALUES (?, ?)", (channel_updates_channel, interaction.guild.id,))
                embed = discord.Embed(title = "📝 ┃ Channel Updates Log", description = "Your channel updates log channel has been updated succesfully!", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def channel_updates_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Process Canceled.")

# server updates confirm button
class serverUpdatesConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def server_updates_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        async with aiosqlite.connect("db/log_server_updates.db") as db: # Open the db
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("UPDATE log SET channel = ? WHERE guild = ?", (server_updates_channel, interaction.guild.id,))
                else: await cursor.execute("INSERT INTO log (channel, guild) VALUES (?, ?)", (server_updates_channel, interaction.guild.id,))
                embed = discord.Embed(title = "📝 ┃ Server Updates Log", description = "Your server updates log channel has been updated succesfully!", color = 0x000000)
                await interaction.response.send_message(embed = embed)
            await db.commit()
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view = self)
    #cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def server_updates_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Process Canceled.")

# server updates confirm button
class ConfirmDisableAll(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.danger)
    async def confirm_disable_all(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        logs_files_list = ["joins", "leaves", "messages_edits", "messages_deletes", "role_create", "role_delete", "role_updates", "role_given", "role_remove",
                           "channel_create", "channel_delete", "channel_updates", "member_ban", "member_unban", "member_timeout" ,"nickname_change", "server_updates"]
        for log_file in logs_files_list:
            async with aiosqlite.connect(f"db/log_{log_file}.db") as db:
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                    await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data: await cursor.execute("DELETE FROM log WHERE guild = ?", (interaction.guild.id,))
                await db.commit()
        await interaction.followup.send("All logs have been disabled successfully.")
    # cancel button
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.gray)
    async def cancel_disable_all(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Process Canceled.")

# disable all settings confirm button
class DisableAll(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Disable All", style = discord.ButtonStyle.red)
    async def disable_all(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        embed = discord.Embed(title = "Disabling all logs", description = "Are you sure that you want to disable all logs in this server?", color = discord.Colour.red())
        await interaction.response.send_message(embed = embed, view = ConfirmDisableAll(), ephemeral=True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)

# Logs Class
class Logs(commands.GroupCog, name = "log"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Logs is online.")

    # Defining sub-groups
    messages_group = app_commands.Group(name = "message", description = "Log messages")
    roles_group = app_commands.Group(name = "role", description = "Log roles")
    members_group = app_commands.Group(name = "member", description = "Log member")
    channels_group = app_commands.Group(name = "channel", description = "Log channels")

    # show settings command
    @app_commands.command(name = "show_settings", description = "Show current settings for all logs commands.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def show_settings(self, interaction: discord.Interaction):
        log_channels_list = []
        logs_files_list = ["channel_create", "channel_delete", "channel_updates", "member_ban", "member_unban", "member_timeout", "nickname_change",
                           "messages_edits", "messages_deletes", "role_create", "role_delete", "role_updates", "role_given", "role_remove",
                           "server_updates", "joins", "leaves"]
        is_all_disabled = True
        for log_file in logs_files_list:
            async with aiosqlite.connect(f"db/log_{log_file}.db") as db:
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                    await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data: log_channels_list.append(self.bot.get_channel(data[0]).mention)
                    else: log_channels_list.append("Disabled")
        embed = discord.Embed(title = "Logs Settings", description = "All current settings", color = 0x000000)
        embed.add_field(name = "Channel Create", value = log_channels_list[0])
        embed.add_field(name = "Channel Delete", value = log_channels_list[1])
        embed.add_field(name = "Channel Updates", value = log_channels_list[2])
        embed.add_field(name = "Member Ban", value = log_channels_list[3])
        embed.add_field(name = "Member Unban", value = log_channels_list[4])
        embed.add_field(name = "Member Timeout", value = log_channels_list[5])
        embed.add_field(name = "Member Nickname", value = log_channels_list[6])
        embed.add_field(name = "Message Edits", value = log_channels_list[7])
        embed.add_field(name = "Message Deletes", value = log_channels_list[8])
        embed.add_field(name = "Role Create", value = log_channels_list[9])
        embed.add_field(name = "Role Delete", value = log_channels_list[10])
        embed.add_field(name = "Role Updates", value = log_channels_list[11])
        embed.add_field(name = "Role Given", value = log_channels_list[12])
        embed.add_field(name = "Role Remove", value = log_channels_list[13])
        embed.add_field(name = "Server Updates", value = log_channels_list[14])
        embed.add_field(name = "Joins", value = log_channels_list[15])
        embed.add_field(name = "Leaves", value = log_channels_list[16])
        await interaction.response.send_message(embed = embed, view = DisableAll())

    #joins command
    @app_commands.command(name = "joins", description = "Log members' joins and send them to a channel.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(switch = "Enable/Disable log.", channel = "Channel to send the log.")
    @app_commands.choices(switch = [app_commands.Choice(name = "enable", value = "enable"), app_commands.Choice(name = "disable", value = "disable")])
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def joins(self, interaction: discord.Interaction, switch: app_commands.Choice[str], channel: discord.TextChannel = None):
        if switch.value == "disable":
            async with aiosqlite.connect("db/log_joins.db") as db: # Open the db
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                    await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data: 
                        await cursor.execute("DELETE FROM log WHERE guild = ?", (interaction.guild.id,))
                        embed = discord.Embed(title = "📝 ┃ Joins Log", description = "Your members' joins log has been disabled succesfully.", color = 0x000000)
                        await interaction.response.send_message(embed = embed)
                    else:
                        await interaction.response.send_message("Members' joins log is already disabled in your server.", ephemeral = True)
                await db.commit()
        if switch.value == "enable":
            if channel == None: return await interaction.response.send_message("You must include a channel to set the log.", ephemeral = True)
            global joins_channel
            joins_channel = channel.id
            view = joinsConfirm()
            em = discord.Embed(title = "Confirmation",
            description = f"Are you sure that you want {channel.mention} to be your joins log channel?",
            colour = 0x2F3136)
            await interaction.response.send_message(embed = em, view = view)

    #leaves command
    @app_commands.command(name = "leaves", description = "Log members' leaves and send them to a channel.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(switch = "Enable/Disable log.", channel = "Channel to send the log.")
    @app_commands.choices(switch = [app_commands.Choice(name = "enable", value = "enable"), app_commands.Choice(name = "disable", value = "disable")])
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def leaves(self, interaction: discord.Interaction, switch: app_commands.Choice[str], channel: discord.TextChannel = None):
        if switch.value == "disable":
            async with aiosqlite.connect("db/log_leaves.db") as db: # Open the db
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                    await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data: 
                        await cursor.execute("DELETE FROM log WHERE guild = ?", (interaction.guild.id,))
                        embed = discord.Embed(title = "📝 ┃ Leaves Log", description = "Your members' leaves log has been disabled succesfully.", color = 0x000000)
                        await interaction.response.send_message(embed = embed)
                    else:
                        await interaction.response.send_message("Members' joins log is already disabled in your server.", ephemeral = True)
                await db.commit()
        if switch.value == "enable":
            if channel == None: return await interaction.response.send_message("You must include a channel to set the log.", ephemeral = True)
            global leaves_channel
            leaves_channel = channel.id
            view = leavesConfirm()
            em = discord.Embed(title = "Confirmation",
            description = f"Are you sure that you want {channel.mention} to be your leaves log channel?",
            colour = 0x2F3136)
            await interaction.response.send_message(embed = em, view = view)

    #log msg edit command
    @messages_group.command(name = "edits", description = "Log edited messages and send them to a channel.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(switch = "Enable/Disable log.", channel = "Channel to send the log.")
    @app_commands.choices(switch = [app_commands.Choice(name = "enable", value = "enable"), app_commands.Choice(name = "disable", value = "disable")])
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def msg_edits(self, interaction: discord.Interaction, switch: app_commands.Choice[str], channel: discord.TextChannel = None):
        if switch.value == "disable":
            async with aiosqlite.connect("db/log_messages_edits.db") as db: # Open the db
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                    await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data: 
                        await cursor.execute("DELETE FROM log WHERE guild = ?", (interaction.guild.id,))
                        embed = discord.Embed(title = "📝 ┃ Edited Messages Log", description = "Your edited messages log has been disabled succesfully.", color = 0x000000)
                        await interaction.response.send_message(embed = embed)
                    else:
                        await interaction.response.send_message("Edited messages' log is already disabled in your server.", ephemeral = True)
                await db.commit()
        if switch.value == "enable":
            if channel == None: return await interaction.response.send_message("You must include a channel to set the log.", ephemeral = True)
            global edits_log_channel
            edits_log_channel = channel.id
            view = editsConfirm()
            em = discord.Embed(title = "Confirmation",
            description = f"Are you sure that you want {channel.mention} to be your edited messages log channel?",
            colour = 0x2F3136)
            await interaction.response.send_message(embed = em, view = view)

    #log msg delete command
    @messages_group.command(name = "deletes", description = "Log deleted messages and send them to a channel.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(switch = "Enable/Disable log.", channel = "Channel to send the log.")
    @app_commands.choices(switch = [app_commands.Choice(name = "enable", value = "enable"), app_commands.Choice(name = "disable", value = "disable")])
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def msg_deletes(self, interaction: discord.Interaction, switch: app_commands.Choice[str], channel: discord.TextChannel = None):
        if switch.value == "disable":
            async with aiosqlite.connect("db/log_messages_deletes.db") as db: # Open the db
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                    await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data: 
                        await cursor.execute("DELETE FROM log WHERE guild = ?", (interaction.guild.id,))
                        embed = discord.Embed(title = "📝 ┃ Deleted Messages Log", description = "Your deleted messages log has been disabled succesfully.", color = 0x000000)
                        await interaction.response.send_message(embed = embed)
                    else:
                        await interaction.response.send_message("Deleted messages' log is already disabled in your server.", ephemeral = True)
                await db.commit()
        if switch.value == "enable":
            if channel == None: return await interaction.response.send_message("You must include a channel to set the log.", ephemeral = True)
            global deletes_log_channel
            deletes_log_channel = channel.id
            view = deletesConfirm()
            em = discord.Embed(title = "Confirmation",
            description = f"Are you sure that you want {channel.mention} to be your deleted messages log channel?",
            colour = 0x2F3136)
            await interaction.response.send_message(embed = em, view = view)

    # role create command
    @roles_group.command(name = "create", description = "Log roles when created.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(switch = "Enable/Disable log.", channel = "Channel to send the log.")
    @app_commands.choices(switch = [app_commands.Choice(name = "enable", value = "enable"), app_commands.Choice(name = "disable", value = "disable")])
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def role_create(self, interaction: discord.Interaction, switch: app_commands.Choice[str], channel: discord.TextChannel = None):
        if switch.value == "disable":
            async with aiosqlite.connect("db/log_role_create.db") as db: # Open the db
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                    await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data:
                        await cursor.execute("DELETE FROM log WHERE guild = ?", (interaction.guild.id,))
                        embed = discord.Embed(title = "📝 ┃ Role Create Log", description = "Your role created log has been disabled succesfully.", color = 0x000000)
                        await interaction.response.send_message(embed = embed)
                    else:
                        await interaction.response.send_message("Roles create log is already disabled in your server.", ephemeral = True)
                await db.commit()
        if switch.value == "enable":
            if channel == None: return await interaction.response.send_message("You must include a channel to set the log.", ephemeral = True)
            global roles_create_channel
            roles_create_channel = channel.id
            view = roleCreateConfirm()
            em = discord.Embed(title = "Confirmation",
            description = f"Are you sure that you want {channel.mention} to be your roles create log channel?",
            colour = 0x2F3136)
            await interaction.response.send_message(embed = em, view = view)

    # role delete command
    @roles_group.command(name = "delete", description = "Log roles when deleted.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(switch = "Enable/Disable log.", channel = "Channel to send the log.")
    @app_commands.choices(switch = [app_commands.Choice(name = "enable", value = "enable"), app_commands.Choice(name = "disable", value = "disable")])
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def role_delete(self, interaction: discord.Interaction, switch: app_commands.Choice[str], channel: discord.TextChannel = None):
        if switch.value == "disable":
            async with aiosqlite.connect("db/log_role_delete.db") as db: # Open the db
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                    await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data:
                        await cursor.execute("DELETE FROM log WHERE guild = ?", (interaction.guild.id,))
                        embed = discord.Embed(title = "📝 ┃ Role Delete Log", description = "Your role deleted log has been disabled succesfully.", color = 0x000000)
                        await interaction.response.send_message(embed = embed)
                    else:
                        await interaction.response.send_message("Roles delete log is already disabled in your server.", ephemeral = True)
                await db.commit()
        if switch.value == "enable":
            if channel == None: return await interaction.response.send_message("You must include a channel to set the log.", ephemeral = True)
            global roles_delete_channel
            roles_delete_channel = channel.id
            view = roleDeleteConfirm()
            em = discord.Embed(title = "Confirmation",
            description = f"Are you sure that you want {channel.mention} to be your roles delete log channel?",
            colour = 0x2F3136)
            await interaction.response.send_message(embed = em, view = view)

    # role update command
    @roles_group.command(name = "updates", description = "Log roles when updated. (name, permissions)")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(switch = "Enable/Disable log.", channel = "Channel to send the log.")
    @app_commands.choices(switch = [app_commands.Choice(name = "enable", value = "enable"), app_commands.Choice(name = "disable", value = "disable")])
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def role_update(self, interaction: discord.Interaction, switch: app_commands.Choice[str], channel: discord.TextChannel = None):
        if switch.value == "disable":
            async with aiosqlite.connect("db/log_role_updates.db") as db: # Open the db
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                    await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data:
                        await cursor.execute("DELETE FROM log WHERE guild = ?", (interaction.guild.id,))
                        embed = discord.Embed(title = "📝 ┃ Role Updates Log", description = "Your role updates log has been disabled succesfully.", color = 0x000000)
                        await interaction.response.send_message(embed = embed)
                    else:
                        await interaction.response.send_message("Roles updates log is already disabled in your server.", ephemeral = True)
                await db.commit()
        if switch.value == "enable":
            if channel == None: return await interaction.response.send_message("You must include a channel to set the log.", ephemeral = True)
            global roles_updates_channel
            roles_updates_channel = channel.id
            view = roleUpdatesConfirm()
            em = discord.Embed(title = "Confirmation",
            description = f"Are you sure that you want {channel.mention} to be your roles updates log channel?",
            colour = 0x2F3136)
            await interaction.response.send_message(embed = em, view = view)

    # role given command
    @roles_group.command(name = "given", description = "Log roles when given to a member.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(switch = "Enable/Disable log.", channel = "Channel to send the log.")
    @app_commands.choices(switch = [app_commands.Choice(name = "enable", value = "enable"), app_commands.Choice(name = "disable", value = "disable")])
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def role_given(self, interaction: discord.Interaction, switch: app_commands.Choice[str], channel: discord.TextChannel = None):
        if switch.value == "disable":
            async with aiosqlite.connect("db/log_role_given.db") as db: # Open the db
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                    await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data:
                        await cursor.execute("DELETE FROM log WHERE guild = ?", (interaction.guild.id,))
                        embed = discord.Embed(title = "📝 ┃ Role Given Log", description = "Your given role log has been disabled succesfully.", color = 0x000000)
                        await interaction.response.send_message(embed = embed)
                    else:
                        await interaction.response.send_message("Roles given log is already disabled in your server.", ephemeral = True)
                await db.commit()
        if switch.value == "enable":
            if channel == None: return await interaction.response.send_message("You must include a channel to set the log.", ephemeral = True)
            global roles_given_channel
            roles_given_channel = channel.id
            view = roleGivenConfirm()
            em = discord.Embed(title = "Confirmation",
            description = f"Are you sure that you want {channel.mention} to be your roles given log channel?",
            colour = 0x2F3136)
            await interaction.response.send_message(embed = em, view = view)

    # role removed command
    @roles_group.command(name = "remove", description = "Log roles when remove from a member.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(switch = "Enable/Disable log.", channel = "Channel to send the log.")
    @app_commands.choices(switch = [app_commands.Choice(name = "enable", value = "enable"), app_commands.Choice(name = "disable", value = "disable")])
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def role_remove(self, interaction: discord.Interaction, switch: app_commands.Choice[str], channel: discord.TextChannel = None):
        if switch.value == "disable":
            async with aiosqlite.connect("db/log_role_remove.db") as db: # Open the db
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                    await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data:
                        await cursor.execute("DELETE FROM log WHERE guild = ?", (interaction.guild.id,))
                        embed = discord.Embed(title = "📝 ┃ Role Removed Log", description = "Your removed role log has been disabled succesfully.", color = 0x000000)
                        await interaction.response.send_message(embed = embed)
                    else:
                        await interaction.response.send_message("Roles removed log is already disabled in your server.", ephemeral = True)
                await db.commit()
        if switch.value == "enable":
            if channel == None: return await interaction.response.send_message("You must include a channel to set the log.", ephemeral = True)
            global roles_removed_channel
            roles_removed_channel = channel.id
            view = roleRemoveConfirm()
            em = discord.Embed(title = "Confirmation",
            description = f"Are you sure that you want {channel.mention} to be your roles removed log channel?",
            colour = 0x2F3136)
            await interaction.response.send_message(embed = em, view = view)

    # member ban command
    @members_group.command(name = "ban", description = "Log member bans.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(switch = "Enable/Disable log.", channel = "Channel to send the log.")
    @app_commands.choices(switch = [app_commands.Choice(name = "enable", value = "enable"), app_commands.Choice(name = "disable", value = "disable")])
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def memebr_ban(self, interaction: discord.Interaction, switch: app_commands.Choice[str], channel: discord.TextChannel = None):
        if switch.value == "disable":
            async with aiosqlite.connect("db/log_member_ban.db") as db: # Open the db
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                    await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data:
                        await cursor.execute("DELETE FROM log WHERE guild = ?", (interaction.guild.id,))
                        embed = discord.Embed(title = "📝 ┃ Member Ban Log", description = "Your member ban log has been disabled succesfully.", color = 0x000000)
                        await interaction.response.send_message(embed = embed)
                    else:
                        await interaction.response.send_message("Member ban log is already disabled in your server.", ephemeral = True)
                await db.commit()
        if switch.value == "enable":
            if channel == None: return await interaction.response.send_message("You must include a channel to set the log.", ephemeral = True)
            global member_ban_channel
            member_ban_channel = channel.id
            view = memberBanConfirm()
            em = discord.Embed(title = "Confirmation",
            description = f"Are you sure that you want {channel.mention} to be your member ban log channel?",
            colour = 0x2F3136)
            await interaction.response.send_message(embed = em, view = view)

    # member unban command
    @members_group.command(name = "unban", description = "Log member unbans.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(switch = "Enable/Disable log.", channel = "Channel to send the log.")
    @app_commands.choices(switch = [app_commands.Choice(name = "enable", value = "enable"), app_commands.Choice(name = "disable", value = "disable")])
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def memebr_unban(self, interaction: discord.Interaction, switch: app_commands.Choice[str], channel: discord.TextChannel = None):
        if switch.value == "disable":
            async with aiosqlite.connect("db/log_member_unban.db") as db: # Open the db
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                    await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data:
                        await cursor.execute("DELETE FROM log WHERE guild = ?", (interaction.guild.id,))
                        embed = discord.Embed(title = "📝 ┃ Member Unban Log", description = "Your member unban log has been disabled succesfully.", color = 0x000000)
                        await interaction.response.send_message(embed = embed)
                    else:
                        await interaction.response.send_message("Member unban log is already disabled in your server.", ephemeral = True)
                await db.commit()
        if switch.value == "enable":
            if channel == None: return await interaction.response.send_message("You must include a channel to set the log.", ephemeral = True)
            global member_unban_channel
            member_unban_channel = channel.id
            view = memberUnbanConfirm()
            em = discord.Embed(title = "Confirmation",
            description = f"Are you sure that you want {channel.mention} to be your member unban log channel?",
            colour = 0x2F3136)
            await interaction.response.send_message(embed = em, view = view)

    # member timeout command
    @members_group.command(name = "timeout", description = "Log member timeout.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(switch = "Enable/Disable log.", channel = "Channel to send the log.")
    @app_commands.choices(switch = [app_commands.Choice(name = "enable", value = "enable"), app_commands.Choice(name = "disable", value = "disable")])
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def memebr_timeout(self, interaction: discord.Interaction, switch: app_commands.Choice[str], channel: discord.TextChannel = None):
        if switch.value == "disable":
            async with aiosqlite.connect("db/log_member_timeout.db") as db: # Open the db
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                    await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data:
                        await cursor.execute("DELETE FROM log WHERE guild = ?", (interaction.guild.id,))
                        embed = discord.Embed(title = "📝 ┃ Member Timeout Log", description = "Your member timeout log has been disabled succesfully.", color = 0x000000)
                        await interaction.response.send_message(embed = embed)
                    else:
                        await interaction.response.send_message("Member timeout log is already disabled in your server.", ephemeral = True)
                await db.commit()
        if switch.value == "enable":
            if channel == None: return await interaction.response.send_message("You must include a channel to set the log.", ephemeral = True)
            global member_timeout_channel
            member_timeout_channel = channel.id
            view = memberTimeoutConfirm()
            em = discord.Embed(title = "Confirmation",
            description = f"Are you sure that you want {channel.mention} to be your member timeout log channel?",
            colour = 0x2F3136)
            await interaction.response.send_message(embed = em, view = view)

    # nickname change command
    @members_group.command(name = "nickname", description = "Log nickname change.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(switch = "Enable/Disable log.", channel = "Channel to send the log.")
    @app_commands.choices(switch = [app_commands.Choice(name = "enable", value = "enable"), app_commands.Choice(name = "disable", value = "disable")])
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def nickname_change(self, interaction: discord.Interaction, switch: app_commands.Choice[str], channel: discord.TextChannel = None):
        if switch.value == "disable":
            async with aiosqlite.connect("db/log_nickname_change.db") as db: # Open the db
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                    await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data:
                        await cursor.execute("DELETE FROM log WHERE guild = ?", (interaction.guild.id,))
                        embed = discord.Embed(title = "📝 ┃ Nickname Change Log", description = "Your nickname change log has been disabled succesfully.", color = 0x000000)
                        await interaction.response.send_message(embed = embed)
                    else:
                        await interaction.response.send_message("Nickname change log is already disabled in your server.", ephemeral = True)
                await db.commit()
        if switch.value == "enable":
            if channel == None: return await interaction.response.send_message("You must include a channel to set the log.", ephemeral = True)
            global nickname_change_channel
            nickname_change_channel = channel.id
            view = nicknameChangeConfirm()
            em = discord.Embed(title = "Confirmation",
            description = f"Are you sure that you want {channel.mention} to be your nickname change log channel?",
            colour = 0x2F3136)
            await interaction.response.send_message(embed = em, view = view)

    # channel create command
    @channels_group.command(name = "create", description = "Log channel create.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(switch = "Enable/Disable log.", channel = "Channel to send the log.")
    @app_commands.choices(switch = [app_commands.Choice(name = "enable", value = "enable"), app_commands.Choice(name = "disable", value = "disable")])
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def channel_create(self, interaction: discord.Interaction, switch: app_commands.Choice[str], channel: discord.TextChannel = None):
        if switch.value == "disable":
            async with aiosqlite.connect("db/log_channel_create.db") as db: # Open the db
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                    await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data:
                        await cursor.execute("DELETE FROM log WHERE guild = ?", (interaction.guild.id,))
                        embed = discord.Embed(title = "📝 ┃ Channel Create Log", description = "Your channel create log has been disabled succesfully.", color = 0x000000)
                        await interaction.response.send_message(embed = embed)
                    else:
                        await interaction.response.send_message("Channel create log is already disabled in your server.", ephemeral = True)
                await db.commit()
        if switch.value == "enable":
            if channel == None: return await interaction.response.send_message("You must include a channel to set the log.", ephemeral = True)
            global channel_create_channel
            channel_create_channel = channel.id
            view = channelCreateConfirm()
            em = discord.Embed(title = "Confirmation",
            description = f"Are you sure that you want {channel.mention} to be your channel create log channel?",
            colour = 0x2F3136)
            await interaction.response.send_message(embed = em, view = view)

    # channel delete command
    @channels_group.command(name = "delete", description = "Log channel delete.")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(switch = "Enable/Disable log.", channel = "Channel to send the log.")
    @app_commands.choices(switch = [app_commands.Choice(name = "enable", value = "enable"), app_commands.Choice(name = "disable", value = "disable")])
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def channel_delete(self, interaction: discord.Interaction, switch: app_commands.Choice[str], channel: discord.TextChannel = None):
        if switch.value == "disable":
            async with aiosqlite.connect("db/log_channel_delete.db") as db: # Open the db
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                    await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data:
                        await cursor.execute("DELETE FROM log WHERE guild = ?", (interaction.guild.id,))
                        embed = discord.Embed(title = "📝 ┃ Channel Delete Log", description = "Your channel delete log has been disabled succesfully.", color = 0x000000)
                        await interaction.response.send_message(embed = embed)
                    else:
                        await interaction.response.send_message("Channel delete log is already disabled in your server.", ephemeral = True)
                await db.commit()
        if switch.value == "enable":
            if channel == None: return await interaction.response.send_message("You must include a channel to set the log.", ephemeral = True)
            global channel_delete_channel
            channel_delete_channel = channel.id
            view = channelDeleteConfirm()
            em = discord.Embed(title = "Confirmation",
            description = f"Are you sure that you want {channel.mention} to be your channel delete log channel?",
            colour = 0x2F3136)
            await interaction.response.send_message(embed = em, view = view)

    # channel updates command
    @channels_group.command(name = "updates", description = "Log channel updates. (name, permissions)")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(switch = "Enable/Disable log.", channel = "Channel to send the log.")
    @app_commands.choices(switch = [app_commands.Choice(name = "enable", value = "enable"), app_commands.Choice(name = "disable", value = "disable")])
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def channel_updates(self, interaction: discord.Interaction, switch: app_commands.Choice[str], channel: discord.TextChannel = None):
        if switch.value == "disable":
            async with aiosqlite.connect("db/log_channel_updates.db") as db: # Open the db
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                    await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data:
                        await cursor.execute("DELETE FROM log WHERE guild = ?", (interaction.guild.id,))
                        embed = discord.Embed(title = "📝 ┃ Channel Updates Log", description = "Your channel updates log has been disabled succesfully.", color = 0x000000)
                        await interaction.response.send_message(embed = embed)
                    else:
                        await interaction.response.send_message("Channel updates log is already disabled in your server.", ephemeral = True)
                await db.commit()
        if switch.value == "enable":
            if channel == None: return await interaction.response.send_message("You must include a channel to set the log.", ephemeral = True)
            global channel_updates_channel
            channel_updates_channel = channel.id
            view = channelUpdatesConfirm()
            em = discord.Embed(title = "Confirmation",
            description = f"Are you sure that you want {channel.mention} to be your channel updates log channel?",
            colour = 0x2F3136)
            await interaction.response.send_message(embed = em, view = view)

    # server updates command
    @app_commands.command(name = "server_updates", description = "Log server updates. (name, icon)")
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(switch = "Enable/Disable log.", channel = "Channel to send the log.")
    @app_commands.choices(switch = [app_commands.Choice(name = "enable", value = "enable"), app_commands.Choice(name = "disable", value = "disable")])
    @app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
    async def server_updates(self, interaction: discord.Interaction, switch: app_commands.Choice[str], channel: discord.TextChannel = None):
        if switch.value == "disable":
            async with aiosqlite.connect("db/log_server_updates.db") as db: # Open the db
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                    await cursor.execute("SELECT channel FROM log WHERE guild = ?", (interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data:
                        await cursor.execute("DELETE FROM log WHERE guild = ?", (interaction.guild.id,))
                        embed = discord.Embed(title = "📝 ┃ Server Updates Log", description = "Your server updates log has been disabled succesfully.", color = 0x000000)
                        await interaction.response.send_message(embed = embed)
                    else:
                        await interaction.response.send_message("Channel updates log is already disabled in your server.", ephemeral = True)
                await db.commit()
        if switch.value == "enable":
            if channel == None: return await interaction.response.send_message("You must include a channel to set the log.", ephemeral = True)
            global server_updates_channel
            server_updates_channel = channel.id
            view = serverUpdatesConfirm()
            em = discord.Embed(title = "Confirmation",
            description = f"Are you sure that you want {channel.mention} to be your server updates log channel?",
            colour = 0x2F3136)
            await interaction.response.send_message(embed = em, view = view)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Logs(bot))