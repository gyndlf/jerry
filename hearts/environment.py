# d6617
# The hearts environment, has all the functions and plays the game

# need to be able to call
# env.reset()
# env.step()

# This is the same irrespective of how the agent is built

# observation = (card's played, highest card played, my cards)

import numpy as np
import logging

logger = logging.getLogger('jerry.environment')

def deal_hands(players=4):
    # Deal the cards
    cards = np.arange(1, 53)  # All cards dealt
    np.random.shuffle(cards)
    length = int(52//players)
    logger.warning('Undealt cards of ' + str(52-length*players))
    hands = np.zeros((players, 4, 14))

    for player in range(players):
        hand = cards[player*length:player*length+length]  # get "your" cards
        for card in hand:
            if card < 14:
                # Heart
                hands[player, 0, card] = 1
            elif card < 27:
                # Clubs
                hands[player, 1, card-13] = 1
            elif card < 40:
                # Spades
                hands[player, 2, card-13-13] = 1
            else:
                # Diamond
                hands[player, 3, card-13-13-13] = 1
        logger.info('Player ' + str(player) + "'s hand\n" + str(hands[player]))
    logger.debug('Sum of player hands =' + str(np.sum(hands)))
    return hands


class Simulator():
    def __init__(self, players, observations='limited'):
        logger.info('Hearts engine initlised')

        # CONSTANTS
        self.hands = deal_hands(players)  # all cards
        self.players = players
        logger.warning('Only limited mode is implemented')
        assert observations == 'limited' or 'expanded' or 'full' or 'super'
        self.mode = observations  # Higher observations convey more infomation, but need a more complex machine
        # limited = (index, suit, card) index=0 played cards (only highest card shown), index=1 cards available
        # expanded = (index, suit, card) index=0 all played cards (card 0 is required suit), index=1 cards available
        # full = (index, suit, card) index=0 all played cards, index=1 cards available, index=2 all cards played (game)
        # super = (index, suit, card) same as full, but index=2,3,4 is cards other plays have played

        #Variables
        self.current_hands = self.hands  # only cards left
        self.played = []  # Cards played this round
        self.suit = 0  # What suit?

        # List of what cards the model holds
        self.hearts = 0
        self.clubs = 1
        self.spades = 2
        self.diamonds = 3

    def load_algorithms(self, algorithms):
        assert algorithms.__len__() == self.players  # Make sure right number is entered
        self.algs = algorithms  # These will be the models

    def print_cards(self):
        logger.info('--- Current cards ---')
        for player in range(self.players):
            logger.info('Player' + str(player) + "'s hand\n" + str(self.current_hands[player]))

    def init_state(self, player):
        # Can choose any card... but choosing a suit is harder.
        suit, card = self.algs[player].choose_first_card(self.current_hands[player])
        self.played = []
        self.suit = suit
        return suit, card

    def gen_state(self, turn):
        # Played is cards played, turn is player's turn
        # create observation
        num_cards = len(self.played)
        highest_card = 0
        for play in self.played:  # Get the highest card of the right suit
            if play[0] == self.suit and play[1] > highest_card:
                highest_card = play[1]
        if self.mode is 'limited':
            # limited = (index, suit, card) index=0 played cards (only highest card shown), index=1 cards available
            o = np.zeros((2, 4, 14))
            logger.debug('Obseration shape' + str(o.shape))
            o[0,self.suit,highest_card] = 1  # only one hot largest card
            o[1, :, :] = self.current_hands[turn]  # add the player's hand
            return o
        else:
            logger.error('Invalid mode')
            raise('Mode not implemeted')

    def choose(self, turn, state):
        # Choose what card to play from the state
        return self.algs[turn].think(self.mode, state)

    def step(self, turn, action):
        # Step in direction of action.
        # action = (suit, card)
        self.current_hands[turn, action[0], action[1]] = 0  # Use the card
        self.played.append(action)
        logger.info('$--- CARDS Played' + str(self.played))

    def find_winner(self):
        pass

