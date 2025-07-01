# animation.py
"""
Module d'animation pour visualiser l'évolution des solutions au fil des générations.
Gère l'exécution de l'algorithme génétique et la création de l'animation interactive.
"""

import plotly.graph_objects as go
from config import NUM_LAMPS, POP_SIZE, MAX_GENERATIONS, SQUARE_SIZE, LAMP_RADIUS
from population import initialize_population
from fitness import evaluate_individual_multiobj
from genetic_ops import tournament_selection, crossover, mutate, non_dominated_sort
from visualization import create_frame, assemble_solution


def run_and_animate():
    """Exécute l'algorithme génétique et génère l'animation des résultats."""
    # Initialisation
    populations = initialize_population()
    best_individuals = [pop[0] for pop in populations]
    frames = []
    fitness_progress = []

    # Boucle d'évolution
    for gen in range(MAX_GENERATIONS):
        # Évaluation de la solution globale
        solution = assemble_solution(best_individuals)
        global_fitness = evaluate_individual_multiobj(solution)
        fitness_progress.append(global_fitness)

        # Création du cadre d'animation pour cette génération
        shapes, scatter = create_frame(solution)
        frames.append(
            go.Frame(
                data=[scatter],
                layout=dict(shapes=shapes),
                name=str(gen)
            )
        )

        # Optimisation pour chaque lampe
        for i in range(NUM_LAMPS):
            # Évaluation des individus
            fitnesses = []
            for individual in populations[i]:
                temp_solution = best_individuals.copy()
                temp_solution[i] = individual
                fit = evaluate_individual_multiobj(temp_solution)
                fitnesses.append(fit)

            # Sélection des non-dominés
            non_dom = non_dominated_sort(populations[i], fitnesses)
            best_cand = max(
                non_dom,
                key=lambda ind: evaluate_individual_multiobj(
                    [ind if idx == i else best_individuals[idx]
                        for idx in range(NUM_LAMPS)]
                )[0]
            )
            best_individuals[i] = best_cand

            # Reproduction
            selected = tournament_selection(populations[i], fitnesses)
            new_pop = []
            for j in range(0, len(selected), 2):
                parent1 = selected[j]
                parent2 = selected[(j + 1) % len(selected)]
                child1 = crossover(parent1, parent2)
                child2 = crossover(parent2, parent1)
                child1 = mutate(child1)
                child2 = mutate(child2)
                new_pop.extend([child1, child2])
            populations[i] = new_pop[:POP_SIZE]

        # Affichage des résultats
        print(
            f"Génération {gen+1}/{MAX_GENERATIONS} - "
            f"Couverture: {global_fitness[0]*100:.2f}%, "
            f"Chevauchement: {-global_fitness[1]:.4f}"
        )

    # Affichage de la solution finale
    print("\nMeilleure configuration finale des lampes :")
    for i, lamp in enumerate(best_individuals):
        print(f"  Lampe {i+1}: ({lamp[0]:.3f}, {lamp[1]:.3f})")

    # Configuration de l'animation
    slider_steps = [
        dict(
            method="animate",
            args=[[frame.name],
                  dict(mode="immediate", frame=dict(duration=0, redraw=True),
                       transition=dict(duration=0))],
            label=f"Gen {i+1}"
        )
        for i, frame in enumerate(frames)
    ]

    sliders = [dict(
        active=0,
        pad={"t": 50},
        steps=slider_steps,
        currentvalue={"prefix": "Génération : "},
        x=0.1,
        y=0,
        len=0.8,
    )]

    # Création des traces pour les indicateurs de performance
    coverage_trace = go.Scatter(
        x=list(range(1, MAX_GENERATIONS + 1)),
        y=[f[0] for f in fitness_progress],
        mode='lines+markers',
        name='Couverture',
        yaxis='y2',
        xaxis='x2'
    )
    overlap_trace = go.Scatter(
        x=list(range(1, MAX_GENERATIONS + 1)),
        y=[-f[1] for f in fitness_progress],
        mode='lines+markers',
        name='Chevauchement',
        yaxis='y2',
        xaxis='x2'
    )

    # Création de la figure finale
    fig = go.Figure(
        data=list(frames[0].data) + [coverage_trace, overlap_trace],
        layout=go.Layout(
            title="Optimisation du placement des lampes",
            shapes=frames[0].layout.shapes,
            xaxis=dict(
                domain=[0, 0.45],
                range=[0, SQUARE_SIZE],
                scaleanchor="y",
                scaleratio=1,
                autorange=False
            ),
            yaxis=dict(
                domain=[0, 1],
                range=[0, SQUARE_SIZE],
                autorange=False
            ),
            xaxis2=dict(domain=[0.55, 1], title="Génération"),
            yaxis2=dict(domain=[0, 1], title="Valeur", autorange=True),
            sliders=sliders,
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(
                    label="Play",
                    method="animate",
                    args=[None, {
                        "frame": {"duration": 300, "redraw": True},
                        "fromcurrent": True,
                        "transition": {"duration": 0}
                    }]
                )]
            )]
        ),
        frames=frames
    )

    # Sauvegarde et affichage
    fig.write_html("optimisation_lampes.html", auto_open=True)
