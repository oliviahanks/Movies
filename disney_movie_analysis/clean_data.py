"""
This script imports the raw data, cleans it, and exports the final dataset.
"""
if __name__ == '__main__' :

  import pandas as pd
  import re
  import math
  import numpy as np
  from clean_data_functions import clean_imdb, clean_rotten_tomatoes, clean_fandom

  # Clean Rotten Tomatoes Dataframe

  rotten_tomatoes = pd.read_csv('data/rotten_tomatoes_raw.csv')
  rotten_tomatoes = clean_rotten_tomatoes(rotten_tomatoes)
  rotten_tomatoes.to_csv('data/rotten_tomatoes.csv', index = False)

  # Clean IMDB Dataframe

  imdb = pd.read_csv('data/imdb_raw.csv')
  imdb = clean_imdb(imdb)
  imdb.to_csv('data/imdb.csv', index = False)

  # Clean Disney Fandom Dataframe

  fandom = pd.read_csv('data/disney_fandom_raw.csv')
  fandom = clean_fandom(fandom)
  fandom.to_csv('data/disney_fandom.csv', index = False)
