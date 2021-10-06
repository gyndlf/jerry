# d7050

import numpy as np
from Player import Player
import logging

logger = logging.getLogger('lastcard')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

players = [Player("1"), Player("2"), Player("r1", random=True), Player("r2", random=True)]  # Make more complex

logger.info("Running round")
for p in players:
    p.reset()

turn = np.random.randint(len(players))


