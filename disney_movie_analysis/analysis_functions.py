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
      list_column: The column of lists to apply the function on
      summary_column: The column to take the averages over

    Returns:
      A pandas dataframe containing the averages for each of the list values.
    """
    # Explode lists in the rows of the column to find all the values included in each list
    values = list(filter(None, list(dataframe[list_column].explode().unique())))

    # Initialize a dictionary to store averages
    val_averages = {}

    # Iterate through each value and take the average for that value
    for value in values:
      # Filter rows where the value is included in the list
        ratings = dataframe[dataframe[list_column].apply(lambda x: value in x if x is not None else False)].loc[:, summary_column].dropna()
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
    # Plot average of column over over another variable
    plt.plot(df.groupby(df[group_column])[average_column].mean()) 
    plt.xlabel(group_column.capitalize())
    plt.ylabel(average_column.capitalize())
    plt.title(f'Average {average_column.capitalize()} By {group_column.capitalize()}')

    # Show average plot
    plt.show()


def top_list_vals(column, n):

  """From a list column, returns counts of the frequency of each list value.

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

  # Return Dataframe
  return top_vals



def merge_imdb_rt(imdb, rotten_tomatoes):
    """Merge cleaned IMDB and Rotten Tomatoes datasets.

    Args:
      imdb: A cleaned IMDB pandas dataframe.
      rotten_tomatoes: A cleaned Rotten Tomatoes dataframe.

    Returns:
      A pandas dataframe of the merged IMDB and Rotten Tomatoes dataframes.
    """

    merged = rotten_tomatoes.drop(['director', 'actors'], axis = 1).merge(imdb, how= 'inner', on = ['title', 'year'])
    merged = merged.rename(columns={'score_y': 'imdb_score', 'comparison_score': 'rotten_tomatoes_score'})

    return merged