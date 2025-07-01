import numpy as np
from parameters import radius


def fitness_nombre_lampes(groupe):
    return len(groupe)


def fitness_portion_aire(groupe, discretization=10):
    step = 1 / discretization
    x = np.linspace(0, 1 - step, discretization)
    y = np.linspace(0, 1 - step, discretization)
    X, Y = np.meshgrid(x, y)
    coverage_mask = np.zeros(X.shape, dtype=bool)

    for (cx, cy) in groupe:
        dist = np.sqrt((X - cx)**2 + (Y - cy)**2)
        coverage_mask |= (dist <= radius)  # union des zones couvertes

    coverage = np.sum(coverage_mask)
    total_area = discretization ** 2
    return coverage / total_area


def fitness_overlapping(groupe, discretization=100):
    step = 1 / discretization
    x = np.linspace(0, 1 - step, discretization)
    y = np.linspace(0, 1 - step, discretization)
    X, Y = np.meshgrid(x, y)

    coverage_count = np.zeros(X.shape, dtype=int)

    for (cx, cy) in groupe:
        dist = np.sqrt((X - cx)**2 + (Y - cy)**2)
        coverage_count += (dist <= radius).astype(int)

    # Overlaps = total coverage count minus number of covered points (once)
    overlaps = np.sum(coverage_count - 1 * (coverage_count > 0))
    total_area = discretization ** 2
    return overlaps / total_area


def fitness_globale(groupe):
    return [-fitness_portion_aire(groupe), fitness_overlapping(groupe)]
