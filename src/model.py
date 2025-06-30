from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting
from fitness import fitness_globale
import numpy as np
import random


def random_generator():
    return random.Random()


def generator(random: random, args: dict):
    r = args["radius"]
    x = random.uniform(0, 1)
    y = random.uniform(0, 1)
    return [x, y, r]


def evaluator(candidates, args):
    group_min = args["group_min"]
    group_max = args["group_max"]

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
    candidates_to_visit = candidates.copy()
    for group_size in groups_size:
        group = []
        for _ in range(group_size):
            group.append(candidates_to_visit.pop())
        groups.append(group)

    # Evaluation des lampes
    fitness_lamp = {}
    for group in groups:
        fitness_group = fitness_globale(group)
        for candidate in group:
            subgroup: list = group.copy()
            subgroup.remove(candidate)
            fitness_subgroup = fitness_globale(subgroup)
            fitness = fitness_group.copy()

            fitness[1] -= fitness_subgroup[1]
            fitness[2] -= fitness_subgroup[2]
            fitness_lamp[id(candidate)] = fitness
    # Retourne une liste des fitness dans l'ordre des candidats
    args["fitness_cache"] = fitness_lamp
    return [fitness_lamp[id(candidate)] for candidate in candidates]


def mutation(random: random, candidates: list, args: dict):
    pm = args["pm"]
    mu = args["mu"]
    sigma = args["sigma"]
    tau = args["tau"]
    for candidate in candidates:
        if random.uniform(0, 1) < pm:
            candidate[0] += random.gauss(mu, sigma)
            candidate[0] = max(0, min(candidate[0], 1))  # borne entre 0 et 1

            candidate[1] += random.gauss(mu, sigma)
            candidate[1] = max(0, min(candidate[1], 1))  # borne entre 0 et 1

            # candidate[2] += random.gauss(mu, sigma)
            # candidate[2] = max(0, min(candidate[2], 1))  # borne entre 0 et 1
    args["sigma"] *= np.exp(random.gauss(sigma=tau))
    return candidates


def blend_crossover(p1, p2, alpha=0.5):
    child = []
    for i in range(len(p1)):
        d = abs(p1[i] - p2[i])
        low = min(p1[i], p2[i]) - alpha * d
        high = max(p1[i], p2[i]) + alpha * d
        gene = random.uniform(low, high)
        if i < 2:  # x, y ∈ [0,1]
            gene = max(0.0, min(1.0, gene))
        child.append(gene)
    return child


def crossover(random, candidates, args):
    group_min = args["group_min"]
    group_max = args["group_max"]
    radius = args["radius"]

    fitness_cache = args["fitness_cache"]

    # 1. Croisement pour créer une descendance
    offspring = []
    while len(offspring) < len(candidates):
        p1, p2 = random.sample(candidates, 2)
        child = blend_crossover(p1, p2)
        offspring.append(child)

    # 2. Évaluation de la descendance
    offspring_fitness = evaluator(offspring, {
        "group_min": group_min,
        "group_max": group_max,
        "radius": radius,
        "fitness_cache": {}
    })

    # Mise à jour du cache fitness pour les enfants
    for c, f in zip(offspring, offspring_fitness):
        # clé modifiée en tuple (immutable) pour dict
        fitness_cache[tuple(c)] = f

    # Combine candidats parents + enfants
    combined = candidates + offspring
    combined_fitness = []
    for ind in combined:
        key = tuple(ind)
        if key in fitness_cache:
            combined_fitness.append(fitness_cache[key])
        else:
            # Si fitness manquant, calculer (au cas où)
            f = evaluator([ind], {
                "group_min": group_min,
                "group_max": group_max,
                "radius": radius,
                "fitness_cache": {}
            })[0]
            fitness_cache[key] = f
            combined_fitness.append(f)
    fitness_array = np.array(combined_fitness)

    nds = NonDominatedSorting()
    fronts = nds.do(fitness_array, only_non_dominated_front=False)

    new_population = []
    for front in fronts:
        if len(new_population) + len(front) <= len(candidates):
            new_population.extend([combined[i] for i in front])
        else:
            rest = len(candidates) - len(new_population)
            # <-- ici conversion en liste
            selected = random.sample(list(front), rest)
            new_population.extend([combined[i] for i in selected])
            break

    return new_population
