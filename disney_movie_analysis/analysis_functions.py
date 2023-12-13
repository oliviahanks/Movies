"""
This script helps with the analysis.
"""

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


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
        ratings = dataframe[list_column.apply(lambda x: value in x if x is not None else False)].loc[:, summary_column.name].dropna()
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


def top_list_vals(column, n):

  """Graphs the average of numberic columns through the years.

  Args:
    column: A column of lists in a pandas dataframe in the form df['col_name']
    n: The number of top values to return

  Returns:
    A pandas dataframe containing counts of the frequency of the top n values in the list column.
  """
  # Count occurrences of each item in the list column
  item_count = column.apply(lambda x: Counter(x))

  # Sum the counts and find the top n most common values
  top_vals = pd.DataFrame(sum(item_count, Counter()).most_common(n))

  return top_vals