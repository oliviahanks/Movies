"""
This script helps with the analysis.
"""

import pandas as pd
import matplotlib.pyplot as plt


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


def year_averages_plot(df, group_column, average_column):

    """Graphs the average of numberic columns through the years.

    Args:
      df: The pandas dataframe being used.
      group_column: The name of a column of to group data by, ie year.
      average_column: The name of a column to graph the averages of over the groups.

    Returns:
      None
    """
    plt.plot(df.groupby(df[group_column])[average_column].mean()) 
    plt.xlabel(group_column.capitalize())
    plt.ylabel(average_column.capitalize())
    plt.title(f'Average {average_column.capitalize()} By {group_column.capitalize()}')
    plt.show()