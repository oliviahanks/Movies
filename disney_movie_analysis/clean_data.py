"""
This script takes the raw data and does the data cleaning and organizing.
"""

import pandas as pd
import re
import math


# Clean Rotten Tomatoes

def clean_rotten_tomatoes(rotten_tomatoes):
    """ Cleans dataframe that was scraped from Rotten Tomatoes using our scrape_rotten_tomatoes function.

    Args:
      rotten_tomatoes: Raw Rotten Tomatoes pandas dataframe.

    Returns:
      A cleaned Rotten Tomatoes dataframe.
    """

    rotten_tomatoes['title'] = rotten_tomatoes['title'].str.replace('[\n]','', regex=True).str.replace('[(][^)]+[)]','', regex=True).str.replace('\d+[%]','', regex=True)

    rotten_tomatoes['actors'] = rotten_tomatoes.actors.str.replace('[\n](Starring: )', '', regex = True)
    rotten_tomatoes['director'] = rotten_tomatoes.director.str.replace('[\n](Directed By: )', '', regex = True)

    rotten_tomatoes['actors'] = rotten_tomatoes['actors'].str.split(',')
    rotten_tomatoes['director'] = rotten_tomatoes['director'].str.split(',')

    rotten_tomatoes['year'] = rotten_tomatoes.year.apply(lambda x: re.findall('\d+', str(x))[0])
    rotten_tomatoes['comparison_score'] = rotten_tomatoes.score.apply(lambda x: int(re.findall('\d+', x)[0])/10)

    rotten_tomatoes['year'] = rotten_tomatoes.year.astype(int)
    rotten_tomatoes['title'] = rotten_tomatoes.title.str.strip()

    return rotten_tomatoes



# Clean IMDB


def clean_imdb(imdb):
    """ Cleans dataframe that was scraped from IMDB using our scrape_imdb function.

    Args:
      imdb: Raw IMDB pandas dataframe.

    Returns:
      A cleaned IMDB dataframe.
    """

    imdb['year'] = imdb['year'].apply(lambda x: re.findall('\d+', str(x))[0]).astype(int)
    imdb['runtime'] = imdb['runtime'].apply(lambda x: re.findall('\d+', str(x))[0]).astype(int)
    imdb['gross'] = imdb['gross'].str.replace('[,]','', regex=True).astype(int)

    imdb['score'] = imdb['score'].astype(float)

    imdb['title'] = imdb['title'].str.replace('[\n][^\n]+[\n]','', regex=True)
    imdb['title'] = imdb.title.str.strip()

    imdb['genre'] = imdb['genre'].str.replace('[\n]','', regex=True).apply(lambda x: x.strip())
    imdb['genre'] = imdb['genre'].apply(lambda x: x.replace(', ', ','))


    imdb[['director', 'actors']] = imdb['director'].str.replace('[\n]','', regex=True).apply(lambda x: str(x).replace(', ', ',')).apply(lambda x: x.strip()).str.split('|', expand = True)

    imdb['actors'] = imdb.actors.str.replace('\s*Stars:\s*', '', regex = True).str.replace('\s*Star:\s*', '', regex = True)
    imdb['actors'] = imdb['actors'].str.split(',')

    imdb['director'] = imdb.director.str.replace('Directors:', '', regex = True).str.replace('Director:', '', regex = True)
    imdb['director'] = imdb['director'].str.split(',')

    imdb['decade'] = imdb.year.apply(lambda x: math.floor(x/10)*10)

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

