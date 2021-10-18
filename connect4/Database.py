# d7141
#
# Code to access the database

import logging
import sqlite3
import pickle
from collections import defaultdict
log = logging.getLogger(__name__)

FILENAME = "evolution.db"

"""
Database contents:
- creatures
    All creatures saved over the generations. Their generation, uid, class and species are stored
- history
    History of the training progress. Stored generation, train time, and species composition
"""


def create_db():
    """Create the database."""
    conn = sqlite3.connect(FILENAME)
    cur = conn.cursor()
    log.info("Creating creatures and history table in db")
    log.warning("Could break if already exists")
    cur.execute("CREATE TABLE creatures (generation INT, uid TEXT, species TEXT, pickle TEXT);")
    cur.execute("CREATE TABLE history (generation INT, time FLOAT, comp TEXT);")
    conn.commit()
    conn.close()


def prune_db():  # TODO: Make it so you keep one per generation
    """Prune the database of all generations except the last one"""
    conn = sqlite3.connect(FILENAME)
    cur = conn.cursor()
    gen = cur.execute("SELECT MAX(generation) FROM creatures;").fetchone()[0]
    cur.execute("DELETE FROM creatures WHERE generation IS NOT ?", (gen,))
    conn.commit()
    conn.close()
    log.warning(f"Pruned {FILENAME} of all generations except generation {gen}")


def clear_db():
    """Clear the database (Reset)"""
    conn = sqlite3.connect(FILENAME)
    cur = conn.cursor()
    log.warning(f"Clearing database of creatures and history in {FILENAME}")
    cur.execute("DELETE FROM creatures")
    cur.execute("DELETE FROM history")
    conn.commit()
    conn.close()


def save_creatures(creatures, gen):
    """Save the creatures to the database"""
    conn = sqlite3.connect(FILENAME)
    cur = conn.cursor()
    species = defaultdict(int)
    for creature in creatures:
        species[creature.species] += 1
        uid = str(gen) + "." + creature.species + "." + str(species[creature.species])
        pic = pickle.dumps(creature)
        cur.execute("INSERT INTO creatures VALUES (?, ?, ?, ?)", (gen, uid, creature.species, pic))
    log.info(f"Saved creatures into {FILENAME}")
    conn.commit()
    conn.close()


def save_history(gen, time, composition):
    """Save the snapshot to the history database"""
    conn = sqlite3.connect(FILENAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO history VALUES (?, ?, ?);", (gen, time, pickle.dumps(composition)))
    log.debug(f"Saved history into {FILENAME}")
    conn.commit()
    conn.close()


def retrieve_history():
    """Retrieve the history of the training (raw)"""
    conn = sqlite3.connect(FILENAME)
    cur = conn.cursor()
    creature = cur.execute("SELECT * FROM history;").fetchall()
    log.info(f"Retrieved history from {FILENAME}")
    conn.commit()
    conn.close()
    return creature


def retrieve_compositions():
    """Retrieve the compositions of trainings"""
    data = retrieve_history()
    comp = []
    for snap in data:
        comp.append(pickle.loads(snap[2]))
    return comp


def retrieve_creature(uid):
    """Load the creature corresponding to the uid"""
    conn = sqlite3.connect(FILENAME)
    cur = conn.cursor()
    creature = cur.execute("SELECT pickle FROM creatures WHERE uid = ?", (uid,)).fetchone()
    conn.commit()
    conn.close()
    log.info(f"Retrieved {uid} from {FILENAME}")
    return pickle.loads(creature[0])


def retrieve_last():
    """Retrieve the last creature saved"""
    conn = sqlite3.connect(FILENAME)
    cur = conn.cursor()
    creature = cur.execute("SELECT uid FROM creatures ORDER BY generation DESC LIMIT 1;").fetchone()
    conn.commit()
    conn.close()
    return creature[0]


def retrieve_last_gen():
    """Retrieve the last generation saved with generation number"""
    conn = sqlite3.connect(FILENAME)
    cur = conn.cursor()
    gen = cur.execute("SELECT MAX(generation) FROM creatures;").fetchone()[0]
    creatures = cur.execute("SELECT pickle FROM creatures WHERE generation = ?", (gen,)).fetchall()
    conn.commit()
    conn.close()
    log.info(f"Loaded last generation {gen} of {len(creatures)} creatures")
    return gen, [pickle.loads(c[0]) for c in creatures]


def main():
    """Run input command args"""
    import argparse
    parser = argparse.ArgumentParser(description="Database functions")
    parser.add_argument(
        "method", type=str, help="Method to run", choices=["clear", "create", "fetch", "prune"]
    )
    parser.add_argument(
        "-db", type=str, required=False, default=FILENAME, help=f"Database file to use [{FILENAME}]"
    )
    args = parser.parse_args()

    db = args.db
    method = args.method
    if method == "clear":
        clear_db()
        print("Cleared database.")
    elif method == "create":
        create_db()
        print("Created database.")
    elif method == "fetch":
        print("Fetch last uid")
        print(retrieve_last())
    elif method == "prune":
        print("Pruning database.")
        prune_db()
    else:
        print("Unknown method")


if __name__ == '__main__':
    main()
