# d6636
# The Dutch environment, has all the functions and plays the game
# Heavily based on heart environment from 52523078f10a60e84297856e424faf6817d91e20

# This is the same irrespective of how the agent is built

# observation = (viewed card, card 1, card 2, card 3, card 4)  <- all one hot coded
# action = 0-3 = choose, 4 = nope, 5 = call 'Dutch!')

import numpy as np
import logging
import random

logger = logging.getLogger('dutch.Player')


class Player():
    def __init__(self, learn=False, lowest=False):
        logger.info('Dutch engine initilised')
        self.hand = self.draw_hand()  # 2 cards, plus two hidden cards
        self.card = None
        self.Q = np.zeros((14,15,15,15,15,6))  # pickup, c1, c2, c3, c4, a  (14=hidden card)
        self.teach = learn  # If it should update the Q table or not
        self.lowest = lowest
        self.legacy_reward = 0  # How many reward points (losing points) that action ended up being
        self.old_state = None  # Then compute from old state
        self.old_action = None
        # Special: 0=none, 14=hidden, 1-13=cards

    def draw_hand(self):
        return self.draw_card(2) + [14, 14]

    def draw_card(self, num_cards=1):
        cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        r = []
        for i in range(num_cards):
            r.append(random.choice(cards))
        return r

    def print_cards(self):
        logger.debug('--- Current cards ---')
        logger.debug(self.hand)

    def gen_state(self, draw=None):
        self.hand.sort()
        if draw is None:
            self.card = self.draw_card()[0]
            return [self.card] + self.hand  # this is the potential card (get rid of list)
        else:
            self.card = draw
            return [draw] + self.hand

    def step(self, action):
        assert 0 <= action <= 6
        discard = None
        if action < 4:
            logger.debug('Swapping with card %a' % action)
            # Then swap with card 1 etc
            if self.hand[action] == 0:
                # They are trying to discard a zero
                discard = self.card
            elif self.card == 12:
                # There is a queen visible that they are trying to "take"
                discard = self.card
                if self.hand[action] == 14:
                    # They are trying to look at a hidden hand, so see what it is
                    self.hand[action] = self.draw_card()[0]
                    logger.debug('Override - Looking at hidden card %a' % action)
            elif self.hand[action] == 14:
                # They are discarding a hidden card, so discard the actual card
                discard = self.draw_card()  # Discard a random card
                self.hand[action] = self.card
            else:
                discard = self.hand[action]
                self.hand[action] = self.card
            done = False
            assert discard != 0 or 14

        elif action == 4:
            # Then don't choose the card
            logger.debug('Not choosing the card')
            discard = self.card
            done = False
        elif action == 5:
            # Then call dutch
            logger.debug('Calling dutch')
            done = True
        else:
            raise IndexError('welp')

        return self.gen_state(), discard, done

    def score(self):
        # Make more complex
        hidden = self.hand.count(14)  # Number of hidden cards
        sc = 0
        for i in range(hidden):
            sc += self.draw_card()[0]
        return (sc + np.sum(self.hand) - 14*hidden)*-1  # Minus off the hidden pts

    def choice(self, s, eps=0.5):
        # Make a choice of action depending on the state
        logger.debug('Hand of %a' % self.hand)
        if self.lowest:
            # Nonlearning system of always choosing the lowest one
            # Never calls dutch
            if self.card < max(self.hand):
                # There is a higher card
                return self.hand.index(max(self.hand))  # Return the value of that max card
            else:
                return 4  # Codes for not picking it up
        else:
            # Either use the q table or random
            logger.debug('Q table %a' % self.Q[s[0], s[1], s[2], s[3], s[4], :])
            if np.random.random() < eps or np.sum(self.Q[s[0], s[1], s[2], s[3], s[4], :]) == 0.:
                logger.debug('RANDOM ACTION')
                a = np.random.randint(0, 6)  # random choice
            else:
                m = np.max(self.Q[s[0], s[1], s[2], s[3], s[4]])
                i = np.where(self.Q[s[0], s[1], s[2], s[3], s[4]] == m)[0]
                #a = np.argmax(self.Q[s[0], s[1], s[2], s[3], s[4]])
                a = np.random.choice(i)
                logger.debug('Q ACTION OF %a' % a)
        return a

    def learn(self, s, a, new_s, r, lr=0.01, gma=0.9):
        if self.teach:
            logger.debug('Learning....')
            # Update the q table
            self.Q[s[0], s[1], s[2], s[3], s[4], a] = \
                self.Q[s[0], s[1], s[2], s[3], s[4], a] + \
                lr*(r + gma*np.max(self.Q[new_s[0], new_s[1], new_s[2], new_s[3], new_s[4], :]) -
                    self.Q[s[0], s[1], s[2], s[3], s[4], a])

    def reset(self):
        # Resetting environment
        logger.debug('Resetting Player.')
        self.hand = self.draw_hand()
        self.discard = None
        self.legacy_reward = 0
        self.old_state = None
        self.old_action = None

