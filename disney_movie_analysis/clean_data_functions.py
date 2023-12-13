"""
This script takes the raw data and does the data cleaning and organizing.
"""

import pandas as pd
import re
import math
import numpy as np


# Clean Rotten Tomatoes

def clean_rotten_tomatoes(rotten_tomatoes):
    """ Cleans dataframe that was scraped from Rotten Tomatoes using our scrape_rotten_tomatoes function.

    Args:
      rotten_tomatoes: Raw Rotten Tomatoes pandas dataframe.

    Returns:
      A cleaned Rotten Tomatoes dataframe.
    """
    # Remove everything other than the title from the title column
    rotten_tomatoes['title'] = rotten_tomatoes['title'].str.replace('[\n]','', regex=True).str.replace('[(][^)]+[)]','', regex=True).str.replace('\d+[%]','', regex=True)
    rotten_tomatoes['title'] = rotten_tomatoes.title.str.strip()

    # Remove 'Starring: ' from actor column and 'Directed By: ' from directors column
    rotten_tomatoes['actors'] = rotten_tomatoes.actors.str.replace('[\n](Starring: )', '', regex = True)
    rotten_tomatoes['director'] = rotten_tomatoes.director.str.replace('[\n](Directed By: )', '', regex = True)

    # Make actors and directors columns into columns of lists
    rotten_tomatoes['actors'] = rotten_tomatoes['actors'].str.split(',')
    rotten_tomatoes['director'] = rotten_tomatoes['director'].str.split(',')

    # Format years in year column as integers
    rotten_tomatoes['year'] = rotten_tomatoes.year.apply(lambda x: re.findall('\d+', str(x))[0])
    rotten_tomatoes['year'] = rotten_tomatoes.year.astype(int)

    # Make a column with the score out of ten to compare with IMDB scores
    rotten_tomatoes['comparison_score'] = rotten_tomatoes.score.apply(lambda x: int(re.findall('\d+', x)[0])/10)

    # Return cleaned dataframe
    return rotten_tomatoes



# Clean IMDB


def clean_imdb(imdb):
    """ Cleans dataframe that was scraped from IMDB using our scrape_imdb function.

    Args:
      imdb: Raw IMDB pandas dataframe.

    Returns:
      A cleaned IMDB dataframe.
    """
    # Format year, runtime, and gross to be able to convert them into integers, and convert score to float
    imdb['year'] = imdb['year'].apply(lambda x: re.findall('\d+', str(x))[0]).astype(int)
    imdb['runtime'] = imdb['runtime'].apply(lambda x: int(re.findall('\d+', str(x))[0]) if re.findall('\d+', str(x)) else np.nan)
    imdb['gross'] = pd.to_numeric(imdb['gross'].str.replace('[,]','', regex=True), errors='coerce').astype('Int64')
    imdb['gross'] = imdb['gross'].astype(int)
    imdb['score'] = imdb['score'].astype(float)

    # Remove everything other than the title
    imdb['title'] = imdb['title'].str.replace('[\n][^\n]+[\n]','', regex=True)
    imdb['title'] = imdb.title.str.strip()

    # Convert the genre column to a column of lists
    imdb['genre'] = imdb['genre'].str.replace('[\n]','', regex=True).apply(lambda x: x.strip())
    imdb['genre'] = imdb['genre'].apply(lambda x: x.replace(', ', ',')).str.split(',')

    # Separate uncleaned director column into director and actors columns
    imdb[['director', 'actors']] = imdb['director'].str.replace('[\n]','', regex=True).apply(lambda x: str(x).replace(', ', ',')).apply(lambda x: x.strip()).str.split('|', expand = True)

    # Remove everything but actor names and convert into a column of lists
    imdb['actors'] = imdb['actors'].str.replace('\s*Stars:\s*', '', regex = True).str.replace('\s*Star:\s*', '', regex = True)
    imdb['actors'] = imdb['actors'].str.split(',')

    # Remove everything but director names and convert into a column of lists
    imdb['director'] = imdb['director'].str.replace('Directors:', '', regex = True).str.replace('Director:', '', regex = True)
    imdb['director'] = imdb['director'].str.split(',')

    # From the year column create a column of decades
    imdb['decade'] = imdb['year'].apply(lambda x: math.floor(x/10)*10)

    # Return cleaned dataframe
    return imdb




# Clean Disney Fandom Data

def clean_fandom(fandom):
    """ Cleans dataframe that was scraped from Disney Fandom using our scrape_fandom function.

    Args:
      imdb: Raw Fandom pandas dataframe.

    Returns:
      A cleaned Disney Fandom dataframe.
    """

    fandom['year'] = fandom['year'].astype(str).str.findall('\((\d{4})').apply(lambda x: ''.join(x))
    fandom['title'] = fandom['title'].str.findall('(^.*?)\s(?=\()').apply(lambda x: ''.join(x))

    return fandom
