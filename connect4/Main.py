# d7148
#
# Run the generation
import logging
import logging.config
logging.config.fileConfig("logging.conf")
log = logging.getLogger(__name__)

import Generation
import Database
import Creature


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Connect 4 reinforcement learner via group evolution simulation")
    parser.add_argument(
        "--new", action='store_true', default=False, help="Reset the database and start a new evolution"
    )
    parser.add_argument(
        "--size", type=int, default=100, help="Size of generation if starting new"
    )
    parser.add_argument(
        "-g", "--gens", type=int, required=True, help="Number of generations to run"
    )
    args = parser.parse_args()

    log.debug(f"Using args: {args}")
    log.info(f"Running {args.gens} generations")
    if args.new:
        # Start a new generation
        creatures = Creature.new_creatures(args.size)
        Generation.run_generations(creatures, args.gens)
    else:
        # Load the last generation
        log.warning(f"Assuming creatures exist in the database")
        lastgen, creatures = Database.retrieve_last_gen()
        Generation.run_generations(creatures, args.gens, genstart=lastgen)
