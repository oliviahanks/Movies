import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

if __name__ == '__main__' :

    ### get disney subset data ###
    url = "https://editorial.rottentomatoes.com/guide/disney-100-essential-movies/"

    response = requests.get(url)
    #response.status_code

    # make soup
    soup = BeautifulSoup(response.text, "html.parser")

    # find all information
    all_headers = soup.find_all(re.compile('^h[2]$'))

    movie_list = []
    movie_info = []
    for movie in all_headers:
        movie_info = []

        # get Title
        if movie.find('a') != None:
            movie_info.append(movie.find('a').get_text())
        
        # get rest of information
        span = movie.find_all('span')
        for test in span:
            # get Year, Score
            if test != None and test.text != '':
                movie_info.append(test.text)
            # get Category
            elif test != None:
                movie_info.append(test['title'])

        movie_list.append(movie_info)


    ### Clean Data ###

    # remove rows without movies
    movie_df = pd.DataFrame(movie_list, columns = ['Title', 'Year', 'Category', 'Score']).dropna()
    
    # clean movie_df
    movie_df['Year'] = movie_df['Year'].astype(str).str.findall('\d+').apply(lambda x: ''.join(x)).astype(int)
    movie_df['Score'] = movie_df['Score'].astype(str).str.findall('\d+').apply(lambda x: ''.join(x)).astype(int)

    # create Rank
    movie_df['Rank'] = movie_df.sort_values(by=['Score'], ascending=False) \
                .reset_index() \
                .sort_values('index') \
                .index + 1

    # reset index
    movie_df = movie_df.sort_values(by = ['Score'], ascending=False).reset_index(drop = True)

    ### Get Book Data ###

    url2 = "https://disney.fandom.com/wiki/Category:Films_based_on_books"

    response2 = requests.get(url2)
    #response2.status_code

    # make soup
    soup2 = BeautifulSoup(response2.text, "html.parser")

    # get title/year informtion
    book_list = soup2.find_all("a", {"class":"category-page__member-link"})

    # parse through data
    adapt_list = []
    for title in book_list:
        adapt_list.append(title.get_text())

    book_df = pd.DataFrame(adapt_list, columns = ['title']).dropna()

    ### Clean Data ###

    book_df['year'] = book_df['title'].astype(str).str.findall('\((\d{4})').apply(lambda x: ''.join(x))
    book_df['title'] = book_df['title'].str.findall('(^.*?)\s(?=\()').apply(lambda x: ''.join(x))


    ### Merge Data ###

    merged_list = movie_df.merge(book_df, how = 'left', left_on = ['Title'], right_on = ['title'])
    # might be a little issue with the merge but will work on later
    merged_list.to_csv('data/bookdata.csv')
