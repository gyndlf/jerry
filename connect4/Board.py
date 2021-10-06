# d7137

# The board
import numpy as np
from Creature import Creature


class Game:
    """The Connect 4 Game: Runs the game over the board"""
    def __init__(self, p1, p2):
        self.board = Board()
        self.players = [p1, p2]  # Load player/creatures 1 and 2

        self.preview = False  # Show the board each round

    def run(self):
        """Runs the connect 4 game"""
        turn = 0  # Which player's turn is it
        rnd = 1
        while not self.board.end():
            col = self.players[turn].next_move(self.board)  # Get the column to place in
            self.board.place(turn+1, col)  # Place the piece

            if self.preview:  # and rnd % 2 == 0:
                print("Round", rnd // 2)
                print(self.board.state)

            turn = (turn + 1) % 2  # Alternate 0,1,0,...
            rnd += 1


class Board:
    """ The Connect 4 Board (per game).
        Intentionally low level, just some smart functions on the numpy array"""
    def __init__(self):
        self.state = np.zeros((6, 7), dtype='int')

    def place(self, id, column):
        """Where [[player]] is the player id, and [[column]] is the column they placed in"""
        assert 0 <= column <= 6  # WARNING: COLUMNS ARE 0 INDEXED
        col = self.state[:, column]
        top = np.nonzero(col)[0]

        if top.size == 0:
            # Its empty
            loc = 5
        elif top.size == 6:
            raise Exception('Invalid column, pick again')
        else:
            loc = top[0]-1
        self.state[loc, column] = id

    def end(self):
        """Has the game ended?"""
        return self.has_won() or self.stalemate()

    def has_won(self):
        """Return true if someone won"""


    def stalemate(self):
        """Return true if board is filled completely"""
        return not np.any(self.state == 0)

    def who_won(self):
        """Return who won (player id)"""
        ...
