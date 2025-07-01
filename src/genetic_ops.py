# genetic_ops.py
import random
import numpy as np
from config import MUTATION_STDDEV, MUTATION_PROB, SQUARE_SIZE

def dominates(fitness_a, fitness_b):
    """
    fitness_a domine fitness_b si fitness_a est >= fitness_b sur tous objectifs
    et strictement > sur au moins un.
    """
    return all(a >= b for a, b in zip(fitness_a, fitness_b)) and any(a > b for a, b in zip(fitness_a, fitness_b))

def non_dominated_sort(population, fitnesses):
    """
    Retourne la liste des individus non dominés.
    """
    non_dominated = []
    for i, fit_i in enumerate(fitnesses):
        dominated = False
        for j, fit_j in enumerate(fitnesses):
            if j != i and dominates(fit_j, fit_i):
                dominated = True
                break
        if not dominated:
            non_dominated.append(population[i])
    return non_dominated

def tournament_selection(population, fitnesses, k=3):
    """
    Sélection par tournoi classique avec k participants.
    Ici, on fait un tournoi basé sur la dominance.
    """
    selected = []
    n = len(population)
    for _ in range(n):
        aspirants_idx = random.sample(range(n), k)
        aspirants = [population[i] for i in aspirants_idx]
        aspirants_fit = [fitnesses[i] for i in aspirants_idx]

        # Choisir le non dominé dans le tournoi
        non_dom = non_dominated_sort(aspirants, aspirants_fit)
        if non_dom:
            winner = random.choice(non_dom)
        else:
            # si tous dominés mutuellement (rare), prendre au hasard
            winner = random.choice(aspirants)

        selected.append(winner)
    return selected

def crossover(parent1, parent2):
    """
    Croisement simple : moyenne des positions.
    parent1, parent2 : tuples (x, y)
    """
    x = (parent1[0] + parent2[0]) / 2
    y = (parent1[1] + parent2[1]) / 2
    return (x, y)

def mutate(individual):
    """
    Mutation gaussienne avec probabilité.
    """
    if random.random() < MUTATION_PROB:
        x = individual[0] + random.gauss(0, MUTATION_STDDEV)
        y = individual[1] + random.gauss(0, MUTATION_STDDEV)
        # Clamp dans carré
        x = min(max(0, x), SQUARE_SIZE)
        y = min(max(0, y), SQUARE_SIZE)
        return (x, y)
    else:
        return individual
