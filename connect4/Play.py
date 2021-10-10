# d7141
#
# Play against a human

import logging
log = logging.getLogger(__name__)  # Inherits main config

import numpy as np
from Board import Game
from Creature import Creature


class Human(Creature):
    """Human player. Override the place methods"""
    def __init__(self):
        super().__init__()

    def next_move(self, board, me):
        # Overriding method
        while True:
            move = input("Column to place in: ")

            try:
                move = int(move)-1
            except Exception as e:
                log.error("Invalid input")
                continue

            if 0 <= int(move)-1 <= 6:
                # Valid move
                return int(move)-1
            else:
                log.error("Invalid range.")


if __name__ == '__main__':
    print("Beginning game.")
    print("You are Player 1")
    if np.random.rand() < 0.5:
        print("You begin!")
        start = True
        game = Game(Human(), Creature(), fancy_display=True)
    else:
        print("The computer begins")
        start = False
        game = Game(Creature(), Human(), fancy_display=True)

    winner = game.run()
    print(f"Player {winner} wins!")
    if (winner == 1 and start) or (winner == 2 and not start):
        print("(That's you)")
    else:
        print("(That's not you)")
