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
        self.table = self.draw_card(msg='Whats the starting card on the table\n[-] : ')  # Whats the card on the table
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
        hand.append(self.draw_card(msg='[0] : '))
        hand.append(self.draw_card(msg='[1] : '))
        logger.warning('Assuming the other two cards are hidden.')
        hand += [14, 14]  # Two hidden cards
        self.actual_hand = hand.copy()  # Otherwise changes (sorting) are synced
        self.hand = hand

    def gen_state(self, draw=None):
        self.hand.sort()  # to combine states in the end
        if draw is None:
            # Then do normal
            self.card = self.draw_card()  # this is the potential card (get rid of list)
            return [self.card] + self.hand
        else:
            self.card = draw
            return [draw] + self.hand

    def choice(self, s):
        # Make a choice of action depending on the state
        logger.debug('Hand of %a' % self.hand)
        logger.debug('Real hand of %a' % self.actual_hand)
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
        extra = False
        if action < 4:
            if self.hand[action] == 0:
                # They are trying to discard a zero
                logger.info('CHOICE: Not choosing the card')
                logger.debug('Discarding the card (Tried to discard a zero)')
                discard = self.card
                extra = True  # So we will draw another card
            elif self.card == 12:
                # There is a queen visible that they are trying to "take"
                discard = self.card
                if self.hand[action] == 14:
                    # They are trying to look at a hidden hand, so see what it is
                    logger.info('CHOICE: Tapping the Queen (on card index %a, as hidden enter it too)' % self.actual_hand.index(self.hand[action]))
                    logger.debug('Override - Looking at hidden card %a' % action)
                    n = self.draw_card()
                    self.actual_hand[self.actual_hand.index(self.hand[action])] = n
                    self.hand[action] = n
                else:
                    logger.debug('Looking at card %a which i already know' % action)
                    extra = True
            elif self.hand[action] == 14:
                # They are discarding a hidden card, so discard the actual card
                logger.info('CHOICE: Swap with index %a (as hidden card, enter it too)' % self.actual_hand.index(self.hand[action]))
                logger.debug('CHOICE: Swapping %a with %a.' % (self.card, discard))
                logger.debug('CHOICE: This is card index %a.' % action)
                discard = self.draw_card()  # Discard a random card
                self.actual_hand[self.actual_hand.index(self.hand[action])] = self.card
                self.hand[action] = self.card
            else:
                discard = self.hand[action]
                self.actual_hand[self.actual_hand.index(self.hand[action])] = self.card
                self.hand[action] = self.card
                logger.debug('CHOICE: Swapping %a with %a.' % (self.card, discard))
                logger.debug('CHOICE: This is card index %a.' % self.hand.index(self.card))
                logger.info('CHOICE: Swap with index %a.' % self.actual_hand.index(self.card))
            self.table = discard
            done = False
            assert discard != 0
            ##logger.info('CHOICE: Swapping %a with %a.' % (self.card, discard))
            #logger.info('CHOICE: This is card index %a.' % self.hand.index(self.card))
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
        return discard, done, extra

    def remove_card(self, discard):
        for card in self.hand:
            if discard == card:  # Cant discard the 14!
                assert discard != 14
                logger.debug('Discarding %a' % (discard))
                logger.info('ACTION: Discarding %a; index of %a' % (discard, self.actual_hand.index(discard)))
                self.hand[self.hand.index(discard)] = 0
                self.actual_hand.remove(discard)
                #self.actual_hand[self.actual_hand.index(card)] = 0

    def run_round(self):
        self.gen_hand()
        self.remove_card(self.table)
        done = False
        while not done:
            msg = input('\nIs my turn? (y/n) : ')
            if msg is 'y' or msg == 'Y':
                # Then compute the round
                s = self.gen_state(draw=self.table)
                logger.debug('State of %a' % s)
                a = self.choice(s)
                discard, done, extra = self.step(a)
                self.remove_card(discard)
                if a == 4 or extra:
                    # They dont want the card
                    logger.info('CHOICE: Draw a new card')
                    s = self.gen_state()
                    logger.debug('State of %a' % s)
                    a = self.choice(s)
                    discard, done, more = self.step(a)
                    self.remove_card(discard)
                    if more:
                        # They still dont want it (illegal queen tap or discard 0)
                        logger.info('CHOICE: Not choosing the card')
            elif msg is 'n' or msg == 'N':
                # Then maybe we can chuck out a card
                logger.info('ACTION: Enter discarded card')
                card = self.draw_card(msg='[:] : ')
                self.table = card
                for c in self.hand:
                    if c == card:
                        # Then lets discard
                        logger.debug('CHOICE: Discarding %a with index of %a' % (card, self.hand.index(card)))
                        logger.info('CHOICE: Discarding %a with real index of %a' % (card, self.actual_hand.index(card)))
                        self.hand[self.hand.index(card)] = 0
                        self.actual_hand.remove(card)
                        #self.actual_hand[self.actual_hand.index(card)] = 0
            else:
                raise ValueError('Ahhhhh nope.')

            if len(self.actual_hand) == 0:
                # Yay! we won!
                done = True
                logger.info('WE WON!!!!')


if __name__ == '__main__':
    logger = logging.getLogger('dutch')
    logger.setLevel(logging.INFO)  # Set level here
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










