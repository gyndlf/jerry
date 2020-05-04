# d6617
# Algorithm that simply chooses the lowest card it can play

import numpy as np

class Lowest():
    def __init__(self):
        self.info = 'Algorithm that takes a hand and chooses the lowest card'

    def think(self, observation):
        # Takes inputs, returns action
        # observation = (num cards played, highest card played, my cards)
        cards = observation[2]  # only 1 suit
        choice = np.argmax(cards)  # array of 1's and 0's
        print('*---LOWEST---*')
        print('Of cards', cards, 'choosing lowest card of', choice)
        return choice

    def choose_first_card(self, cards):
        # What card should you play first?
        print('Cards:', cards)
        card = 0
        for i in range(14):
            print(i)
            if np.argmax(cards[:, i]) > 0:
                # There is a card
                card = (13*np.argmax(cards[:, i])) + i
                print('Choose', np.argmax(cards[:, i]), i)
                print('which is', card)
                break
        if card == 0:
            raise('Ummmmm')
        return card

