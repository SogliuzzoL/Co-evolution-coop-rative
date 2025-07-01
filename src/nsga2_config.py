import inspyred
from model import random_generator, generator, evaluator, mutation, crossover
from animation import generations
from parameters import group_min, group_max, radius, mu, sigma, tau, pm, pop_size, nb_group, max_evaluations
from datetime import datetime


def animated_observer(population, num_generations, num_evaluations, args):
    snapshot = [(-ind.fitness[0], ind.fitness[1])
                for ind in population]
    candidates = [ind.candidate for ind in population]
    generations.append((num_generations, snapshot, candidates))
    print(
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
        f"Génération {num_generations} | "
        f"Évaluations: {num_evaluations} | "
        f"Population: {len(population)}"
    )


def run_nsga2():
    nsga2 = inspyred.ec.emo.NSGA2(random=random_generator())
    nsga2.terminator = inspyred.ec.terminators.evaluation_termination
    nsga2.variator = [inspyred.ec.variators.gaussian_mutation,
                      inspyred.ec.variators.blend_crossover]
    # nsga2.variator = [mutation, crossover]
    nsga2.observer = animated_observer

    pareto_front = nsga2.evolve(
        generator=generator,
        evaluator=evaluator,
        pop_size=pop_size,
        max_evaluations=max_evaluations,
        maximize=False,
        bounder=inspyred.ec.Bounder(0, 1),
        group_min=group_min,
        group_max=group_max,
        radius=radius,
        mu=mu,
        sigma=sigma,
        tau=tau,
        pm=pm,
        fitness_cache={},
        nb_group=nb_group,
    )
    return pareto_front
