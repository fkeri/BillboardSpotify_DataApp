from dash import Dash, html
import pandas as pd

from . import (
    distributions_1d_text,
    distributions_1d_radio,
    distributions_1d_date_range,
    distributions_1d_plot,
    distributions_1d_data_granularity,
)


def create_layout(
    app: Dash,
    data: pd.DataFrame,
) -> html.Div:
    return html.Div(
        className="app-div bg-light",
        children=[
            html.H1(
                app.title,
                className="text-center text-weight-bold",
            ),
            html.H2(
                app.subtitle,
                className="text-center text-weight-bold",
            ),
            html.Hr(),
            # Spotify Audio Feature Visualization - Distributions Over Time
            html.Div(
                [
                    html.H2(
                        app.card_1,
                        className="card-header text-left align-vertical border-custom-light-gray",
                    ),
                    html.Div(
                        className="card-body text-justify m-auto",
                        children=[distributions_1d_text.render()],
                    ),
                    html.Div(
                        className="card-body",
                        children=[
                            distributions_1d_radio.render(app),
                            distributions_1d_date_range.render(app),
                            distributions_1d_data_granularity.render(app),
                            distributions_1d_plot.render(app, data),
                        ],
                    ),
                ],
                className="card text-white bg-plotly-dark mb-3 border-custom-light-gray m-auto",
                style={"width": "85vw"},
            ),
        ],
    )
