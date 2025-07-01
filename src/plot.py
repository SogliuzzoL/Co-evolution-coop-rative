import matplotlib.pyplot as plt
from matplotlib.patches import Circle


def plot_group(individuals):
    """
    Affiche un groupe d'individus sous forme de cercles.
    individuals : liste de listes/tuples [x, y, r]
    """
    fig, ax = plt.subplots(figsize=(6, 6))

    for ind in individuals:
        x, y, r = ind
        circle = Circle((x, y), radius=r, alpha=0.2,
                        edgecolor='black', facecolor='blue')
        ax.add_patch(circle)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.set_title("Visualisation d'un groupe d'individus")
    ax.grid(True)
    plt.show()
