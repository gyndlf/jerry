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
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.warning('Dutch is not fully implimented. This extends towards the following')
logger.warning('- Jack and Queen dont allow you to steal / look at cards')
logger.warning('- There is no final round after someone calls Dutch')
logger.warning('- There are no hidden cards (Players see all cards at the start)')
logger.warning('- You always draw from hidden')

# TODO:
#  - Beat me
#  - if you chuck out a card that you have, discard that too
#  - 5 pts if you get rid of a card slot
#  - can give it rewards if its total sum is nice and low

lr = 0.01  # learning rate
eps = 0.9  # random exploration
gma = 0.95  # gamma (how much it looks ahead)
decay_rate = 0.99999  # decay rate

epis = 1000000  # episodes
epis_lag = 10000  # Lag between updating trickle down iterations

players = [Player(learn=True), Player(), Player(), Player(lowest=True)]


# %%
start = time.time()
logger.info('Running %a episodes with trickling every %a episodes.' % (epis, epis_lag))
for game in range(1, epis+1):
    logger.debug('#--- EPISODE ' + str(game) + '---#')
    for p in players:
        p.reset()
    turn = np.random.randint(4)  # random player to start
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
        logger.debug('Turn %a' % turn)

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

        if end:
            # Just run one last round (bypass the normal round system)
            logger.debug('Game over.')
            # Find who has the lowest score
            scores = [p.score() for p in players]
            winner = scores.index(max(scores))  # Who got the lowest score (points are negative)
            logger.debug('Scores of %a' % scores)
            logger.debug('Player %a won!' % winner)
            for i, p in enumerate(players):
                s = p.gen_state()
                # a = p.choice(s, eps=eps)  # Overwritten with 4 for calling dutch
                new_s, discard, end = p.step(5)
                score = p.score()
                if i == winner:
                    score += 10  # Bonus points for getting the lowest score
                p.learn(s, 5, new_s, r=score, lr=lr, gma=gma)  # How good it was to be in this state
            done = True

    # After the round pass onto next system
    if game % epis_lag == 0:
        logger.debug('Trickling down q table')
        est = ((time.time()-start)/game * (epis-game)/60).__round__(2)
        print('\rAt episode %a/%a. Est %a mins remaining.' % (game, epis, est), end='')
        # Player 0 => Player 1 => Player 2 => Player 3
        #players[3].Q = players[2].Q
        players[2].Q = players[1].Q
        players[1].Q = players[0].Q

print()
logger.info('Done.')
logger.info('Took %a mins.' % (((time.time()-start)/60).__round__(2)))
# np.save('q-table.npy', players[0].Q)
