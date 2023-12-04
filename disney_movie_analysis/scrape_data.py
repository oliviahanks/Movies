"""
This script performs the webscraping and produces the raw dataset to be cleaned.
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_html_text(bs, name, attrs):
    try:
        text = bs.find(name, attrs).text
    except:
        text = None
    return text


# Read in Rotten Tomatoes Data

def scrape_rotten_tomatoes(webpage):
    r = requests.get(webpage)

    soup = BeautifulSoup(r.text)

    movies = {'title':[], 'year':[], 'score':[], 'actors':[], 'director':[]}

    occurences = soup.find_all("div", {"class": "row countdown-item"})
    for occurence in occurences:
        movies['title'].append(occurence.find('div', {'class': 'article_movie_title'}).text)
        movies['year'].append(occurence.find('span', {'class:', 'subtle start-year'}).text) 
        movies['score'].append(occurence.find('span', {'class': 'tMeterScore'}).text)
        movies['actors'].append(get_html_text(occurence, 'div', {'class': 'info cast'}))
        movies['director'].append(get_html_text(occurence, 'div', {'class': 'info director'}))

    return pd.DataFrame(movies)




# Read In IMDB Data

def scrape_imdb(webpage):
    r = requests.get(webpage)
    soup = BeautifulSoup(r.text)

    movies = {'title':[], 'year':[], 'score':[], 'runtime':[], 'rating':[], 'genre':[], 'gross':[], 'director': []}

    occurences = soup.find_all("div", {"class": "lister-item-content"})

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

    return pd.DataFrame(movies)
