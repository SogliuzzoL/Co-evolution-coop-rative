# population.py
"""
Gestion des populations pour l'algorithme génétique.
"""

import random
from config import NUM_LAMPS, POP_SIZE, SQUARE_SIZE


def initialize_population():
    """
    Initialise les sous-populations pour chaque lampe.

    Returns:
        list: Liste de sous-populations, chacune contenant POP_SIZE individus
    """
    populations = []
    for _ in range(NUM_LAMPS):
        pop = [
            (random.uniform(0, SQUARE_SIZE), random.uniform(0, SQUARE_SIZE))
            for _ in range(POP_SIZE)
        ]
        populations.append(pop)
    return populations
