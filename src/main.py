from individu import Lampe
from model import random_generator, generator, evaluator

import inspyred
import numpy as np
import matplotlib.pyplot as plt

nsga2 = inspyred.ec.emo.NSGA2(random=random_generator())
nsga2.terminator = inspyred.ec.terminators.evaluation_termination
nsga2.variator = []

pareto_front = nsga2.evolve(
    generator = generator,
    evaluator=evaluator,

    # args
    population_size = 100,
    group_min = 1,
    group_max = 10,
    radius = 0.2,
    fitness_lamp = {}
)
