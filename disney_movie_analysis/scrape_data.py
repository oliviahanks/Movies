"""
This script performs the webscraping and produces the raw dataset to be cleaned.
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_html_text(bs, name, attrs):
    """ A function to get certain text from scraped webpage without causing an error if it does not exist.

    Args:
      bs: A beautiful_soup object.
      name: The name of the html class.
      attrs: The attributes in the class that we are looking for.

    Returns:
      The text following the class and attribute if it exists, otherwise an NA.
    """
    # Check if an element is in beautiful soup, if it is get the text from it, if not set text = NA
    try:
        element = bs.find(name, attrs)
        text = element.text if element else "NA"
    except:
        text = "NA"
    return text


# Read in Rotten Tomatoes Data

def scrape_rotten_tomatoes(webpage):
    """ Scrapes data from Rotten Tomatoes webpage.

    Args:
      webpage: A Rotten Tomatoes webpage link to get the data from.

    Returns:
      A raw, uncleaned Rotten Tomatoes dataframe.
    """
    # Send a request to a given url
    r = requests.get(webpage) 

    # Create a beautiful soup object
    soup = BeautifulSoup(r.text, features="lxml")

    # Initialize a dictionary to hold information
    movies = {'title':[], 'year':[], 'score':[], 'actors':[], 'director':[]} 

    # Find all movie data occurences
    occurences = soup.find_all("div", {"class": "row countdown-item"})

    # Iterate through each occurence, extracting relevant information and storing it in the dictionary
    for occurence in occurences:
        movies['title'].append(occurence.find('div', {'class': 'article_movie_title'}).text)
        movies['year'].append(occurence.find('span', {'class:', 'subtle start-year'}).text) 
        movies['score'].append(occurence.find('span', {'class': 'tMeterScore'}).text)
        movies['actors'].append(get_html_text(occurence, 'div', {'class': 'info cast'}))
        movies['director'].append(get_html_text(occurence, 'div', {'class': 'info director'}))

    # Return a pandas dataframe created from the dictionary
    return pd.DataFrame(movies)




# Read In IMDB Data

def scrape_imdb(webpage):
    """ Scrapes data from IMDB webpage.

    Args:
      webpage: An IMDB webpage link to get the data from.

    Returns:
      A raw, uncleaned IMDB dataframe.
    """
    # Send a request to a given url
    r = requests.get(webpage)

    # Create a beautiful soup object
    soup = BeautifulSoup(r.text, features="lxml")

    # Initialize a dictionary to hold information
    movies = {'title':[], 'year':[], 'score':[], 'runtime':[], 'rating':[], 'genre':[], 'gross':[], 'director': []}

    # Find all movie data occurences
    occurences = soup.find_all("div", {"class": "lister-item-content"})

    # Iterate through each occurence, extracting relevant information and storing it in the dictionary
    for occurence in occurences:
        movies['title'].append(get_html_text(occurence, 'h3', {'class': 'lister-item-header'}))
        movies['year'].append(get_html_text(occurence, 'span', {'class:', 'lister-item-year text-muted unbold'})) 
        movies['rating'].append(get_html_text(occurence, 'span', {'class': 'certificate'}))
        movies['runtime'].append(get_html_text(occurence, 'span', {'class': 'runtime'}))
        movies['genre'].append(get_html_text(occurence, 'span', {'class': 'genre'}))
        movies['score'].append(get_html_text(occurence, 'span', {'class': 'ipl-rating-star__rating'}))
        movies['gross'].append(get_html_text(occurence, 'span', {'name': 'nv'}))

        names = occurence.find_all('p', {'class': 'text-muted text-small'})
        text_list = [name.get_text() for name in names]
        director_list = [x for x in text_list if "Director" in x]

        movies['director'].append(director_list[0] if director_list else "")

    # Return a pandas dataframe created from the dictionary
    return pd.DataFrame(movies)




# Read in Disney Fandom Data

def scrape_fandom(webpage):
    """ Scrapes data from the Disney Fandom webpage.

    Args:
      webpage: An Disney Fandom webpage link to get the data from.

    Returns:
      A raw, uncleaned IMDB dataframe.
    """
    response = requests.get(url)

    # make soup
    soup = BeautifulSoup(response.text, "html.parser")

    # get title/year informtion
    book_list = soup.find_all("a", {"class":"category-page__member-link"})

    # parse through data
    adapt_list = []
    for title in book_list:
        adapt_list.append(title.get_text())

    return pd.DataFrame(adapt_list, columns = ['title']).dropna()
