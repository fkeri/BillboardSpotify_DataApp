from dash import Dash, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from . import ids

AUDIO_FEATURES = {
    "danceability": "Danceability describes how suitable a track is for dancing based on a combination of musical elements, such as tempo, rhythm stability, beat strength, and overall regularity. Its value ranges from 0 (least danceable) to 1 (most danceable).",
    "energy": "Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.",
    # "key": "The key the track is in. Integers map to pitches using standard Pitch Class notation. E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1.",
    "loudness": "The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db.",
    # "mode": "Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.",
    "speechiness": "Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.",
    "acousticness": "Acousticness is a confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.",
    "instrumentalness": "Instrumentalness predicts whether a track contains no vocals. 'Ooh' and 'aah' sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly 'vocal'. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.",
    "liveness": "Liveness detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.",
    "valence": "Valence is a measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).",
    "tempo": "The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.",
    # "duration_min": "The duration of the track in minutes.",
    # "time_signature": "An estimated time signature. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure). The time signature ranges from 3 to 7 indicating time signatures of '3/4', to '7/4'.",
}


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.DENSITY_HEATMAP_RADIO_1_INFO, "children"),
        Input(ids.DENSITY_HEATMAP_RADIO_1, "value"),
    )
    def display_info_for_audio_feature(selected_audio_feature):
        return f"{AUDIO_FEATURES[selected_audio_feature]}"

    @app.callback(
        Output(ids.DENSITY_HEATMAP_RADIO_2_INFO, "children"),
        Input(ids.DENSITY_HEATMAP_RADIO_2, "value"),
    )
    def display_info_for_audio_feature(selected_audio_feature):
        return f"{AUDIO_FEATURES[selected_audio_feature]}"

    return html.Div(
        children=[
            dbc.Row(
                [
                    # Audio Feature 1 - Radio Group Column
                    dbc.Col(
                        html.Div(
                            [
                                html.H5(
                                    "1. Select the first Spotify Audio Feature:",
                                    className="mb-2",
                                ),
                                dbc.RadioItems(
                                    id=ids.DENSITY_HEATMAP_RADIO_1,
                                    options=list(AUDIO_FEATURES.keys()),
                                    value="danceability",
                                    inline=False,
                                    className="btn-group d-flex justify-content-start mb-2",
                                    inputClassName="btn-check",
                                    labelClassName="btn btn-outline-info text-white p-2",
                                    labelCheckedClassName="active",
                                ),
                                dbc.Alert(
                                    id=ids.DENSITY_HEATMAP_RADIO_1_INFO,
                                    color="info",
                                    className="m-auto mb-1",
                                ),
                            ],
                            className="radio-group",
                        ),
                        width=6,
                    ),
                    # Audio Feature 2 - Radio Group Column
                    dbc.Col(
                        html.Div(
                            [
                                html.H5(
                                    "2. Select the second Spotify Audio Feature:",
                                    className="mb-2",
                                ),
                                dbc.RadioItems(
                                    id=ids.DENSITY_HEATMAP_RADIO_2,
                                    options=list(AUDIO_FEATURES.keys()),
                                    value="valence",
                                    inline=False,
                                    className="btn-group d-flex justify-content-start mb-2",
                                    inputClassName="btn-check",
                                    labelClassName="btn btn-outline-info text-white p-2",
                                    labelCheckedClassName="active",
                                ),
                                dbc.Alert(
                                    id=ids.DENSITY_HEATMAP_RADIO_2_INFO,
                                    color="info",
                                    className="m-auto mb-4",
                                ),
                            ],
                            className="radio-group",
                        ),
                        width=6,
                    ),
                ]
            ),
        ],
    )
