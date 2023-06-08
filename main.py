from dash import Dash
from dash_bootstrap_components.themes import LUX

from src.components.layout import create_layout

import pandas as pd
import json
import os

processed_dir = "data/processed"
external_dir = "data/external"

BILLBOARD_SPOTIFY_FILEPATH = os.path.join(
    processed_dir, "billboardYearlySpotifyTracksAudioFeatures.json"
)
BILLBOARD_HISTORICAL_1960_1990_PATH = os.path.join(
    external_dir, "1960-1990_yearData.json"
)
BILLBOARD_HISTORICAL_1991_2022_PATH = os.path.join(
    external_dir, "1991-2022_yearData.json"
)
YEAR_START = 1960
YEAR_END = 2022


def load_billboard_hot_100_data(filepath_1, filepath_2):
    with open(filepath_1, "r") as json_file:
        file_1 = json.load(json_file)
        file_1 = pd.DataFrame(file_1)
    with open(filepath_2, "r") as json_file:
        file_2 = json.load(json_file)
        file_2 = pd.DataFrame(file_2)
    return pd.concat([file_1, file_2]).reset_index(drop=True)


app = Dash(external_stylesheets=[LUX])
server = app.server

# Load Billboard-Spotify Data
with open(BILLBOARD_SPOTIFY_FILEPATH, "r") as json_file:
    json_data = json.load(json_file)
data = pd.DataFrame(json_data)

# Load weekly raw Billboard Chart Data
data_billboard_charts = load_billboard_hot_100_data(
    BILLBOARD_HISTORICAL_1960_1990_PATH, BILLBOARD_HISTORICAL_1991_2022_PATH
)

app.title = "Popular Tracks' Audio Feature Exploration:"
app.subtitle = "Interactive Data App"
app.card_1 = "Distributions of Audio Features Over Time"

app.layout = create_layout(app, data, data_billboard_charts)
app.run_server(debug=False)
