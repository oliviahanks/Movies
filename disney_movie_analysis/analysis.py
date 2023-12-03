import pandas as pd


def list_averages(dataframe, list_column, summary_column):
    values = list(filter(None, list(list_column.explode().unique())))

    val_averages = {}

    for value in values:
        ratings = dataframe[list_column.apply(lambda x: value in x)].loc[:, summary_column.name].dropna()
        avg_rating = ratings.mean()
        val_averages[value] = avg_rating.round(4)

    val_averages = pd.DataFrame(val_averages.items())

    return val_averages