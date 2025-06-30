from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Liste globale pour stocker les générations
generations = []


def create_animation(generations, group_min, group_max):
    fig = make_subplots(rows=1, cols=3, subplot_titles=[
        "Surface vs Nb Lampes",
        "Overlapping vs Nb Lampes",
        "Surface vs Overlapping"
    ])

    frames = []

    for gen, data in generations:
        nb_lampes = [d[0] for d in data]
        surface = [d[1] for d in data]
        overlapping = [d[2] for d in data]

        frame = go.Frame(
            data=[
                go.Scatter(x=nb_lampes, y=surface, mode='markers',
                           marker=dict(color='blue')),
                go.Scatter(x=nb_lampes, y=overlapping,
                           mode='markers', marker=dict(color='green')),
                go.Scatter(x=overlapping, y=surface, mode='markers',
                           marker=dict(color='red')),
            ],
            name=f"Gen {gen}"
        )
        frames.append(frame)

    # Ajout des traces initiales vides
    fig.add_trace(go.Scatter(x=[], y=[], mode='markers',
                  marker=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=[], y=[], mode='markers',
                  marker=dict(color='green')), row=1, col=2)
    fig.add_trace(go.Scatter(x=[], y=[], mode='markers',
                  marker=dict(color='red')), row=1, col=3)

    fig.update_layout(
        title="Évolution de la population par génération",
        xaxis=dict(title="Nb Lampes", range=[group_min - 1, group_max + 1]),
        yaxis=dict(title="Surface", range=[-0.1, 1.1]),
        xaxis2=dict(title="Nb Lampes", range=[group_min - 1, group_max + 1]),
        yaxis2=dict(title="Overlapping", range=[-0.1, 1.1]),
        xaxis3=dict(title="Overlapping", range=[-0.1, 1.1]),
        yaxis3=dict(title="Surface", range=[-0.1, 1.1]),
        updatemenus=[{
            "type": "buttons",
            "buttons": [
                {"label": "Play", "method": "animate", "args": [
                    None, {"frame": {"duration": 500, "redraw": True}}]},
                {"label": "Pause", "method": "animate", "args": [[None], {
                    "mode": "immediate", "frame": {"duration": 0}, "transition": {"duration": 0}}]}
            ]
        }],
        sliders=[{
            "steps": [
                {
                    "method": "animate",
                    "args": [[f.name], {"mode": "immediate", "frame": {"duration": 0}, "transition": {"duration": 0}}],
                    "label": f.name
                } for f in frames
            ]
        }]
    )

    fig.frames = frames
    fig.write_html("animation.html", auto_open=False)
