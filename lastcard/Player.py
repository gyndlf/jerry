# d7050

import logging
import numpy as np

START_HAND_SIZE = 7
# All cards are simply their normal equivalent. The ones below are the special cards
PICK_UP_2 = 2
PICK_UP_5 = 5
CHANGE_SUIT = 1
SKIP = 10


logger = logging.getLogger('lastcard.Player')

class Player:
    def __init__(self, name: str, random=False):
        self.q = np.zeros((20, 20, 20, 20, 20, 3))  # same num, same colour, col1, col2, col3, action
        self.hand = []
        self.name = name

    def draw_card(self):
        # Returns 1-13
        return np.random.randint(1, 14)  # (14 is never returned)

    def init_hand(self):
        self.hand = [self.draw_card() for i in range(START_HAND_SIZE)]

    def print_hand(self):
        print(self.name + "'s hand: ", self.hand)

    def step(self, action):
        # Play out the action according to the state
        pass

    def score(self):
        # Give a score of how good the hand is
        pass

    def choice(self, state):
        # Return an action depending on the current state
        pass

    def gen_state(self, card):
        pass

    def reset(self):
        pass

