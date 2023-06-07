from dash import html, dcc


def render() -> html.Div:
    return html.Div(
        children=[
            html.P(
                "In this section, you may visualize Distributions of Spotify Track Audio Features on Billboard Hot 100 historical data."
            ),
            html.P(
                [
                    "Spotify Track Audio Features are available through ",
                    html.A(
                        "Spotify's Web API",
                        href="https://developer.spotify.com/documentation/web-api/reference/get-several-audio-features",
                        target="_blank",
                        style={"color": "white"},
                    ),
                    """, where Spotify enables us to extract 13 numerical Audio Features for each track. I was curious to examine how each of these Features' distributions
                    changed over time, so I decided to extract Audio Features of tracks that appeared on the Billboard Hot 100 historical data.""",
                ]
            ),
            html.P(
                [
                    "To observe how an Audio Feature's distribution changes over time, you can do the following:",
                    html.Ol(
                        [
                            html.Li(
                                [
                                    html.H6("Select Spotify Audio Feature:"),
                                    html.Ul(
                                        [
                                            html.Li(
                                                "To compare distributions over time, we display ridgeline plots for the selected Audio Feature"
                                            ),
                                            html.Li(
                                                dcc.Markdown(
                                                    children="Exception: Audio Features `mode`, `key`, and `time_signature` are represented using bar plots since they are not continuous numerical variables"
                                                ),
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                            html.Li(
                                [
                                    html.H6("Select Year Range:"),
                                    html.Ul(
                                        [
                                            html.Li(
                                                "The range of Billboard Hot 100 historical data"
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                            html.Li(
                                [
                                    html.H6("Select Data Granularity:"),
                                    html.Ul(
                                        [
                                            html.Li(
                                                "Here you may select how many Billboard years will be included in each distribution"
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                    dcc.Markdown(
                        children="""Example: if we select `danceability` as the Audio Feature to explore, with the `Year Range` of \[1960, 2022\], and the `Data Granularity` of 10 years, we 
                                may observe a ridgeline plot of 7 different distributions. That is, we observe how `danceability` distribution evolved for each decade since the 1960s to the present."""
                    ),
                ]
            ),
        ],
    )
