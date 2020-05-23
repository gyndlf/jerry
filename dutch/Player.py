# d6636
# The Dutch environment, has all the functions and plays the game
# Heavily based on heart environment from 52523078f10a60e84297856e424faf6817d91e20

# This is the same irrespective of how the agent is built

# observation = (viewed card, card 1, card 2, card 3, card 4)  <- all one hot coded
# action = 0-3 = choose, 4 = nope, 5 = call 'Dutch!')

import numpy as np
import logging
import random

logger = logging.getLogger('dutch.environment')


class Player():
    def __init__(self):
        logger.info('Dutch engine initilised')
        self.hand = self.draw_card(4)  # all cards
        self.card = None
        self.Q = np.zeros((14,14,14,14,14,6))  # pickup, c1, c2, c3, c4, a

    def draw_card(self, num_cards=1):
        cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        r = []
        for i in range(num_cards):
            r.append(random.choice(cards))
        return r

    def print_cards(self):
        logger.debug('--- Current cards ---')
        logger.debug(self.hand)

    def gen_state(self):
        self.card = self.draw_card()  # this is the potential card
        # TODO:
        #  Sort hand so that the lowest card is always first
        return self.card + self.hand

    def step(self, action):
        assert 0 <= action <= 6
        if action < 4:
            # Then swap with card 1 etc
            self.hand[action] = self.card
            done = False

        elif action == 4:
            # Then don't choose the card
            done = False

        elif action == 5:
            # Then call dutch
            done = True

        else:
            raise IndexError('welp')

        reward = 0

        return self.gen_state(), reward, done

    def reset(self):
        # Resetting environment
        logger.debug('Resetting Player.')

        self.hand = self.draw_card(4)

