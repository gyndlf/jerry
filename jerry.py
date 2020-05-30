# d6623
# This is the main controlling python file. Everything should be used only in class form

print('Jerry v1.2')
print('"I would never lose to a machine" - Felonius Gru')

import logging
logger = logging.getLogger('jerry')
logger.setLevel(logging.DEBUG)  # Set level here
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

from blackjack.blackjack import Blackjack
from dutch.dutch import Dutch
from cards.eyes import Eyes

eyes = Eyes()
blackjack = Blackjack()
dutch = Dutch(eyes=eyes)

while True:
    # Get the inputed cards
    logger.info('Begin Dutch')
    dutch.run_round()
    logger.info('end')
