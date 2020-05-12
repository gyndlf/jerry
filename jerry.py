# d6623
# This is the main controlling python file. Everything should be used only in class form

print('Jerry v1.1')
print('"I would never lose to a machine" - Felonius Gru')

import logging
logger = logging.getLogger('jerry')
logger.setLevel(logging.INFO)  # Set level here
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

from blackjack.blackjack import Blackjack
from cards.eyes import Eyes

blackjack = Blackjack()
eyes = Eyes()

while True:
    # Get the inputed cards
    logger.info('Begin Blackjack')
    cards = blackjack.gen_hand(eyes)
    blackjack.run_round(eyes, cards)
    logger.info('end')
