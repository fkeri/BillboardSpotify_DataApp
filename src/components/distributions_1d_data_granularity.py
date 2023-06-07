from dash import Dash, html
import dash_bootstrap_components as dbc

from . import ids

DATA_GRANULARITY = {
    "1": "1 year",
    "2": "2 years",
    "5": "5 years",
    "10": "10 years",
    "20": "20 years",
}


def render(app: Dash) -> html.Div:
    return html.Div(
        children=[
            html.H5(
                "3. Select Data Granularity (aggregate songs every X years):",
                className="mb-2",
            ),
            html.Div(
                [
                    dbc.RadioItems(
                        id=ids.DISTRIBUTIONS_1D_DATA_GRANULARITY,
                        options=DATA_GRANULARITY,
                        value="10",
                        inline=False,
                        className="btn-group d-flex justify-content-center mb-2",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-info text-white p-2",
                        labelCheckedClassName="active",
                    ),
                ],
                className="radio-group",
            ),
        ],
        className="radio-group",
    )
