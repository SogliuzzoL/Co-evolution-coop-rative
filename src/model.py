from fitness import fitness_globale
import numpy as np
import random


def random_generator():
    return random.Random()


def generator(random: random, args: dict):
    x = random.uniform(0, 1)
    y = random.uniform(0, 1)
    return [x, y]


def evaluator(candidates, args):
    group_min = args["group_min"]
    group_max = args["group_max"]
    nb_group = args["nb_group"]

    # Génération des groupes
    groups = []
    for _ in range(nb_group):
        group_size = int(random.uniform(group_min, group_max))
        group = random.sample(candidates, group_size)
        groups.append(group)

    # Initialiser les contributions
    fitness_lamp = [[0, 0] for _ in candidates]
    count_lamp = [0 for _ in candidates]

    # Map index pour retrouver les candidats
    candidate_index = {tuple(c): i for i, c in enumerate(candidates)}

    for group in groups:
        fitness_group = fitness_globale(group)
        for candidate in group:
            subgroup = [c for c in group if c != candidate]
            fitness_subgroup = fitness_globale(subgroup)
            contribution = [fitness_group[i] - fitness_subgroup[i]
                            for i in range(2)]
            idx = candidate_index[tuple(candidate)]
            for i in range(2):
                fitness_lamp[idx][i] += contribution[i]
            count_lamp[idx] += 1

    # Normaliser
    for i in range(len(candidates)):
        if count_lamp[i] == 0:
            fitness_lamp[i] = [0, 1]
        else:
            fitness_lamp[i] = [
                fitness_lamp[i][0] / count_lamp[i],
                fitness_lamp[i][1] / count_lamp[i]
            ]

    return fitness_lamp


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


def crossover(random: random, candidates: list, args: dict):
    offspring = []
    for i in range(0, len(candidates), 2):
        if i + 1 < len(candidates):
            parent1 = candidates[i]
            parent2 = candidates[i + 1]
            alpha = random.uniform(-0.2, 1.2)
            child1 = [
                alpha * parent1[0] + (1 - alpha) * parent2[0],
                alpha * parent1[1] + (1 - alpha) * parent2[1],
            ]
            child2 = [
                (1 - alpha) * parent1[0] + alpha * parent2[0],
                (1 - alpha) * parent1[1] + alpha * parent2[1],
            ]
            child1[0] = max(0, min(child1[0], 1))
            child1[1] = max(0, min(child1[1], 1))
            child2[0] = max(0, min(child2[0], 1))
            child2[1] = max(0, min(child2[1], 1))
            offspring.extend([child1, child2])
        else:
            offspring.append(candidates[i])
    return candidates + offspring
