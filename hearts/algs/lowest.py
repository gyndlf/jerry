# d6617
# Algorithm that simply chooses the lowest card it can play

import numpy as np
import logging

logger = logging.getLogger('jerry.algs.lowest')

class Lowest():
    def __init__(self):
        self.info = 'Algorithm that takes a hand and chooses the lowest card'

    def think(self, mode, observation):
        # Takes inputs, returns action
        assert mode == 'limited'

        suit, card = np.where(observation[0,:,:]==1)
        suit = int(suit)
        card = int(card)

        sel = np.argmax(observation[1, suit])  # array of 1's and 0's
        if sel == 0:
            choice = self.choose_sub_card(observation[1])
            # There is none of that suit
            # Then choose worst card
        else:
            choice = (suit, sel)
        logger.debug('Choosing lowest card of' + str(choice))
        return choice

    def choose_first_card(self, cards):
        # What card should you play first?
        logger.debug('Cards:\n' + str(cards))
        card = 0
        for i in range(14):
            if np.sum(cards[:, i]) > 0:
                # There is a card
                logger.debug('(Best card) Choose' + str((np.argmax(cards[:, i]), i)))
                return np.argmax(cards[:, i]), i
        logger.error('Indexing error')
        raise IndexError('Ummmmm')

    def choose_sub_card(self, cards):
        # What card do you throw away? (Worst card?)
        card = 0
        for i in range(13,-1,-1):  # just go backwards
            # print(i, '==>', np.argmax(cards[:, i]))
            if np.sum(cards[:, i]) > 0:
                # There is a card
                logger.debug('(Worst card) Choose' + str((np.argmax(cards[:, i]), i)))
                return np.argmax(cards[:, i]), i
        logger.error('Indexing error')
        raise IndexError('Uhhhhh')
