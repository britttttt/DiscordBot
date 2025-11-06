import asyncio
from discord.ext import commands


ALL_SPACES = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
X, O, BLANK = 'X', 'O', ' '

def getBlankBoard():
    """Create a new, blank tic-tac-toe board"""
    board = {space: BLANK for space in ALL_SPACES}
    return board

def getBoardStr(board):
    """Return a text-representation of the board"""
    return (
        f"{board['1']}|{board['2']}|{board['3']}    1 2 3\n"
        f"-+-+-    -+-+-\n"
        f"{board['4']}|{board['5']}|{board['6']}    4 5 6\n"
        f"-+-+-    -+-+-\n"
        f"{board['7']}|{board['8']}|{board['9']}    7 8 9"
    )

def isValidSpace(board, space):
    """Returns True if the space is a valid space number and the space is blank."""
    return (isinstance(space, str)
            and space in ALL_SPACES
            and board.get(space) == BLANK)

def isWinner(board, player):
    """Return True if player is a winner on this TicTacToeBoard"""
    b, p = board, player
    return ((b['1'] == b['2'] == b['3'] == p) or
            (b['4'] == b['5'] == b['6'] == p) or
            (b['7'] == b['8'] == b['9'] == p) or
            (b['1'] == b['4'] == b['7'] == p) or
            (b['2'] == b['5'] == b['8'] == p) or
            (b['3'] == b['6'] == b['9'] == p) or
            (b['3'] == b['5'] == b['7'] == p) or
            (b['1'] == b['5'] == b['9'] == p))

def isBoardFull(board):
    """Return True if every space on the board has been taken."""
    for space in ALL_SPACES:
        if board[space] == BLANK:
            return False
    return True

def updateBoard(board, space, mark):
    """Sets the space on the board to mark."""
    board[space] = mark


class TicTacToe(commands.Cog):
    """TicTacToe commands and helpers"""

    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}

    @commands.command(name="tictactoe", aliases=["ttt"])
    async def start_tictactoe(self, ctx):
        """Start a new TicTacToe game in this channel."""
        channel_id = ctx.channel.id
        if channel_id in self.active_games:
            await ctx.send("A game is already active in this channel — Type `!move <position>` to play or `!endgame` to end it.")
            return
        
        board = getBlankBoard()
        self.active_games[channel_id] = {
            "board": board, 
            "turn": X, 
            "players": [ctx.author.id, None]
        }
        await ctx.send(
            f"TicTacToe started by {ctx.author.mention}! Positions are 1-9:\n"
            f"```{getBoardStr(board)}```\n"
            f"{ctx.author.mention} is **X**. Use `!move <pos>` to play (e.g. `!move 5`)."
        )

    @commands.command(name="move")
    async def move(self, ctx, position: str):
        """Make a move in the active TicTacToe game."""
        channel_id = ctx.channel.id
        game = self.active_games.get(channel_id)
        
        if not game:
            await ctx.send("No active game in this channel. Start a game with `!tictactoe`")
            return
        
        position = position.strip()
        if position not in ALL_SPACES:
            await ctx.send("Invalid move — choose a number 1-9")
            return
        
        board = game["board"]
        if not isValidSpace(board, position):
            await ctx.send("That space is taken — choose another space")
            return
        
        starter_id, other_id = game["players"]
        author_id = ctx.author.id
        
        if author_id == starter_id:
            player_index = 0
        elif other_id is None:
            # First player other than the starter becomes player 1 (O)
            game["players"][1] = author_id
            player_index = 1
        elif author_id == other_id:
            player_index = 1
        else:
            await ctx.send("This game is full! Only the two players can make moves.")
            return
        

        current_turn = game["turn"]
        expected_player = 0 if current_turn == X else 1
        
        if player_index != expected_player:
            await ctx.send(f"It's not your turn! Waiting for **{current_turn}** to move.")
            return
        
        mark = X if player_index == 0 else O
        updateBoard(board, position, mark)
        
        board_text = f"```{getBoardStr(board)}```"
        
        if isWinner(board, mark):
            await ctx.send(board_text)
            await ctx.send(f"{ctx.author.mention} (**{mark}**) has won the game! 🎉")
            del self.active_games[channel_id]
            return
        
        if isBoardFull(board):
            await ctx.send(board_text)
            await ctx.send("It's a tie! 🤝")
            del self.active_games[channel_id]
            return
        
        game["turn"] = O if game["turn"] == X else X
        next_mark = game["turn"]
        
        next_player_id = game["players"][0] if next_mark == X else game["players"][1]
        if next_player_id:
            next_mention = f"<@{next_player_id}>"
            await ctx.send(f"{board_text}\nNext: {next_mention} (**{next_mark}**)")
        else:
            await ctx.send(f"{board_text}\nNext: **{next_mark}** - waiting for another player to join!")

    @commands.command(name="endgame")
    async def end_game(self, ctx):
        """Force end the active game in this channel (starter or admin only)"""
        channel_id = ctx.channel.id
        game = self.active_games.get(channel_id)
        
        if not game:
            await ctx.send("No active game to end")
            return
        
        starter_id = game["players"][0]
        if ctx.author.id != starter_id and not ctx.author.guild_permissions.manage_guild:
            await ctx.send("Only the person who created the game or a mod can end it!")
            return
        
        del self.active_games[channel_id]
        await ctx.send("Game ended!")


async def setup(bot):
    await bot.add_cog(TicTacToe(bot))