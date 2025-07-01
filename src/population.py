# population.py
import random
from config import NUM_LAMPS, POP_SIZE, SQUARE_SIZE

def initialize_population():
    """
    Initialise une liste de sous-populations,
    une par lampe. Chaque sous-population contient POP_SIZE individus
    chacun défini par (x,y) dans le carré.
    """
    populations = []
    for _ in range(NUM_LAMPS):
        pop = []
        for _ in range(POP_SIZE):
            x = random.uniform(0, SQUARE_SIZE)
            y = random.uniform(0, SQUARE_SIZE)
            pop.append((x, y))
        populations.append(pop)
    return populations
