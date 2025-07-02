# visualization.py
"""
Fonctions de visualisation pour l'animation des solutions.
"""

import plotly.graph_objects as go
from config import SQUARE_SIZE, LAMP_RADIUS


def assemble_solution(best_individuals):
    """
    Combine les meilleurs individus de chaque sous-population en une solution complète.

    Args:
        best_individuals: Liste des meilleurs individus par lampe

    Returns:
        list: Solution complète [(x1,y1), (x2,y2), ...]
    """
    return best_individuals


def create_frame(lamps_positions):
    """
    Crée un cadre d'animation pour une configuration de lampes donnée.

    Args:
        lamps_positions: Positions des lampes [(x,y), ...]

    Returns:
        tuple: (shapes, scatter) pour Plotly
    """
    # Création du carré de base
    shapes = [dict(
        type="rect",
        x0=0, y0=0, x1=SQUARE_SIZE, y1=SQUARE_SIZE,
        line=dict(color="black"),
        fillcolor="white"
    )]

    # Ajout des cercles pour chaque lampe
    for pos in lamps_positions:
        shapes.append(dict(
            type="circle",
            xref="x", yref="y",
            x0=pos[0] - LAMP_RADIUS, y0=pos[1] - LAMP_RADIUS,
            x1=pos[0] + LAMP_RADIUS, y1=pos[1] + LAMP_RADIUS,
            fillcolor="orange",
            opacity=0.7,
            line=dict(color="darkorange")
        ))

    # Points centraux des lampes
    scatter = go.Scatter(
        x=[p[0] for p in lamps_positions],
        y=[p[1] for p in lamps_positions],
        mode='markers',
        marker=dict(color='red', size=8),
        name='Positions des lampes',
        xaxis='x1',
        yaxis='y1'
    )

    return shapes, scatter
