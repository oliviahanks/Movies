import pandas as pd
import re


# Clean Rotten Tomatoes


rotten_tomatoes = pd.read_csv('disney_movie_analysis/data/rotten_tomatoes_raw.csv')

rotten_tomatoes = rotten_tomatoes.drop(32)

rotten_tomatoes['title'] = rotten_tomatoes['title'].str.replace('[\n]','', regex=True).str.replace('[(][^)]+[)]','', regex=True).str.replace('\d+[%]','', regex=True)

rotten_tomatoes['actors'] = rotten_tomatoes.actors.str.replace('[\n](Starring: )', '', regex = True)
rotten_tomatoes['director'] = rotten_tomatoes.director.str.replace('[\n](Directed By: )', '', regex = True)

rotten_tomatoes['actors'] = rotten_tomatoes['actors'].str.split(',')
rotten_tomatoes['director'] = rotten_tomatoes['director'].str.split(',')

rotten_tomatoes['year'] = rotten_tomatoes.year.apply(lambda x: re.findall('\d+', str(x))[0])
rotten_tomatoes['comparison_score'] = rotten_tomatoes.score.apply(lambda x: int(re.findall('\d+', x)[0])/10)

rotten_tomatoes['year'] = rotten_tomatoes.year.astype(int)
rotten_tomatoes['title'] = rotten_tomatoes.title.str.strip()

rotten_tomatoes.to_csv('disney_movie_analysis/data/rotten_tomatoes.csv', index = False)



# Clean IMDB


imdb = pd.read_csv('disney_movie_analysis/data/imdb_raw.csv')

imdb = imdb.drop(19, axis='index')
imdb = imdb.drop(170, axis='index')

imdb['year'] = imdb['year'].apply(lambda x: re.findall('\d+', str(x))[0]).astype(int)
imdb['runtime'] = imdb['runtime'].apply(lambda x: re.findall('\d+', str(x))[0]).astype(int)
imdb['gross'] = imdb['gross'].str.replace('[,]','', regex=True).astype(int)

imdb['score'] = imdb['score'].astype(float)

imdb['title'] = imdb['title'].str.replace('[\n][^\n]+[\n]','', regex=True)
imdb['genre'] = imdb['genre'].str.replace('[\n]','', regex=True).apply(lambda x: x.strip())

imdb[['director', 'actors']] = imdb['director'].str.replace('[\n]','', regex=True).apply(lambda x: x.replace(', ', ',')).apply(lambda x: x.strip()).str.split('|', expand = True)

imdb['actors'] = imdb.actors.str.replace('\s*Stars:\s*', '', regex = True).str.replace('\s*Star:\s*', '', regex = True)
imdb['director'] = imdb.director.str.replace('Directors:', '', regex = True).str.replace('Director:', '', regex = True)

imdb['actors'] = imdb['actors'].str.split(',')
imdb['director'] = imdb['director'].str.split(',')

imdb['title'] = imdb.title.str.strip()

imdb.to_csv('disney_movie_analysis/data/imdb.csv', index = False)
