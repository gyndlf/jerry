# %%
# d6636
# The code to run the heart learning system.

from Player import Player
import numpy as np
import time
import logging

logger = logging.getLogger('dutch')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
#ch.setLevel(logging.INFO)  # Set the level here
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.warning('Dutch is not fully implimented. This extends towards the following')
logger.warning('- Jack and Queen dont allow you to steal / look at cards')
logger.warning('- There is no final round after someone calls Dutch')

lr = 0.01  # learning rate
eps = 0.9  # random exploration
gma = 0.95  # gamma (how much it looks ahead)
decay_rate = 0.999999  # decay rate

epis = 100000  # episodes
epis_lag = 100  # Lag between updating trickle down iterations

rev_list = []  # rewards per episode

players = [Player(learn=True), Player(), Player(), Player()]


# %%
start = time.time()
logger.info('Running %a episodes with trickling every %a episodes.' % (epis, epis_lag))
for game in range(epis):
    logger.debug('#--- EPISODE ' + str(game) + '---#')
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
        a = players[turn].choice(s, eps=eps)

        new_s, discard, end = players[turn].step(a)

        # Update the Q table
        players[turn].learn(s, a, new_s, r=0, lr=lr, gma=gma)  # No reward

        # See if any player has the same card as the one played
        if discard is not None:
            # They have chosen a card and swapped one out
            for player in players:
                if discard in player.hand:
                    player.hand[player.hand.index(discard)] = 0

        # Update the turn counter
        turn += 1
        if turn > 3:
            turn -= 4  # Loop back around
        logger.debug('Turn %a' % turn)

        if end:
            # Just run one last round (bypass the normal round system)
            logger.debug('Last round')

            # Find who has the lowest score
            for p in players:
                score = p.score()
                p.learn(s, a, new_s, r=score, lr=lr, gma=gma)  # How good it was to be in this state
            done = True

    # After the round pass onto next system
    if epis % epis_lag == 0:
        logger.debug('Trickling down q table')
        # Player 1 => Player 2 => Player 3 => Player 4
        players[3].Q = players[2].Q
        players[2].Q = players[1].Q
        players[1].Q = players[0].Q

logger.info('Done.')
logger.info('Took %a seconds.' % ((start-time.time()).__round__(2)))