from dash import Dash, dcc, html

from . import ids

DECADES = {
    1960: "1960",
    1970: "1970",
    1980: "1980",
    1990: "1990",
    2000: "2000",
    2010: "2010",
    2020: "2020",
}


def render(app: Dash) -> html.Div:
    return html.Div(
        [
            html.H5("2. Select Year Range:", className="mb-2"),
            dcc.RangeSlider(
                1960,
                2022,
                value=[1960, 2022],
                tooltip={"placement": "bottom", "always_visible": True},
                step=1,
                marks=DECADES,
                id=ids.DISTRIBUTIONS_1D_DATE_RANGE,
                className="w-75 m-auto mb-5 p-2",
            ),
        ],
    )
