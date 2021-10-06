# d7137

# The board
import numpy as np


class Board:
    """The Connect 4 Board"""
    def __init__(self, p1, p2):
        self.state = np.zeros((6,7), dtype='int')
        self.players = [p1, p2]  # Load player 1 and 2

    def run(self):
        """Runs the connect 4 game"""
        turn = 0  # Which player's turn is it
        while not self.has_won():
            move = self.players[turn].next_move(self.state)
            self.place(turn, move)

    def place(self, player, column):
        """Where [[player]] is the player id, and [[column]] is the column they placed in"""
        ...

    def has_won(self):
        """Return true if someone won"""
        ...

    def who_won(self):
        """Return who won (player id)"""
        ...
