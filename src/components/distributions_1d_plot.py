import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

import pandas as pd
from ridgeplot import ridgeplot
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import numpy as np

from . import ids

DISCRETE_AUDIO_FEATURES = ["mode", "key", "time_signature"]


def get_year_intervals(year_start, year_end, selected_data_granularity):
    year_intervals = [
        [year, year + selected_data_granularity - 1]
        for year in range(
            year_start,
            year_end + 1 - selected_data_granularity,
            selected_data_granularity,
        )
    ]
    # add the leftover interval if not divisible by years range
    if len(year_intervals) == 0:
        year_intervals = [[year_start, year_end]]
    elif year_intervals[-1][1] < year_end:
        year_intervals.append([year_intervals[-1][1] + 1, year_end])

    # year-labels are either intervals (for data granularity > 1) or individual years
    if selected_data_granularity == 1:
        year_labels = [year_interval[0] for year_interval in year_intervals]
    else:
        year_labels = [
            f"{year_interval[0]}-{year_interval[1]}" for year_interval in year_intervals
        ]

    return year_intervals, year_labels


def get_bar_figure(data, year_intervals, year_labels, selected_audio_feature):
    ROW_COLUMN_DICT = {
        "key": {"ncols": 3},
        "mode": {"ncols": 2},
        "time_signature": {"ncols": 2},
    }

    # transform the dataframe to have correct year labels
    year_labels_data_trans = []
    for i in range(len(year_intervals)):
        year_labels_data_trans.extend(
            [year_labels[i]]
            * len(
                data[
                    (data["year"] >= year_intervals[i][0])
                    & (data["year"] <= year_intervals[i][1])
                ]
            )
        )
    year_labels_data_trans = pd.Series(year_labels_data_trans, name="year")
    data_trans = pd.concat(
        [year_labels_data_trans, data[selected_audio_feature]], axis=1
    )
    if selected_audio_feature == "mode":
        data_trans[selected_audio_feature].replace(1, "major", inplace=True)
        data_trans[selected_audio_feature].replace(0, "minor", inplace=True)

    data_value_counts = pd.DataFrame(data_trans.value_counts()).reset_index()
    data_value_counts.columns = ["year", selected_audio_feature, "percentage"]

    # transform the counts to percentages
    for idx in range(len(data_value_counts)):
        all_count = len(
            data_trans[data_trans["year"] == data_value_counts.at[idx, "year"]]
        )
        data_value_counts.at[idx, "percentage"] /= all_count / 100

    data_value_counts.sort_values(
        by=["year", selected_audio_feature, "percentage"], inplace=True
    )

    n_colors = data_value_counts[selected_audio_feature].nunique()
    color_scale = px.colors.sample_colorscale(
        "Portland", [n / (n_colors - 1) for n in range(n_colors)]
    )

    ROW_COLUMN_DICT[selected_audio_feature]["nrows"] = math.ceil(
        n_colors / ROW_COLUMN_DICT[selected_audio_feature]["ncols"]
    )

    color_dict = dict(
        zip(
            np.array(sorted(data_value_counts[selected_audio_feature].unique())).astype(
                "str"
            ),
            color_scale,
        )
    )

    # Convert the audio_feature column to str, since plotly assumes that all
    # numerical values are continous -> we want to consider them discrete!
    data_value_counts[selected_audio_feature] = data_value_counts[
        selected_audio_feature
    ].astype("str")
    main_fig = px.bar(
        data_value_counts,
        y="percentage",
        x="year",
        orientation="v",
        color=selected_audio_feature,
        color_discrete_map=color_dict,
        barmode="group",
    )

    main_fig.update_layout(
        title=f"Bar Plot of {selected_audio_feature.capitalize()} Ratio over Time",
        title_x=0.5,
        height=600,
        yaxis_title=f"{selected_audio_feature.capitalize()} Percentage",
        xaxis_title=f"Year Interval",
        template="plotly_dark",
        plot_bgcolor="rgb(237, 237, 237)",
        font=dict(
            family="Nunito Sans",
            size=16,
        ),
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, step="year", stepmode="backward"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
        ),
    )

    figs = [main_fig]

    fig_plots = make_subplots(
        rows=ROW_COLUMN_DICT[selected_audio_feature]["nrows"],
        cols=ROW_COLUMN_DICT[selected_audio_feature]["ncols"],
        shared_xaxes=True,
        vertical_spacing=0.02,
        horizontal_spacing=0.05,
    )

    for idx, audio_feature_value in enumerate(
        data_value_counts[selected_audio_feature].unique()
    ):
        curr_fig = go.Scatter(
            x=data_value_counts["year"].unique(),
            y=data_value_counts[
                data_value_counts[selected_audio_feature] == audio_feature_value
            ]["percentage"],
            line=dict(width=4, color=color_dict[audio_feature_value]),
            marker=dict(size=8, line=dict(width=2, color="rgb(17, 17, 17)")),
            name=audio_feature_value,
        )

        fig_plots.add_trace(
            curr_fig,
            row=int(idx / ROW_COLUMN_DICT[selected_audio_feature]["ncols"] + 1),
            col=idx % ROW_COLUMN_DICT[selected_audio_feature]["ncols"] + 1,
        )
        fig_plots.update_yaxes(
            title_text=f"{selected_audio_feature.capitalize()}={audio_feature_value} (%)",
            row=int(idx / ROW_COLUMN_DICT[selected_audio_feature]["ncols"] + 1),
            col=idx % ROW_COLUMN_DICT[selected_audio_feature]["ncols"] + 1,
            title_standoff=0,
        )

    fig_plots.update_layout(
        height=ROW_COLUMN_DICT[selected_audio_feature]["nrows"] * 400,
        title=f"Bar Plot of {selected_audio_feature.capitalize()} Ratio over Time",
        title_x=0.5,
        legend_title_text="key",
        template="plotly_dark",
        # yaxis_title_standoff=0,
        plot_bgcolor="rgb(237, 237, 237)",
        font=dict(
            family="Nunito Sans",
            size=14,
        ),
    )
    fig_plots.update_yaxes(
        range=[
            data_value_counts["percentage"].min() - 0.5,
            data_value_counts["percentage"].max() + 0.5,
        ],
        nticks=10,
    )

    for col_idx in range(1, ROW_COLUMN_DICT[selected_audio_feature]["ncols"] + 1):
        fig_plots.update_xaxes(
            title_text=f"Year Interval",
            row=ROW_COLUMN_DICT[selected_audio_feature]["nrows"],
            col=col_idx,
        )

    figs.append(fig_plots)
    return figs


def get_ridgeplot_figure(data, year_intervals, year_labels, selected_audio_feature):
    # The ridgeplot function requires the following transformation:
    audio_feature_dist = [
        data[(data["year"] >= year_interval[0]) & (data["year"] <= year_interval[1])][
            [selected_audio_feature]
        ].to_numpy()
        for year_interval in year_intervals
    ]

    # if there is only one distribution to plot, we can't use ridgeplot
    if len(audio_feature_dist) > 1:
        fig = ridgeplot(
            samples=audio_feature_dist,
            colorscale="viridis",
            colormode="index",
            coloralpha=0.6,
            labels=year_labels,
            spacing=1 / 3,
        )
    else:
        print("I'm here")
        fig = ff.create_distplot(
            [[val[0] for val in audio_feature_dist[0]]], year_labels
        )

    # Again, update the figure layout to your liking here
    fig.update_layout(
        title=f"Ridgeline Density Plot of {selected_audio_feature.capitalize()} Distributions over Time",
        title_x=0.5,
        height=max(400, 150 * (len(audio_feature_dist) + 1)),
        # plot_bgcolor="rgb(255, 255, 255)",
        yaxis_title=f"Density Plot's Year Interval",
        xaxis_title=f"{selected_audio_feature.capitalize()}",
        template="plotly_dark",
        font=dict(
            family="Nunito Sans",
            size=16,
        ),
    )

    return fig


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.DISTRIBUTIONS_1D_PLOT, "children"),
        [
            Input(ids.DISTRIBUTIONS_1D_RADIO, "value"),
            Input(ids.DISTRIBUTIONS_1D_DATE_RANGE, "value"),
            Input(ids.DISTRIBUTIONS_1D_DATA_GRANULARITY, "value"),
        ],
    )
    def update_audio_feature_analysis_figure(
        selected_audio_feature, selected_date_range, selected_data_granularity
    ):
        selected_data_granularity = int(selected_data_granularity)
        year_start = selected_date_range[0]
        year_end = selected_date_range[1]

        # Given year_start, year_end, and selected_data_granularity:
        #   -> generate year intervals and their labels
        year_intervals, year_labels = get_year_intervals(
            year_start, year_end, selected_data_granularity
        )

        # We'll generate different plot types:
        #   1. Bar plot -> for discrete audio features
        #   2. Ridgeplot -> for continuous audio features
        if selected_audio_feature in DISCRETE_AUDIO_FEATURES:
            fig = get_bar_figure(
                data, year_intervals, year_labels, selected_audio_feature
            )
        else:
            fig = get_ridgeplot_figure(
                data, year_intervals, year_labels, selected_audio_feature
            )

        if selected_audio_feature in DISCRETE_AUDIO_FEATURES:
            return html.Div(
                [
                    html.Div(
                        dcc.Graph(figure=fig[0], style={"margin": "auto"}),
                        id="graph_0",
                        className="mt-3",
                    ),
                    html.Div(
                        dcc.Graph(figure=fig[1], style={"margin": "auto"}),
                        id="graph_1",
                        className="mt-3",
                    ),
                ],
                id=ids.DISTRIBUTIONS_1D_PLOT,
                className="mt-3",
            )
        else:
            return html.Div(
                dcc.Graph(figure=fig, style={"margin": "auto"}),
                id="graph_0",
                className="mt-3",
            )

    return html.Div(id=ids.DISTRIBUTIONS_1D_PLOT)
