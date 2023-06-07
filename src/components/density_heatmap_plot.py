import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

import pandas as pd

from . import ids

WINDOW_STEP = 52  # window step is 52 weeks


def get_billboard_density_heatmap(
    audio_feature_1: str,
    audio_feature_2: str,
    data_animation: pd.DataFrame,
    data_billboard_charts: pd.DataFrame,
):
    animation_frames_df = (
        data_animation[["artist", "title", audio_feature_1, audio_feature_2, "frame"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    n_frames = int(animation_frames_df[["frame"]].max())
    unique_dates = data_billboard_charts["date"].unique()
    plot_colorscale = px.colors.make_colorscale(
        ["#111111"] + px.colors.sequential.Agsunset
    )

    audio_feature_1_scale = {
        "min": animation_frames_df[audio_feature_1].min(),
        "max": animation_frames_df[audio_feature_1].max(),
    }
    audio_feature_2_scale = {
        "min": animation_frames_df[audio_feature_2].min(),
        "max": animation_frames_df[audio_feature_2].max(),
    }

    # Outline definition of the animation plot (frame=0)
    fig = go.Figure(
        go.Histogram2dContour(
            x=animation_frames_df[animation_frames_df["frame"] == 0][[audio_feature_1]]
            .to_numpy()
            .T[0],
            y=animation_frames_df[animation_frames_df["frame"] == 0][[audio_feature_2]]
            .to_numpy()
            .T[0],
            colorscale=plot_colorscale,
            hovertemplate=audio_feature_1
            + ": %{x:.2f}<br>"
            + audio_feature_2
            + ": %{y:.2f}<br>"
            + "count: %{z}<extra></extra>",
        )
    )

    # Define all the animation frames
    frames = []
    for i in range(0, n_frames + 1, WINDOW_STEP):
        frames.append(
            go.Frame(
                data=[
                    go.Histogram2dContour(
                        x=animation_frames_df[animation_frames_df["frame"] == i][
                            [audio_feature_1]
                        ]
                        .to_numpy()
                        .T[0],
                        y=animation_frames_df[animation_frames_df["frame"] == i][
                            [audio_feature_2]
                        ]
                        .to_numpy()
                        .T[0],
                        colorscale=plot_colorscale,
                    )
                ],
                layout=go.Layout(
                    title_text=f"Date Range: from {unique_dates[i]} to {unique_dates[i+WINDOW_STEP*10]}",
                ),
                name=f"Frame: {i}",
            )
        )
    fig.frames = frames

    # Define buttons for the animation plot
    updatemenus = [
        dict(
            type="buttons",
            showactive=False,
            direction="left",
            pad={"r": 20, "t": 77},
            x=0.1,
            xanchor="right",
            y=0,
            yanchor="top",
            buttons=[
                dict(
                    label="PLAY",
                    method="animate",
                    args=[
                        None,
                        {
                            "frame": {"duration": 200, "redraw": True},
                            "fromcurrent": True,
                        },
                    ],
                ),
                dict(
                    args=[
                        [None],
                        {
                            "frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0},
                        },
                    ],
                    label="PAUSE",
                    method="animate",
                ),
            ],
        )
    ]

    # Define the slider for the animation plot
    sliders = [
        dict(
            steps=[
                dict(
                    method="animate",
                    args=[
                        [f"Frame: {i}"],
                        dict(
                            mode="immediate",
                            frame=dict(duration=400, redraw=True),
                            transition=dict(duration=0),
                        ),
                    ],
                    label=f"{str(unique_dates[i]).split('-')[0]}",
                )
                for i in range(0, n_frames + 1, WINDOW_STEP)
            ],
            active=0,
            transition={"duration": 300, "easing": "cubic-in-out"},
            x=0.1,  # slider starting position
            y=0,
            xanchor="left",
            yanchor="top",
            pad={"b": 10, "t": 50},
            len=0.9,
        )
    ]

    # Finishing touches on the animation plot layout
    fig.update_layout(
        title=f"Date Range: from {unique_dates[0]} to {unique_dates[WINDOW_STEP*10]}",
        template="plotly_dark",
        height=800,
        xaxis=dict(
            range=[
                audio_feature_1_scale["min"],
                audio_feature_1_scale["max"],
            ],
            autorange=False,
            zeroline=False,
            showgrid=False,
            title=audio_feature_1,
        ),
        yaxis=dict(
            range=[
                audio_feature_2_scale["min"],
                audio_feature_2_scale["max"],
            ],
            autorange=False,
            zeroline=False,
            showgrid=False,
            title=audio_feature_2,
        ),
        updatemenus=updatemenus,
        sliders=sliders,
        plot_bgcolor="#111111",
        font=dict(
            family="Nunito Sans",
            size=16,
        ),
    )

    return fig


def render(
    app: Dash, data_billboard_charts: pd.DataFrame, data_animation: pd.DataFrame
) -> html.Div:
    @app.callback(
        Output(ids.DENSITY_HEATMAP_PLOT, "children"),
        [
            Input(ids.DENSITY_HEATMAP_RADIO_1, "value"),
            Input(ids.DENSITY_HEATMAP_RADIO_2, "value"),
        ],
    )
    def update_audio_feature_analysis_figure(
        selected_audio_feature_1, selected_audio_feature_2
    ):
        animated_fig = get_billboard_density_heatmap(
            selected_audio_feature_1,
            selected_audio_feature_2,
            data_animation,
            data_billboard_charts,
        )
        return html.Div(
            dcc.Graph(figure=animated_fig, style={"margin": "auto"}),
            id="graph_0",
            className="mt-2",
        )

    return html.Div(id=ids.DENSITY_HEATMAP_PLOT)
