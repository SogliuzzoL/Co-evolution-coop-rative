# config.py
"""
Configuration globale du système d'optimisation des lampes.
Contient tous les paramètres ajustables de l'algorithme.
"""

# Paramètres du problème
SQUARE_SIZE = 1.0        # Taille du carré (1x1 unité)
LAMP_RADIUS = 0.2        # Rayon d'éclairage des lampes

# Paramètres de l'algorithme génétique
NUM_LAMPS = 9            # Nombre de lampes à optimiser
POP_SIZE = 30            # Taille de chaque sous-population
MAX_GENERATIONS = 25     # Nombre maximal de générations

# Paramètres de mutation
MUTATION_STDDEV = 0.05   # Écart-type pour la mutation gaussienne
MUTATION_PROB = 0.3      # Probabilité qu'une mutation se produise

# Paramètres de calcul de fitness
GRID_RESOLUTION = 100    # Résolution de la grille pour calculer la couverture
