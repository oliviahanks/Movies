"""
This script performs the webscraping and produces the raw dataset to be cleaned.
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup



# Read in Rotten Tomatoes Data


r2 = requests.get("https://editorial.rottentomatoes.com/guide/disney-100-essential-movies/")

soup2 = BeautifulSoup(r2.text)

movies = {'title':[], 'year':[], 'score':[], 'actors':[], 'director':[]}

occurences = soup2.find_all("div", {"class": "row countdown-item"})
for occurence in occurences:
    movies['title'].append(occurence.find('div', {'class': 'article_movie_title'}).text)
    movies['year'].append(occurence.find('span', {'class:', 'subtle start-year'}).text) 
    movies['score'].append(occurence.find('span', {'class': 'tMeterScore'}).text)
    movies['actors'].append(get_html_text(occurence, 'div', {'class': 'info cast'}))
    movies['director'].append(get_html_text(occurence, 'div', {'class': 'info director'}))

rotten_tomatoes = pd.DataFrame(movies)

rotten_tomatoes.to_csv('disney_movie_analysis/data/rotten_tomatoes_raw.csv', index = False)





# Read In IMDB Data

r3 = requests.get("https://www.imdb.com/list/ls089035876/?sort=release_date,desc&st_dt=&mode=detail&page=1")
soup3 = BeautifulSoup(r3.text)

r4 = requests.get("https://www.imdb.com/list/ls089035876/?sort=release_date,desc&st_dt=&mode=detail&page=2")
soup4 = BeautifulSoup(r4.text)

r5 = requests.get("https://www.imdb.com/list/ls089035876/?sort=release_date,desc&st_dt=&mode=detail&page=3")
soup5 = BeautifulSoup(r5.text)

r6 = requests.get("https://www.imdb.com/list/ls089035876/?sort=release_date,desc&st_dt=&mode=detail&page=4")
soup6 = BeautifulSoup(r6.text)

r7 = requests.get("https://www.imdb.com/list/ls089035876/?sort=release_date,desc&st_dt=&mode=detail&page=5")
soup7 = BeautifulSoup(r7.text)


movies2 = {'title':[], 'year':[], 'score':[], 'runtime':[], 'rating':[], 'genre':[], 'gross':[], 'director': []}

occurences = soup3.find_all("div", {"class": "lister-item-content"}) + soup4.find_all("div", {"class": "lister-item-content"}) + soup5.find_all("div", {"class": "lister-item-content"}) + soup6.find_all("div", {"class": "lister-item-content"}) + soup7.find_all("div", {"class": "lister-item-content"}) 
for occurence in occurences:
    movies2['title'].append(get_html_text(occurence, 'h3', {'class': 'lister-item-header'}))
    movies2['year'].append(get_html_text(occurence, 'span', {'class:', 'lister-item-year text-muted unbold'})) 
    movies2['rating'].append(get_html_text(occurence, 'span', {'class': 'certificate'}))
    movies2['runtime'].append(get_html_text(occurence, 'span', {'class': 'runtime'}))
    movies2['genre'].append(get_html_text(occurence, 'span', {'class': 'genre'}))
    movies2['score'].append(get_html_text(occurence, 'span', {'class': 'ipl-rating-star__rating'}))
    movies2['gross'].append(get_html_text(occurence, 'span', {'name': 'nv'}))

    names = occurence.find_all('p', {'class': 'text-muted text-small'})
    text_list = [name.get_text() for name in names]
    director_list = [x for x in text_list if "Director" in x]

    movies2['director'].append(director_list[0] if director_list else "")

    imdb = pd.DataFrame(movies2)

imdb.to_csv('disney_movie_analysis/data/imdb.csv', index = False)
