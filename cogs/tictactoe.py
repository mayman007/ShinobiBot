from typing import List
from discord.ext import commands
import discord
from discord import app_commands


class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        super().__init__(style = discord.ButtonStyle.secondary, label = '\u200b', row = y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed
    # This is part of the "meat" of the game logic
    async def callback(self, interaction: discord.Interaction):
        global player1
        global player2
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return
        if view.current_player == view.X:
            if interaction.user != player1:
                await interaction.response.send_message("It's not your Turn!", ephemeral = True)
            else:
                self.style = discord.ButtonStyle.danger
                self.label = 'X'
                self.disabled = True
                view.board[self.y][self.x] = view.X
                view.current_player = view.O
                content = f"It is now {player2.mention}'s turn **O**"
        else:
            if interaction.user != player2:
                await interaction.response.send_message("It's not your Turn!", ephemeral = True)
            else:
                self.style = discord.ButtonStyle.success
                self.label = 'O'
                self.disabled = True
                view.board[self.y][self.x] = view.O
                view.current_player = view.X
                content = f"It is now {player1.mention}'s turn **X**"
        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = f'{player1.mention} **X** won!'
            elif winner == view.O:
                content = f'{player2.mention} **O** won!'
            else:
                content = "It's a tie!"
            for child in view.children:
                child.disabled = True
            view.stop()
        await interaction.response.edit_message(content = content, view = view)

# This is our actual board View
class TicTacToe(discord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons
    # This is not required
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2
    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner -- it is used by the TicTacToeButton
    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X
        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X
        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie
        return None

class tictactoe(commands.Cog):
    def __init__(self, client):
        self.client = client

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("TicTacToe is online.")

    # tictactoe command
    @app_commands.command(name = "tictactoe", description = "Play TicTacToe.")
    @app_commands.describe(enemy = "Player to challenge.")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def tictactoe(self, interation: discord.Interaction, enemy: discord.Member):
        await interation.response.send_message(f"Tic Tac Toe: {interation.user.mention} goes first **X**", view = TicTacToe())
        global player1, player2
        player1 = interation.user
        player2 = enemy

async def setup(bot: commands.Bot):
   await bot.add_cog(tictactoe(bot))