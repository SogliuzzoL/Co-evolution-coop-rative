from nsga2_config import run_nsga2
from animation import create_animation, generations


def main():
    # Lancer l’optimisation NSGA-II
    pareto_front = run_nsga2()

    # Générer l’animation à partir des données collectées
    create_animation(generations)


if __name__ == "__main__":
    main()
