from nsga2_config import run_nsga2
from animation import create_animation, generations
from parameters import group_min, group_max


def main():
    # Lancer l’optimisation NSGA-II
    pareto_front = run_nsga2()

    # Générer l’animation à partir des données collectées
    create_animation(generations, group_min, group_max)


if __name__ == "__main__":
    main()
