# %%
# d6636
# The code to run the heart learning system.

from Player import Player
import numpy as np
import time
import logging

logger = logging.getLogger('dutch-gen')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
#ch.setLevel(logging.INFO)  # Set the level here
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.warning('Dutch is not fully implimented. This extends towards the following')
logger.warning('- Jack and Queen dont allow you to steal / look at cards')
logger.warning('- There is no final round after someone calls Dutch')
logger.warning('- There are no hidden cards (Players see all cards at the start)')

lr = 0.01  # learning rate
eps = 0.9  # random exploration
gma = 0.95  # gamma (how much it looks ahead)
decay_rate = 0.99999  # decay rate

epis = 1000000  # episodes
epis_lag = 10000  # Lag between updating trickle down iterations

players = [Player(learn=True), Player(), Player(), Player()]


# %%
start = time.time()
logger.info('Running %a episodes with trickling every %a episodes.' % (epis, epis_lag))
for game in range(1, epis):
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
                s = p.gen_state()
                a = p.choice(s, eps=eps)
                new_s, discard, end = p.step(a)
                score = p.score()
                # TODO:
                #  - Make it being in this state and calling dutch is this good
                #  - Also make it +10 if you have the lowest score
                #  - Make it so if you call dutch you only update the q table once
                p.learn(s, a, new_s, r=score, lr=lr, gma=gma)  # How good it was to be in this state
            done = True

    # After the round pass onto next system
    if game % epis_lag == 0:
        logger.debug('Trickling down q table')
        est = ((time.time()-start)/game * (epis-game)/60).__round__(2)
        print('\rAt episode %a. Est %a mins remaining.' % (game, est), end='')
        # Player 1 => Player 2 => Player 3 => Player 4
        players[3].Q = players[2].Q
        players[2].Q = players[1].Q
        players[1].Q = players[0].Q

logger.info('\nDone.')
logger.info('Took %a mins.' % (((time.time()-start)/60).__round__(2)))
np.save('q-table.npy', players[0].Q)