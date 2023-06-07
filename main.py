from dash import Dash
from dash_bootstrap_components.themes import LUX

from src.components.layout import create_layout
import data_utils

import pandas as pd

BILLBOARD_SPOTIFY_FILEPATH = "C:/Users/fkeri/portfolio-projects/BillboardTop100Visualization/data/processed/billboardYearlySpotifyTracksAudioFeatures.json"
ANIMATION_FRAMES_PATH = "C:\\Users\\fkeri\\portfolio-projects\\BillboardTop100\\src\\data\\billboardAnimationFramesDecade.json"
BILLBOARD_HISTORICAL_TOP100_PATH = "C:\\Users\\fkeri\\portfolio-projects\\BillboardTop100\\data\\external\\1960-2022_yearData.json"
YEAR_START = 1960
YEAR_END = 2022


def main() -> None:
    app = Dash(external_stylesheets=[LUX])

    # Load the data
    data = pd.read_json(BILLBOARD_SPOTIFY_FILEPATH)
    # This is a {'year': DataFrame} Dictionary for years in [1960, 2022]
    billboard_charts_df = data_utils.load_billboard_top_100_data(
        BILLBOARD_HISTORICAL_TOP100_PATH
    )

    # Let's concatenate the above Dictionary Dataframes:
    data_billboard_charts = pd.concat(
        [billboard_charts_df[year] for year in range(YEAR_START, YEAR_END + 1)]
    ).reset_index(drop=True)

    data_animation = pd.read_json(ANIMATION_FRAMES_PATH)
    data_animation["duration_ms"] /= 1000 * 60
    data_animation.rename(columns={"duration_ms": "duration_min"}, inplace=True)

    app.title = "Popular Tracks' Audio Feature Exploration:"
    app.subtitle = "Interactive Data App"
    app.card_1 = "Distributions of Audio Features Over Time"
    app.card_2 = "Joint Distributions of Audio Features Over Time"

    app.layout = create_layout(app, data, data_billboard_charts, data_animation)
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
