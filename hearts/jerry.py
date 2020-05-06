# %%
# d6617
# The code to run the system. Cause jupyter is just..... better

from environment import Simulator
from lowest_alg import Lowest
import numpy as np

import logging

logger = logging.getLogger('jerry')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
#ch.setLevel(logging.INFO)  # Set the level here
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.debug('Hi')
# Save logs to file
# fh = logging.FileHandler('jerry.log')
# fh.setLevel(logging.DEBUG)


lowest = Lowest()

players = 4
observations = 'limited'  # limited or expanded mode of observations
scoring = 'single'  # face or single modes
algs = [lowest, lowest, lowest, lowest]

sim = Simulator(players=players, observations=observations, scoring=scoring)
sim.load_algorithms(algs)

# %%
starting_player = 0  # make this ace of clubs eventually
done = False
i = 1

while i < 14:  # 14 is a full game of 4 players
    logger.info('#--- ROUND ' + str(i) + '---#')
    # sim.print_cards()
    # For each round:
    # For each player in round
    # Choose an action depending on the state
    # Do the action
    # Compute the reward
    # (Q table modification if applicable)
    # Change new state, to current state
    # Compute points
    logger.info('$--- Player Turn ' + str(starting_player) + '---$')
    a = sim.init_state(starting_player)
    sim.step(starting_player, a)
    move = 1

    while move < players:
        # So only a certain number of moves

        turn = starting_player + move
        if turn > 3:
            turn -= 4  # Loop back around
        logger.info('$--- Player Turn ' + str(turn) + ' ---$')

        s = sim.gen_state(turn)
        logger.info('State of\n' + str(s))

        a = sim.choose(turn, s)  # Make a decision
        sim.step(turn, a)  # play that decision

        move += 1
    starting_player = sim.find_winner(starting_player)
    i += 1
sim.print_cards()
logger.info('Final scores of ' + str(sim.scores))
logger.info('Cards left ' + str(np.sum(sim.current_hands)))

