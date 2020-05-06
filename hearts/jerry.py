# %%
# d6617
# The code to run the system. Cause jupyter is just..... better

from environment import Simulator
from algs import lowest, highlow, slowlow
import numpy as np

import logging

logger = logging.getLogger('jerry')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
#ch.setLevel(logging.INFO)  # Set the level here
ch.setFormatter(formatter)
logger.addHandler(ch)

# Save logs to file
# fh = logging.FileHandler('jerry.log')
# fh.setLevel(logging.DEBUG)



players = 4
observations = 'limited'  # limited or expanded mode of observations
scoring = 'single'  # face or single modes

algs = [slowlow.SlowLow(players=players),
        lowest.Lowest(),
        lowest.Lowest(),
        highlow.HighLow()]

sim = Simulator(players=players, observations=observations, scoring=scoring)
sim.load_algorithms(algs)

# %%
num_games = 5000
total_scores = np.zeros((players))
logger.info('Running %a games with algs of %a' % (num_games, algs))
for game in range(num_games):
    sim.reset()
    starting_player = 0  # make this ace of clubs eventually
    done = False
    i = 1

    while i < int(52//players)+1:  # 14 is a full game of 4 players
        logger.debug('#--- ROUND ' + str(i) + '---#')
        # sim.print_cards()
        # For each round:
        # For each player in round
        # Choose an action depending on the state
        # Do the action
        # Compute the reward
        # (Q table modification if applicable)
        # Change new state, to current state
        # Compute points
        logger.debug('$--- Player Turn ' + str(starting_player) + ' -> ' + str(algs[starting_player]) + '---$')
        a = sim.init_state(starting_player)
        sim.step(starting_player, a)
        move = 1

        while move < players:
            # So only a certain number of moves
            turn = starting_player + move
            if turn > players-1:
                turn -= players  # Loop back around
            logger.debug('$--- Player Turn ' + str(turn) + ' -> ' + str(algs[turn]) + ' ---$')

            s = sim.gen_state(turn)
            logger.debug('State of\n' + str(s))

            a = sim.choose(turn, s)  # Make a decision
            sim.step(turn, a)  # play that decision

            move += 1
        starting_player = sim.find_winner(starting_player)
        i += 1
    sim.print_cards()
    logger.debug('Final scores of ' + str(sim.scores))
    logger.debug('Cards left ' + str(np.sum(sim.current_hands)))
    total_scores += sim.scores
logger.info('Final scores of %a' % total_scores)

