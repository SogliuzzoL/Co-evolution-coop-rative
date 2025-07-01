import random
from datetime import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from fitness import fitness_globale
from itertools import combinations
from parameters import group_size
import numpy as np
from parameters import radius

generations = []


def find_best_group_by_surface(candidates, max_samples=100):
    best_group = None
    max_surface = float('-inf')
    all_groups = list(combinations(candidates, group_size))
    if len(all_groups) > max_samples:
        sampled_groups = random.sample(all_groups, max_samples)
    else:
        sampled_groups = all_groups

    for candidate_group in sampled_groups:
        surface, _ = fitness_globale(candidate_group)
        current_surface = -surface  # car fitness_globale donne surface négative ?
        if current_surface > max_surface:
            max_surface = current_surface
            best_group = candidate_group
    return best_group


def find_best_group_by_overlapping(candidates, max_samples=100):
    best_group = None
    min_overlapping = float('inf')
    all_groups = list(combinations(candidates, group_size))
    if len(all_groups) > max_samples:
        sampled_groups = random.sample(all_groups, max_samples)
    else:
        sampled_groups = all_groups

    for candidate_group in sampled_groups:
        _, overlapping = fitness_globale(candidate_group)
        if overlapping < min_overlapping:
            min_overlapping = overlapping
            best_group = candidate_group
    return best_group


def find_best_group_compromise(candidates, max_samples=100, alpha=0.5):
    """
    Trouve un groupe qui optimise un compromis entre surface et overlapping.
    alpha contrôle le poids donné à la surface (entre 0 et 1).
    score = alpha * surface_norm - (1 - alpha) * overlapping_norm
    (Il faut normaliser surface et overlapping pour qu'ils soient comparables.)
    """
    best_group = None
    best_score = float('-inf')
    all_groups = list(combinations(candidates, group_size))
    if len(all_groups) > max_samples:
        sampled_groups = random.sample(all_groups, max_samples)
    else:
        sampled_groups = all_groups

    # Pré-calcul pour normalisation min/max
    surfaces = []
    overlappings = []
    for candidate_group in sampled_groups:
        s, o = fitness_globale(candidate_group)
        surfaces.append(-s)  # surface positive
        overlappings.append(o)

    min_surface, max_surface = min(surfaces), max(surfaces)
    min_overlap, max_overlap = min(overlappings), max(overlappings)

    def normalize(value, vmin, vmax):
        if vmax == vmin:
            return 0.5  # éviter division par 0
        return (value - vmin) / (vmax - vmin)

    for candidate_group, s, o in zip(sampled_groups, surfaces, overlappings):
        s_norm = normalize(s, min_surface, max_surface)
        o_norm = normalize(o, min_overlap, max_overlap)
        score = alpha * s_norm - (1 - alpha) * o_norm
        if score > best_score:
            best_score = score
            best_group = candidate_group

    return best_group


def create_animation(generations):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            "Surface vs Overlapping (Individus)",
            f"Groupe de {group_size} lampes",
            "Évolution Surface & Overlapping (Individus)",
            f"Évolution Surface & Overlapping (Groupe {group_size})"
        ],
        vertical_spacing=0.2
    )

    annotation_x = 0.75
    annotation_y = 1.05

    fig.update_layout(annotations=[dict(
        x=annotation_x,
        y=annotation_y,
        xref="paper",
        yref="paper",
        text="",
        showarrow=False,
        font=dict(size=12, color="black"),
        align="center"
    )])

    # Stockage moyennes par génération
    mean_surfaces = []
    mean_overlappings = []
    group_surfaces = []
    group_overlappings = []
    gens = []

    frames = []
    for gen, data, candidates in generations:
        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Génération {gen} en cours...")

        surface = [d[0] for d in data]
        overlapping = [d[1] for d in data]

        mean_surfaces.append(np.mean(surface))
        mean_overlappings.append(np.mean(overlapping))
        gens.append(gen)

        groupe = find_best_group_compromise(candidates)
        fitness_groupe = fitness_globale(groupe)

        group_surfaces.append(-fitness_groupe[0])
        group_overlappings.append(fitness_groupe[1])

        scatter_trace = go.Scatter(
            x=overlapping,
            y=surface,
            mode='markers',
            marker=dict(color='blue'),
            name="Individus"
        )

        shapes = [dict(
            type="circle",
            xref="x2",
            yref="y2",
            x0=x - radius,
            y0=y - radius,
            x1=x + radius,
            y1=y + radius,
            line=dict(color="black"),
            fillcolor="blue",
            opacity=0.3
        ) for x, y in groupe]

        annotation_text = (
            f"Fitness groupe {group_size} : Surface = {-fitness_groupe[0]:.3f}, "
            f"Overlapping = {fitness_groupe[1]:.3f}"
        )

        frame = go.Frame(
            data=[scatter_trace],
            name=f"Gen {gen}",
            layout=go.Layout(
                shapes=shapes,
                annotations=[dict(
                    x=annotation_x,
                    y=annotation_y,
                    xref="paper",
                    yref="paper",
                    text=annotation_text,
                    showarrow=False,
                    font=dict(size=12, color="black"),
                    align="center"
                )]
            )
        )
        frames.append(frame)

    # Traces initiales vides pour animation (col 1 et 2)
    fig.add_trace(go.Scatter(x=[], y=[], mode='markers',
                  name="Individus"), row=1, col=1)
    fig.add_trace(go.Scatter(x=[], y=[], mode='markers',
                  name=f"Groupe {group_size}"), row=1, col=2)

    # Courbes fixes en bas à gauche (col 1, row 2)
    fig.add_trace(go.Scatter(
        x=gens, y=mean_surfaces,
        mode='lines+markers',
        name='Surface moyenne',
        line=dict(color='green')
    ), row=2, col=1)

    fig.add_trace(go.Scatter(
        x=gens, y=mean_overlappings,
        mode='lines+markers',
        name='Overlapping moyen',
        line=dict(color='red')
    ), row=2, col=1)

    # Courbes fixes en bas à droite (col 2, row 2)
    fig.add_trace(go.Scatter(
        x=gens, y=group_surfaces,
        mode='lines+markers',
        name='Surface groupe',
        line=dict(color='green', dash='dash')
    ), row=2, col=2)

    fig.add_trace(go.Scatter(
        x=gens, y=group_overlappings,
        mode='lines+markers',
        name='Overlapping groupe',
        line=dict(color='red', dash='dash')
    ), row=2, col=2)

    fig.update_layout(
        title=f"Évolution et Fitness Globale du groupe de {group_size} lampes",
        xaxis=dict(title="Overlapping"),
        yaxis=dict(title="Surface"),
        xaxis2=dict(title="x (lampes)", range=[0, 1]),
        yaxis2=dict(title="y (lampes)", range=[
                    0, 1], scaleanchor="x2", scaleratio=1),
        xaxis3=dict(title="Génération"),
        yaxis3=dict(title="Valeur"),
        xaxis4=dict(title="Génération"),
        yaxis4=dict(title="Valeur"),
        updatemenus=[{
            "type": "buttons",
            "buttons": [
                {"label": "Play", "method": "animate",
                 "args": [None, {"frame": {"duration": 500, "redraw": True}}]},
                {"label": "Pause", "method": "animate",
                 "args": [[None], {"mode": "immediate",
                                   "frame": {"duration": 0},
                                   "transition": {"duration": 0}}]}
            ]
        }],
        sliders=[{
            "steps": [
                {"method": "animate",
                 "args": [[f.name], {"mode": "immediate",
                                     "frame": {"duration": 0},
                                     "transition": {"duration": 0}}],
                 "label": f.name
                 } for f in frames
            ]
        }],
        height=700,
        width=1000
    )

    fig.frames = frames
    fig.write_html("animation.html")
