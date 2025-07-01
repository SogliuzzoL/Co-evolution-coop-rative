# fitness.py
import numpy as np
from config import LAMP_RADIUS, SQUARE_SIZE, GRID_RESOLUTION

def coverage(individual):
    """
    Calcule la proportion de la surface du carré couverte par les lampes.
    individual : liste de positions [(x,y), ...] d'une solution complète (toutes lampes)
    """
    grid_x, grid_y = np.meshgrid(np.linspace(0, SQUARE_SIZE, GRID_RESOLUTION),
                                 np.linspace(0, SQUARE_SIZE, GRID_RESOLUTION))
    points = np.vstack([grid_x.ravel(), grid_y.ravel()]).T
    covered = np.zeros(points.shape[0], dtype=bool)
    r = LAMP_RADIUS

    for (x, y) in individual:
        dist = np.linalg.norm(points - np.array([x, y]), axis=1)
        covered |= dist <= r

    return np.sum(covered) / len(covered)

def overlap(individual):
    """
    Calcule la surface totale de chevauchement entre lampes.
    individual : liste de positions [(x,y), ...] d'une solution complète (toutes lampes)
    """
    r = LAMP_RADIUS
    overlap_area = 0.0

    def circle_intersection_area(d, r):
        if d >= 2*r:
            return 0.0
        part1 = r*r * np.arccos(d/(2*r))
        part2 = (d/2)*np.sqrt(4*r*r - d*d)
        return 2*(part1 - part2)

    n = len(individual)
    for i in range(n):
        for j in range(i+1, n):
            d = np.linalg.norm(np.array(individual[i]) - np.array(individual[j]))
            overlap_area += circle_intersection_area(d, r)

    return overlap_area

def evaluate_individual_multiobj(individual):
    """
    Retourne un tuple (coverage, -overlap) à maximiser.
    """
    cov = coverage(individual)
    ovlp = overlap(individual)
    return (cov, -ovlp)
