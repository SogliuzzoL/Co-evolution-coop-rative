import numpy as np
import plotly.graph_objects as go
from population import initialize_population
from fitness import evaluate_individual_multiobj
from genetic_ops import tournament_selection, crossover, mutate, non_dominated_sort
from config import NUM_LAMPS, POP_SIZE, MAX_GENERATIONS, SQUARE_SIZE, LAMP_RADIUS


def assemble_solution(best_individuals):
    return best_individuals


def create_frame(lamps_positions):
    shapes = []
    shapes.append(dict(
        type="rect",
        x0=0, y0=0, x1=SQUARE_SIZE, y1=SQUARE_SIZE,
        line=dict(color="black"),
        fillcolor="white"
    ))
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
    scatter = go.Scatter(
        x=[p[0] for p in lamps_positions],
        y=[p[1] for p in lamps_positions],
        mode='markers',
        marker=dict(color='red', size=8),
        name='Lampes',
        xaxis='x1',
        yaxis='y1'
    )
    return shapes, scatter


def run_and_animate():
    populations = initialize_population()
    best_individuals = [pop[0] for pop in populations]
    frames = []
    fitness_progress = []

    for gen in range(MAX_GENERATIONS):
        solution = assemble_solution(best_individuals)
        global_fitness = evaluate_individual_multiobj(solution)
        fitness_progress.append(global_fitness)

        shapes, scatter = create_frame(solution)
        frames.append(go.Frame(data=[scatter], layout=dict(
            shapes=shapes), name=str(gen)))

        for i in range(NUM_LAMPS):
            fitnesses = []
            for individual in populations[i]:
                temp_solution = best_individuals.copy()
                temp_solution[i] = individual
                fit = evaluate_individual_multiobj(temp_solution)
                fitnesses.append(fit)

            non_dom = non_dominated_sort(populations[i], fitnesses)
            best_cand = max(non_dom, key=lambda ind: evaluate_individual_multiobj(
                [ind if idx == i else best_individuals[idx] for idx in range(NUM_LAMPS)])[0])
            best_individuals[i] = best_cand

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

        print(
            f"Génération {gen+1} - Couverture: {global_fitness[0]*100:.2f}%, Overlap: {-global_fitness[1]:.4f}")

    print("\nMeilleure configuration finale des lampes :")
    for i, lamp in enumerate(best_individuals):
        print(f" Lampe {i+1}: ({lamp[0]:.3f}, {lamp[1]:.3f})")

    # Slider animation pour la carte principale (lampes)
    slider_steps = []
    for i in range(len(frames)):
        step = dict(
            method="animate",
            args=[[frames[i].name],
                  dict(mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))],
            label=f"Gen {i+1}"
        )
        slider_steps.append(step)

    sliders = [dict(
        active=0,
        pad={"t": 50},
        steps=slider_steps,
        currentvalue={"prefix": "Génération : "},
        x=0.1,
        y=0,
        len=0.8,
    )]

    # Graphique de la couverture et overlap
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
        name='Overlap',
        yaxis='y2',
        xaxis='x2'
    )

    # Layout avec deux graphiques côte à côte
    fig = go.Figure(
        data=list(frames[0].data) + [coverage_trace, overlap_trace],
        layout=go.Layout(
            title="Évolution de la position des lampes et des indicateurs",
            shapes=frames[0].layout.shapes,
            xaxis=dict(domain=[0, 0.45], range=[0, SQUARE_SIZE],
                       scaleanchor="y", scaleratio=1, autorange=False),
            yaxis=dict(domain=[0, 1], range=[0, SQUARE_SIZE], autorange=False),
            xaxis2=dict(domain=[0.55, 1], title="Génération"),
            yaxis2=dict(domain=[0, 1], title="Valeur", autorange=True),
            sliders=sliders,
            updatemenus=[dict(type="buttons",
                              buttons=[dict(label="Play",
                                            method="animate",
                                            args=[None, {"frame": {"duration": 300, "redraw": True},
                                                         "fromcurrent": True,
                                                         "transition": {"duration": 0}}])])]
        ),
        frames=frames
    )

    fig.show()


if __name__ == "__main__":
    run_and_animate()
