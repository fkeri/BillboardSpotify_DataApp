import json
import pandas as pd

FILEPATH = "C:\\Users\\fkeri\\portfolio-projects\\BillboardTop100\\data\\external\\1960-2022_yearData.json"
YEAR_START = 1960  # inclusive
YEAR_END = 2022  # inclusive


def get_df_for_year(data, year):
    """
    Returns a DataFrame of weekly billboard top-100 data for a given year.

    Args:
        data (dict): dictionary of billboard top-100 data
        year (str): given year

    Returns:
        DataFrame: weekly billboard top-100 data for a given year
    """
    df = pd.DataFrame()
    for week in range(len(data[str(year)])):
        weeklyDf = pd.DataFrame(data[str(year)][week]["entries"])
        # add the date of the weekly chart to the DataFrame
        weeklyDf["date"] = data[str(year)][week]["date"]
        df = pd.concat([df, weeklyDf.drop(["image", "isNew"], axis=1)], axis=0)
    return df


def get_unique_entries(df):
    """
    Returns a DataFrame of unique (artist, title) combinations that appeared
    on the billboard top-100 data in the years in [1960, 2022]

    Args:
        df (DataFrame): dataframe of billboard top-100 data

    Returns:
        allTimeDf (DataFrame): unique entries of billboard top-100 data
    """
    allTimeDf = pd.DataFrame()
    for year in range(YEAR_START, YEAR_END + 1):
        yearDf = (
            df[str(year)][["artist", "title"]].drop_duplicates().reset_index(drop=True)
        )
        allTimeDf = pd.concat([yearDf, allTimeDf], axis=0)
    allTimeDf = allTimeDf.drop_duplicates().reset_index()
    # NOTE: when trying to count the number of entries for a given artist,
    #       we must also think about if there are featuring artists.
    #       allTimeDf[allTimeDf['artist'] == 'Drake'] vs.
    #       allTimeDf[allTimeDf['artist'].str.contains('Drake')]
    return allTimeDf


def load_billboard_top_100_data(filepath=FILEPATH):
    """
    Load Billboard Top-100 data from JSON file.

    Args:
        filepath (str): path to JSON file containing billboard top-100 data

    Returns:
        df (DataFrame): DataFrame of historical billboard top-100 data
    """
    # Opening JSON file
    f = open(filepath, "r")
    # Returns JSON object as a dictionary
    data = json.load(f)

    # Create a DataFrame consisting of weekly billboard top-100
    # rankings for years in [YEAR_START-YEAR_END]
    df = {}
    for year in range(YEAR_START, YEAR_END + 1):
        df[int(year)] = get_df_for_year(data, year)
    f.close()

    return df
