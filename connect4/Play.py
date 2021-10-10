# d7141
#
# Play against a human

import logging
log = logging.getLogger(__name__)  # Inherits main config

import numpy as np
from Board import Game
from Creature import Creature
import Database


class Human(Creature):
    """Human player. Override the place methods"""
    def __init__(self):
        super().__init__()

    def next_move(self, board, me):
        # Overriding method
        while True:
            move = input("Column to place in: ")

            try:
                move = int(move)
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

    uid = input("Enter uid for creature in db")
    assert type(uid) == str
    creature = Database.retrieve_creature(uid)

    if np.random.rand() < 0.5:
        print("You begin!")
        print("You are Player 1")
        start = True
        game = Game(Human(), creature, fancy_display=True)
    else:
        print("The computer begins")
        print("You are Player 2")
        start = False
        game = Game(creature, Human(), fancy_display=True)

    winner = game.run()
    print(f"Player {winner} wins!")
    if (winner == 1 and start) or (winner == 2 and not start):
        print("(That's you)")
    else:
        print("(That's not you)")
