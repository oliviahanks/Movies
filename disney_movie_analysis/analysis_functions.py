"""
This script helps with the analysis.
"""

import pandas as pd


def list_averages(dataframe, list_column, summary_column):

    """Takes the averages for each value in a column of lists.

    Args:
      dataframe: The pandas dataframe being used.
      list_column: The column of lists to apply the function on, in the form df[column]
      summary_column: The column to take the averages over, in the form df[column]

    Returns:
      A pandas dataframe containing the averages for each of the list values.
    """
    # Explode lists in the rows of the column to find all the values included in each list
    values = list(filter(None, list(list_column.explode().unique())))

    # Initialize a dictionary to store averages
    val_averages = {}

    # Iterate through each value and take the average for that value
    for value in values:
      # Filter rows where the value is included in the list
        ratings = dataframe[list_column.apply(lambda x: value in x)].loc[:, summary_column.name].dropna()
        avg_rating = ratings.mean()
        val_averages[value] = avg_rating.round(4)

    # Convert dictionary to pandas dataframe
    val_averages = pd.DataFrame(val_averages.items())

    # Return dataframe
    return val_averages

