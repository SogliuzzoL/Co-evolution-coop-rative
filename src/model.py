from individu import Lampe

import inspyred
import numpy as np

import random

def random_generator():
    return random.Random()

def generator(random: random, args: dict):
    population = []

    population_size = args["population_size"]
    r = args["radius"]

    for _ in range(population_size):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        r = r
        lampe = Lampe(x, y, r)
        population.append(lampe)
    return population

def evaluator(candidates, args):
    group_min = args["group_min"]
    group_max = args["group_max"]
    fitness_lamp = {id(candidate) : -np.inf for candidate in candidates}

    # Génération de la taille des groupes
    groups_size = []
    candidates_size = len(candidates)
    while candidates_size > group_min:
        size = random.randint(group_min, min(group_max, candidates_size))
        groups_size.append(size)
        candidates_size -= size

    if candidates_size != 0:
        groups_size.append(candidates_size)

    # Génération des groupes
    groups = []
    candidates_to_visite = candidates.copy()
    for group_size in groups_size:
        group = []
        for _ in range(group_size):
            group.append(candidates_to_visite.pop())
        groups.append(group)

    return groups

def crossover(random, candidates, args) :
  
  fitness_values = evaluator()
  