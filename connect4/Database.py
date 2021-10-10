# d7141
#
# Code to access the database

import logging
import sqlite3
import pickle
from collections import defaultdict
log = logging.getLogger(__name__)

FILENAME = "evolution.db"


def create_db():
    """Create the databse."""
    conn = sqlite3.connect(FILENAME)
    cur = conn.cursor()
    log.info("Creating creatures table in db")
    cur.execute("CREATE TABLE creatures (generation INT, uid TEXT, species TEXT, pickle TEXT)")
    conn.commit()
    conn.close()


def clear_db():
    """Clear the database (Reset)"""
    conn = sqlite3.connect(FILENAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM creatures")
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


def retrieve_creature(uid):
    """Load the creature corresponding to the uid"""
    conn = sqlite3.connect(FILENAME)
    cur = conn.cursor()
    creature = cur.execute("SELECT pickle FROM creatures WHERE uid = ?", (uid,)).fetchone()
    conn.commit()
    conn.close()
    log.info(f"Retrieved {uid} from {FILENAME}")
    return pickle.loads(creature[0])
