import pandas as pd

imdb = pd.read_csv('disney_movie_analysis/data/imdb.csv')
rotten_tomatoes = pd.read_csv('disney_movie_analysis/data/rotten_tomatoes.csv')


def list_averages(dataframe, list_column, summary_column):

    """Takes the averages for each value in a column of lists.

    Args:
      dataframe: The pandas dataframe being used.
      list_column: The column of lists to apply the function on, in the form df[column]
      summary_column: The column to take the averages over, in the form df[column]

    Returns:
      A pandas dataframe containing the averages for each of the list values.
    """

    values = list(filter(None, list(list_column.explode().unique())))

    val_averages = {}

    for value in values:
        ratings = dataframe[list_column.apply(lambda x: value in x)].loc[:, summary_column.name].dropna()
        avg_rating = ratings.mean()
        val_averages[value] = avg_rating.round(4)

    val_averages = pd.DataFrame(val_averages.items())

    return val_averages

if __name__ == '__main__':
    # Merge Datasets
    merged = rotten_tomatoes.merge(imdb, how= 'inner', on = ['title', 'year'])
    merged.to_csv('disney_movie_analysis/data/merged.csv', index = False)
