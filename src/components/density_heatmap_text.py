from dash import html


def render() -> html.Div:
    return html.Div(
        children=[
            html.P(
                """In this section, to visualize the joint distribution of two Spotify Track Audio Features over time, 
                we generate an animated 2D Histogram Contour Plot (Density Heatmap)."""
            ),
            html.P(
                """To generate the Density Heatmap, first select two Spotify Track Audio Features. 
                The two selected Audio Features' values are divided into bins, and we count the number of observations (tracks) in each bin. 
                The resulting bin counts are then plotted as a heatmap, where the color intensity represents the number of observations in each bin. 
                Moreover, the plot also includes contour lines that connect points of equal counts to visualize the shape of the joint distribution."""
            ),
            html.P(
                """The joint distribution of two Spotify Track Audio Features includes 10 years of Billboard Top-100 song data. 
                However, we can press PLAY to animate how the joint distribution changes over time, or use the slider to move to a specific year.
                For instance, in the first animation frame, the joint distribution includes data in the [1960, 1970] year-range. The next frame will
                also include 10 years of data, but this time in the [1961, 1971] year-range. We continue to visualize 10-year joint distributions until the
                [2012, 2022] year-range."""
            ),
        ],
    )
