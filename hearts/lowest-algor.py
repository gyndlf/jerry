# d6617
# Algorithm that simply chooses the lowest card it can play

import numpy as np

class Lowest():
    def __init__(self):
        self.info = 'Algorithm that takes a hand and chooses the lowest card'

    def think(self, observation):
        # Takes inputs, returns action
        # observation = (num cards played, highest card played, my cards)
        cards = observation[2]
        choice = np.argmax(cards)  # array of 1's and 0's
        print('*---LOWEST---*')
        print('Of cards', cards, 'choosing lowest card of', choice)
        return choice

