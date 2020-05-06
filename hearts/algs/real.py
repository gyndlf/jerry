# d6619
# A real player agent. Thus the sim doesn't actually know what cards it has
# d6617
# Algorithm that simply chooses the lowest card it can play

import numpy as np
import logging

logger = logging.getLogger('jerry.algs.real')

class Real():
    def __init__(self):
        self.info = 'A real player. Cards must be manually entered'
        self.help = 'Hearts = 0, clubs = 1, spades = 2, diamonds = 3'

    def enter_card(self):
        done = False
        while not done:
            entered = input('Enter card (suit, card) {h for help}: ')
            if entered == 'h':
                print(self.help)
            else:
                try:
                    choice = eval(entered)
                    done = True
                except:
                    logger.error('Invalid card enter')
        return choice

    def think(self, mode, observation):
        # Takes inputs, returns action
        assert mode == 'limited'

        choice = self.enter_card()

        # Check if valid

        return choice

    def choose_first_card(self, cards):
        # What card should you play first?
        logger.debug('Cards:\n' + str(cards))
        return self.enter_card()

    def choose_sub_card(self, cards):
        # What card do you throw away? (Worst card?)
        return self.enter_card()
