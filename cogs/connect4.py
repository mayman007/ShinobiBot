import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from typing import Union
from itertools import groupby, chain


class Board(list):
	__slots__ = frozenset({'width', 'height'})
	def __init__(self, width, height, player1_name=None, player2_name=None):
		self.width = width
		self.height = height
		for x in range(width):
			self.append([0] * height)

	def __getitem__(self, pos: Union[int, tuple]):
		if isinstance(pos, int):
			return list(self)[pos]
		elif isinstance(pos, tuple):
			x, y = pos
			return list(self)[x][y]
		else:
			raise TypeError('pos must be an int or tuple')

	def __setitem__(self, pos: Union[int, tuple], new_value):
		x, y = self._xy(pos)
		if self[x, y] != 0:
			raise IndexError("there's already a move at that position")
		# basically self[x][y] = new_value
		# super().__getitem__(x).__setitem__(y, new_value)
		self[x][y] = new_value

	def _xy(self, pos):
		if isinstance(pos, tuple):
			return pos[0], pos[1]
		elif isinstance(pos, int):
			x = pos
			return x, self._y(x)
		else:
			raise TypeError('pos must be an int or tuple')

	def _y(self, x):
		"""find the lowest empty row for column x"""
		# start from the bottom and work up
		for y in range(self.height-1, -1, -1):
			if self[x, y] == 0:
				return y
		raise ValueError('that column is full')

	def _pos_diagonals(self):
		"""Get positive diagonals, going from bottom-left to top-right."""
		for di in ([(j, i - j) for j in range(self.width)] for i in range(self.width + self.height - 1)):
			yield [self[i, j] for i, j in di if i >= 0 and j >= 0 and i < self.width and j < self.height]

	def _neg_diagonals(self):
		"""Get negative diagonals, going from top-left to bottom-right."""
		for di in ([(j, i - self.width + j + 1) for j in range(self.height)] for i in range(self.width + self.height - 1)):
			yield [self[i, j] for i, j in di if i >= 0 and j >= 0 and i < self.width and j < self.height]

	def _full(self):
		"""is there a move in every position?"""
		for x in range(self.width):
			if self[x, 0] == 0:
				return False
		return True

class Connect4Game:
	__slots__ = frozenset({'board', 'turn_count', '_whomst_forfeited', 'names'})
	FORFEIT = -2
	TIE = -1
	NO_WINNER = 0
	PIECES = (
		'\N{medium white circle}'
		'\N{large red circle}'
		'\N{large blue circle}'
	)

	def __init__(self, player1_name=None, player2_name=None):
		if player1_name is not None and player2_name is not None:
			self.names = (player1_name, player2_name)
		else:
			self.names = ('Player 1', 'Player 2')
		self.board = Board(7, 6)
		self.turn_count = 0
		self._whomst_forfeited = 0

	def move(self, column):
		self.board[column] = self.whomst_turn()
		self.turn_count += 1

	def forfeit(self):
		"""forfeit the game as the current player"""
		self._whomst_forfeited = self.whomst_turn_name()

	def _get_forfeit_status(self):
		if self._whomst_forfeited:
			status = '{} won ({} forfeited)\n'
			return status.format(
				self.other_player_name(),
				self.whomst_turn_name()
			)
		raise ValueError('nobody has forfeited')

	def __str__(self):
		win_status = self.whomst_won()
		status = self._get_status()
		instructions = ''
		if win_status == self.NO_WINNER:
			instructions = self._get_instructions()
		elif win_status == self.FORFEIT:
			status = self._get_forfeit_status()
		return (
			status
			+ instructions
			+ '\n'.join(self._format_row(y) for y in range(self.board.height))
		)

	def _get_status(self):
		win_status = self.whomst_won()
		if win_status == self.NO_WINNER:
			status = (self.whomst_turn_name() + "'s turn"
				+ self.PIECES[self.whomst_turn()])
		elif win_status == self.TIE:
			status = "It's a tie!"
		elif win_status == self.FORFEIT:
			status = self._get_forfeit_status()
		else:
			status = self._get_player_name(win_status) + ' won!'
		return status + '\n'

	def _get_instructions(self):
		instructions = ''
		for i in range(1, self.board.width+1):
			instructions += str(i) + '\N{combining enclosing keycap}'
		return instructions + '\n'

	def _format_row(self, y):
		return ''.join(self[x, y] for x in range(self.board.width))

	def __getitem__(self, pos):
		x, y = pos
		return self.PIECES[self.board[x, y]]

	def whomst_won(self):
		"""Get the winner on the current board.
		If there's no winner yet, return Connect4Game.NO_WINNER.
		If it's a tie, return Connect4Game.TIE"""
		lines = (
			self.board, # columns
			zip(*self.board), # rows (zip picks the nth item from each column)
			self.board._pos_diagonals(), # positive diagonals
			self.board._neg_diagonals(), # negative diagonals
		)
		if self._whomst_forfeited:
			return self.FORFEIT
		for line in chain(*lines):
			for player, group in groupby(line):
				if player != 0 and len(list(group)) >= 4:
					return player
		if self.board._full():
			return self.TIE
		else:
			return self.NO_WINNER

	def other_player_name(self):
		self.turn_count += 1
		other_player_name = self.whomst_turn_name()
		self.turn_count -= 1
		return other_player_name

	def whomst_turn_name(self):
		return self._get_player_name(self.whomst_turn())

	def whomst_turn(self):
		return self.turn_count%2+1

	def _get_player_name(self, player_number):
		player_number -= 1 # these lists are 0-indexed but the players aren't
		return self.names[player_number]

class Connect4(commands.Cog):
	CANCEL_GAME_EMOJI = '🚫'
	DIGITS = [str(digit) + '\N{combining enclosing keycap}' for digit in range(1, 8)] + ['🚫']
	VALID_REACTIONS = [CANCEL_GAME_EMOJI] + DIGITS
	GAME_TIMEOUT_THRESHOLD = 600

	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

	#wakin~
	@commands.Cog.listener()
	async def on_ready(self):
		print("Connect 4 is online.")

  	#CONNECT4
	@app_commands.command(name = "connect4", description = "play connect 4.")
	@app_commands.describe(player2 = "Player to challenge.")
	@app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
	async def connect4(self, interaction: discord.Interaction, player2: discord.Member):
		"""
		Play connect4 with another player
		"""
		player1 = interaction.user
		game = Connect4Game(
			player1.mention,
			player2.mention
		)
		await interaction.response.send_message("Game Started!", ephemeral = True)
		message = await interaction.channel.send(str(game))
		for digit in self.DIGITS:
			await message.add_reaction(digit)
		def check(reaction, user):
			return (
				user == (player1, player2)[game.whomst_turn()-1]
				and str(reaction) in self.VALID_REACTIONS
				and reaction.message.id == message.id
			)
		while game.whomst_won() == game.NO_WINNER:
			try:
				reaction, user = await self.bot.wait_for(
					'reaction_add',
					check=check,
					timeout=self.GAME_TIMEOUT_THRESHOLD
				)
			except asyncio.TimeoutError:
				game.forfeit()
				await message.reply("> Game was ended due to running out of time!")
				break
			await asyncio.sleep(0.2)
			try:
				await message.remove_reaction(reaction, user)
			except discord.errors.Forbidden:
				pass
			if str(reaction) == self.CANCEL_GAME_EMOJI:
				game.forfeit()
				break
			try:
				# convert the reaction to a 0-indexed int and move in that column
				game.move(self.DIGITS.index(str(reaction)))
			except ValueError:
				pass # the column may be full
			await message.edit(content=str(game))
		await self.end_game(game, message)

	@classmethod
	async def end_game(cls, game, message):
		await message.edit(content=str(game))
		await cls.clear_reactions(message)

	@staticmethod
	async def clear_reactions(message):
		try:
			await message.clear_reactions()
		except discord.HTTPException:
			pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Connect4(bot))