# d6644
# Class file to run the all Dutch necessary actions

import numpy as np
import os
import logging

logger = logging.getLogger('jerry.dutch')

class Dutch:
    def __init__(self, eyes):
        logger.info('Loading dutch...')
        self.base = os.path.dirname(os.path.abspath(__file__))
        self.Q = np.load(os.path.join(self.base, 'q-table.npy'))  # Adjust for use
        self.eyes = eyes
        self.hand = None
        self.actual_hand = None

        logger.debug('Using qtable at %a' % os.path.join(self.base, 'q-table.npy'))

    def refine_card(self, card):
        # All cards are accepted
        return card

    def draw_card(self, msg='[-] : '):
        # Use the eyes alg to "see" the card
        input(msg)
        return self.refine_card(int(self.eyes.read()[1]))  # only want the value not the suit

    def gen_hand(self):
        hand = []
        logger.info('Load each card one at a time')
        hand.append(self.draw_card(msg='[1] : '))
        hand.append(self.draw_card(msg='[2] : '))
        hand.append(self.draw_card(msg='[3] : '))
        hand.append(self.draw_card(msg='[4] : '))
        self.actual_hand = hand.copy()  # Otherwise changes (sorting) are synced
        self.hand = hand

    def gen_state(self):
        self.card = self.draw_card()  # this is the potential card (get rid of list)
        self.hand.sort()  # to combine states in the end
        return [self.card] + self.hand

    def choice(self, s):
        # Make a choice of action depending on the state
        logger.debug('Q table %a' % self.Q[s[0], s[1], s[2], s[3], s[4], :])
        m = np.max(self.Q[s[0], s[1], s[2], s[3], s[4]])
        i = np.where(self.Q[s[0], s[1], s[2], s[3], s[4]] == m)[0]
        #a = np.argmax(self.Q[s[0], s[1], s[2], s[3], s[4]])
        a = np.random.choice(i)
        logger.debug('Q ACTION OF %a' % a)
        return a

    def step(self, action):
        assert 0 <= action <= 6
        discard = None
        if action < 4:
            # Then swap with card 1 etc
            discard = self.hand[action]
            self.hand[action] = self.card
            inx = self.actual_hand.index(discard)
            self.actual_hand[inx] = self.card
            done = False
            logger.info('CHOICE: Swapping %a with %a.' % (self.card, discard))
            logger.info('CHOICE: This is card index %a.' % inx)
        elif action == 4:
            # Then don't choose the card
            logger.info('CHOICE: Not choosing the card')
            discard = self.card
            done = False
        elif action == 5:
            # Then call dutch
            logger.info('CHOICE: Calling dutch')
            done = True
        else:
            raise IndexError('welp')
        return discard, done

    def run_round(self):
        self.gen_hand()
        done = False
        while not done:
            msg = input('Is my turn? (y/n) : ')
            if msg is 'y' or msg == 'Y':
                # Then compute the round
                s = self.gen_state()
                a = self.choice(s)
                discard, done = self.step(a)
            elif msg is 'n' or msg == 'N':
                # Then maybe we can chuck out a card
                logger.info('Looking for discarded')
                card = self.draw_card(msg='[:] : ')
                if card in self.hand:
                    # Then lets discard
                    logger.info('CHOICE: Discarding %a with index of %a' % (card, self.actual_hand.index(card)))
                    self.hand[self.hand.index(card)] = 0
                    self.actual_hand[self.actual_hand.index(card)] = 0
                else:
                    logger.info('No matching card.')
            else:
                raise ValueError('Ahhhhh nope.')


if __name__ == '__main__':
    logger = logging.getLogger('dutch')
    logger.setLevel(logging.DEBUG)  # Set level here
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    class Eyes:
        def read(self):
            l = input('{Enter card Number}\n')
            return None, int(l)

    logger.info('Running local sim')
    dutch = Dutch(Eyes())
    logger.warning('Just ignore lines like [.]. Only enter cards when told')
    dutch.run_round()










