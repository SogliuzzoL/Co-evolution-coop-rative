import math
import matplotlib.pyplot as plt
import numpy as np
import sys


def fitness_nombre_lampes(groupe):
    return len(groupe)


def fitness_portion_aire(groupe):

    # TODO lower discretization here to speed up computation, increase for increased precision
    discretization = 100
    discretizationStep = 1 / discretization

    totalArea = discretization * discretization
    coverage = 0.0

    for x in np.arange(0.0, 1, discretizationStep):
        for y in np.arange(0.0, 1, discretizationStep):
            for lampe in groupe:
                radius = lampe[2]
                distance = math.sqrt(
                    math.pow(lampe[0] - x, 2) + math.pow(lampe[1] - y, 2))
                if distance <= radius:
                    coverage += 1
                    break
    return coverage / totalArea


def fitness_overlapping(groupe):

    # TODO lower discretization here to speed up computation, increase for increased precision
    discretization = 100
    discretizationStep = 1 / discretization

    totalArea = discretization * discretization
    overlaps = 0

    for x in np.arange(0.0, 1, discretizationStep):
        for y in np.arange(0.0, 1, discretizationStep):
            coveredBylamp = 0
            for lampe in groupe:
                radius = lampe[2]
                distance = math.sqrt(
                    math.pow(lampe[0] - x, 2) + math.pow(lampe[1] - y, 2))
                if distance <= radius:
                    coveredBylamp += 1
            if coveredBylamp > 0:
                overlaps += coveredBylamp - 1
    return overlaps / totalArea


def fitness_globale(groupe):
    return [fitness_nombre_lampes(groupe), -fitness_portion_aire(groupe), fitness_overlapping(groupe)]
