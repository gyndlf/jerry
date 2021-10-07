# d7137

# The board
import logging
import numpy as np
from scipy.signal import convolve2d
from Creature import Creature

log = logging.getLogger(__name__)  # Inherits main config


class Game:
    """The Connect 4 Game: Runs the game over the board"""
    def __init__(self, p1, p2):
        self.board = Board()
        self.players = [p1, p2]  # Load player/creatures 1 and 2

        self.preview = True  # Show the board each round

    def run(self):
        """Runs the connect 4 game"""
        turn = 0  # Which player's turn is it
        rnd = 0
        while not self.board.end():
            log.debug(f"Round {rnd // 2} : {['1', '2'][turn]}")
            log.debug(self.board.state)

            col = self.players[turn].next_move(self.board)  # Get the column to place in
            self.board.place(turn+1, col)  # Place the piece

            turn = (turn + 1) % 2  # Alternate 0,1,0,...
            rnd += 1
        winner = self.board.who_won()
        log.debug(f"Winner: {winner}")
        return winner


class Board:
    """ The Connect 4 Board (per game).
        Intentionally low level, just some smart functions on the numpy array"""
    def __init__(self):
        self.state = None  # Stub
        self.clear()

    def clear(self):
        """Clear the board"""
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
            # Invalid column to place the piece in. Computer will chose a random column
            perm = np.random.permutation(7)
            log.debug(f"Invalid column {column}: Trying a random selection")
            for column in perm:  # Try them all
                log.debug(f"Choose {column}")
                col = self.state[:, column]
                top = np.nonzero(col)[0]
                if top.size != 6:
                    # Place it.
                    if top.size == 0:
                        loc = 5
                    else:
                        loc = top[0]-1
                    break
        else:
            loc = top[0]-1
        self.state[loc, column] = id  # Actually place it now

    def end(self):
        """Has the game ended?"""
        return self.has_won() or self.stalemate()

    def has_won(self):
        """Return true if someone won"""
        return self.who_won() is not None

    def stalemate(self):
        """Return true if board is filled completely"""
        return not np.any(self.state == 0)

    def who_won(self):
        """Return who won (player id)"""
        # Nicely based off https://stackoverflow.com/questions/29949169/python-connect-4-check-win-function

        horizontal_kernel = np.array([[1, 1, 1, 1]])
        vertical_kernel = np.transpose(horizontal_kernel)
        diag1_kernel = np.eye(4, dtype=np.uint8)
        diag2_kernel = np.fliplr(diag1_kernel)
        detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]

        for kernel in detection_kernels:
            if (convolve2d(self.state == 1, kernel, mode="valid") == 4).any():
                return 1
            elif (convolve2d(self.state == 2, kernel, mode="valid") == 4).any():  # Assuming only 1 win condition is met
                return 2
        return None  # No one won :(
