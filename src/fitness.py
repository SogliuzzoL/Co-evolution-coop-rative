# fitness.py
"""
Calcul des fonctions objectives pour l'optimisation :
- Couverture de la surface
- Chevauchement des zones éclairées
"""

import numpy as np
from config import LAMP_RADIUS, SQUARE_SIZE, GRID_RESOLUTION


def coverage(individual):
    """
    Calcule la proportion de la surface couverte par les lampes.

    Args:
        individual: Liste des positions [(x,y), ...] des lampes

    Returns:
        float: Proportion couverte [0-1]
    """
    # Création d'une grille de points
    grid_x, grid_y = np.meshgrid(
        np.linspace(0, SQUARE_SIZE, GRID_RESOLUTION),
        np.linspace(0, SQUARE_SIZE, GRID_RESOLUTION)
    )
    points = np.vstack([grid_x.ravel(), grid_y.ravel()]).T

    # Calcul des points couverts
    covered = np.zeros(points.shape[0], dtype=bool)
    r = LAMP_RADIUS

    for (x, y) in individual:
        dist = np.linalg.norm(points - np.array([x, y]), axis=1)
        covered |= dist <= r

    return np.sum(covered) / len(covered)


def overlap(individual):
    """
    Calcule la surface totale de chevauchement entre les lampes.

    Args:
        individual: Liste des positions [(x,y), ...] des lampes

    Returns:
        float: Surface totale de chevauchement
    """
    r = LAMP_RADIUS
    overlap_area = 0.0

    def circle_intersection_area(d, r):
        """Calcule l'aire d'intersection de deux cercles de rayon r séparés par d."""
        if d >= 2*r:
            return 0.0
        part1 = r*r * np.arccos(d/(2*r))
        part2 = (d/2)*np.sqrt(4*r*r - d*d)
        return 2*(part1 - part2)

    # Calcul des chevauchements pour chaque paire de lampes
    n = len(individual)
    for i in range(n):
        for j in range(i+1, n):
            d = np.linalg.norm(
                np.array(individual[i]) - np.array(individual[j]))
            overlap_area += circle_intersection_area(d, r)

    return overlap_area


def evaluate_individual_multiobj(individual):
    """
    Évalue une solution selon les deux critères d'optimisation.

    Args:
        individual: Solution à évaluer

    Returns:
        tuple: (couverture, -chevauchement) à maximiser
    """
    cov = coverage(individual)
    ovlp = overlap(individual)
    return (cov, -ovlp)
