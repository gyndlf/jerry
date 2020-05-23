# %%
# d6636
# The code to run the heart learning system.

from Player import Player
import numpy as np

import logging

logger = logging.getLogger('dutch')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
#ch.setLevel(logging.INFO)  # Set the level here
ch.setFormatter(formatter)
logger.addHandler(ch)

lr = 0.01  # learning rate
eps = 0.5  # random exploration
gma = 0.9  # gamma
epis = 10000000  # episodes
decay_rate = 0.9999  # decay rate
rev_list = []  # rewards per episode

players = [Player(), Player(), Player(), Player()]


# %%
logger.info('Running %a game.' % epis)
for game in range(epis):
    logger.debug('#--- GAME ' + str(game) + '---#')
    for p in players:
        p.reset()
    turn = np.random.randint(4)
    logger.debug('Turn %a' % turn)
    done = False
    eps *= decay_rate  # slow the random exploration

    while not done:  # iterate through each player again and again players
        # sim.print_cards()
        # For each round:
        # For each player in round
        # Choose an action depending on the state
        # Do the action
        # Compute the reward
        # (Q table modification if applicable)
        # Change new state, to current state
        # Compute points

        # Generate state
        s = players[turn].gen_state()
        logger.debug('State of %a' % s)

        # Choose state
        q = players[turn].Q
        logger.debug('Q table %a' % q[s[0], s[1], s[2], s[3], s[4]])
        if np.random.random() < eps or np.sum(q[s[0], s[1], s[2], s[3], s[4]]) is 0:
            logger.debug('RANDOM ACTION')
            a = np.random.randint(0, 5)  # random choice
        else:
            logger.debug('Q table action')
            a = np.argmax(q[s[0], s[1], s[2], s[3], s[4]])

        new_s, reward, end = players[turn].step(a)

        # Update the Q table
        q[s[0], s[1], s[2], s[3], s[4], a] = \
            q[s[0], s[1], s[2], s[3], s[4], a] + \
            lr*(reward + gma*np.max(q[new_s[0], new_s[1], new_s[2], new_s[3], new_s[4], :]) -
                q[s[0], s[1], s[2], s[3], s[4], a])

        players[turn].Q = q  # Save it

        # Update the turn counter
        turn += 1
        if turn > 3:
            turn -= 4  # Loop back around
        logger.debug('Turn %a' % turn)

        if end:
            # Just run one last round (bypass the normal round system)
            logger.debug('Last round')
            done = True

