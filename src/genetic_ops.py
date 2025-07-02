# genetic_ops.py
"""
Opérations génétiques pour l'algorithme évolutionnaire :
- Sélection
- Croisement
- Mutation
- Tri non-dominé
"""

import random
from config import MUTATION_STDDEV, MUTATION_PROB, SQUARE_SIZE


def dominates(fitness_a, fitness_b):
    """
    Détermine si une solution en domine une autre (au sens de Pareto).

    Args:
        fitness_a: Tuple de valeurs objectives
        fitness_b: Tuple de valeurs objectives

    Returns:
        bool: True si a domine b
    """
    return (all(a >= b for a, b in zip(fitness_a, fitness_b)) and
            any(a > b for a, b in zip(fitness_a, fitness_b)))


def non_dominated_sort(population, fitnesses):
    """
    Identifie les solutions non dominées dans une population.

    Args:
        population: Liste des solutions
        fitnesses: Liste des valeurs objectives correspondantes

    Returns:
        list: Solutions non dominées
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
    Sélection par tournoi avec k participants.

    Args:
        population: Population source
        fitnesses: Valeurs objectives
        k: Nombre de participants par tournoi

    Returns:
        list: Individus sélectionnés
    """
    selected = []
    n = len(population)
    for _ in range(n):
        # Sélection des participants au tournoi
        aspirants_idx = random.sample(range(n), k)
        aspirants = [population[i] for i in aspirants_idx]
        aspirants_fit = [fitnesses[i] for i in aspirants_idx]

        # Choix du gagnant parmi les non-dominés
        non_dom = non_dominated_sort(aspirants, aspirants_fit)
        winner = random.choice(
            non_dom) if non_dom else random.choice(aspirants)
        selected.append(winner)
    return selected


def crossover(parent1, parent2):
    """
    Croisement par moyenne des positions parentales.

    Args:
        parent1: Premier parent (x, y)
        parent2: Second parent (x, y)

    Returns:
        tuple: Enfant (x, y)
    """
    x = (parent1[0] + parent2[0]) / 2
    y = (parent1[1] + parent2[1]) / 2
    return (x, y)


def blend_crossover(parent1, parent2, alpha=0.5):
    """
    Croisement par blend crossover (BLX-α) entre deux parents.

    Args:
        parent1: Premier parent (x, y)
        parent2: Second parent (x, y)
        alpha: Paramètre de dispersion (par défaut: 0.5)

    Returns:
        tuple: Enfant (x, y) généré dans l'intervalle étendu
    """
    # Calcul des intervalles pour chaque dimension
    x_min = min(parent1[0], parent2[0])
    x_max = max(parent1[0], parent2[0])
    x_range = x_max - x_min
    x_child = x_min - alpha * x_range + \
        (1 + 2 * alpha) * x_range * random.random()

    y_min = min(parent1[1], parent2[1])
    y_max = max(parent1[1], parent2[1])
    y_range = y_max - y_min
    y_child = y_min - alpha * y_range + \
        (1 + 2 * alpha) * y_range * random.random()

    return (x_child, y_child)


def mutate(individual):
    """
    Mutation gaussienne avec probabilité MUTATION_PROB.

    Args:
        individual: Solution à muter

    Returns:
        tuple: Solution mutée (ou identique)
    """
    if random.random() < MUTATION_PROB:
        x = individual[0] + random.gauss(0, MUTATION_STDDEV)
        y = individual[1] + random.gauss(0, MUTATION_STDDEV)
        # Contraintes aux limites du carré
        x = min(max(0, x), SQUARE_SIZE)
        y = min(max(0, y), SQUARE_SIZE)
        return (x, y)
    return individual
