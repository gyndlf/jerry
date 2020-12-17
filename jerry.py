# d6623
# This is the main controlling python file. Everything should be used only in class form

print('Jerry v1.2.2')
print('"I would never lose to a machine" - Felonius Gru')

import logging
logger = logging.getLogger('jerry')
logger.setLevel(logging.DEBUG)  # Set level here
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

from cards.Eyes import Eyes
from Blackjack.Blackjack import Blackjack
#from dutch.dutch import Dutch

eyes = Eyes()
blackjack = Blackjack(eyes=eyes)
#dutch = Dutch(eyes=eyes)

while True:
    logger.info("Begin jerry")
    logger.info('BlackJack')
    cards = blackjack.gen_hand()
    blackjack.run_round(cards)
    logger.info("End of round")
