import requests
import urllib
import requests_html
import string
import time
import json
import re
import typing
import pandas as pd

from requests_html import HTMLSession
from bs4 import BeautifulSoup as Soup
from get_ids import *


def get_movies():
    '''
    retrieves movies and related information from the top 1000 titles;
    returns 6 lists, 
    might remove (replaced by dataframe search)
    '''
    ranks = []
    titles = []
    ref_num = []
    pages = []
    gross_earnings = []
    release_years = []
        
    for offset in range(0,801,200):
        task = 'https://www.boxofficemojo.com/chart/top_lifetime_gross/?offset='
        task = task + str(offset)
        response = requests.get(task)
        data = response.text
        soup = Soup(data, 'lxml')

        tags = soup.find('div', id='table')
        i = 0
        for i in range(1,201):
            ranking_tags = tags.find_all('tr')
            row = ranking_tags[i].find_all('td')

            r = re.search('[,0-9]+',str(row[0]))
            ranks.append(int(r.group(0).replace(',','')))
            
            ref = re.search('/tt[0-9]+/',str(row[1]))
            ref_num.append(ref.group(0).replace('/',''))

            t = re.search('>[(&amp;|&)½?/!0-9 éa-zA-Z,.:\'\·-]+<',str(row[1]))
            result = t.group(0).replace('>','').replace('<','').replace('amp;','')
            titles.append(result)

            g = re.search('[0-9,]+',str(row[2]))
            gross_earnings.append(int(g.group(0).replace(',','')))

            y = re.search('[0-9]+',str(row[3]))
            release_years.append(int(y.group(0)))
        for num in ref_num:
            page = 'imdb.com/title/'
            page = page + num
            pages.append(page)
    
    return(ranks, titles, ref_num, pages, gross_earnings, release_years)

    
def get_titles(soup):
    tags = soup.find('div', class_="title_wrapper")
    title_tag = tags.find('h1')
    t = re.search('>[(&amp;|&)½?/!0-9 éa-zA-Z,.:\'\·-]+',str(title_tag))
    return(t.group(0).replace('>','').replace('<',''))
   

def get_years(soup):
   # tags = soup.find('div', class_="title_wrapper") #likely not necessary (redundant)
    year_tag = soup.find('span', id='titleYear')
    y = re.search('>[0-9]+<', str(year_tag))
    return(y.group(0).replace('>','').replace('<',''))


def get_directors(soup:str):
    '''
    retrieves the direcors for a given film
    returns a list of strings
    '''
    directors = [] 
  
    tags = soup.find_all('div', class_='credit_summary_item')
    for tag in tags:
        if "Director" in str(tag):
            clean = re.findall('>[a-zA-z .]*[a-z]+<', str(tag))
            for item in clean:
                directors.append(item.replace('>','').replace('<',''))
    return(directors)


def get_mpaa_rating(soup:str): 
    '''
    retrieves the mpaa rating (ie PG-13) for a given film
    '''
    mpaa_rating = []

    tags = soup_main.find('div', class_="title_wrapper")
    mpaa = tags.find_all("div", class_="subtext")
    r = re.search('\s[a-zA-Z0-9/-]+\s',str(mpaa))
    rating = str(r.group(0).strip())
    if "Not" in rating:
        rating += " Rated"
    return(rating)


def get_keywords(soup:str):
    '''
    retrieves the top keywords for a given film
    returns a list of strings
    '''
    keywords = []

    tags = soup.find_all('span', class_='itemprop')
   
    for item in tags:
        clean = re.findall('[a-zA-Z ]+', str(item))
        keywords.append(clean[2])
    return keywords

def get_genres(soup:str):
    '''
    retrieves the genre types for a given film
    returns a list of strings
    '''
    genre_tag = []
    genre = []

    tags = soup.find_all('div', class_='see-more inline canwrap')
    for category in tags:
        category = str(category)
        if "genre" in category:
            genre_tag = category
    clean = re.findall('>[ ][a-zA-Z ]+<', str(genre_tag))
    for item in clean:
        item = item.replace('> ','').strip()
        item = item.replace('<','').strip()
        genre.append(item)
    return(genre)

def get_budget(soup:str): 
    '''
    retrieves the budget for a given film
    '''
    budget = int()

    tags = soup.find('div', id='titleDetails')
    box_office = tags.find_all('div', class_="txt-block")
    for item in box_office:
        if "Budget" in str(item):
            b = re.search('([0-9]*,[0-9]*)+',str(item))
            budget = int(b.group(0).replace('$','').replace(',',''))
    return(budget)

def get_gross(soup:str): 
    '''
    retrieves the budget for a given film
    '''
    gross = int()

    tags = soup.find('div', id='titleDetails')
    box_office = tags.find_all('div', class_="txt-block")
    for item in box_office:
        if "Gross USA" in str(item):
            p = re.search('([0-9]*,[0-9]*)+',str(item))
            gross = int(p.group(0).replace('$','').replace(',',''))          
    return(gross)

def get_actors(soup:str):
    '''
    retrieves the actors and their corresponding character roles for a given film
    returns two lists of strings
    '''
    actors = []
    characters = []

    tags = soup.find('table', class_= "cast_list")
    actor_tags = tags.find_all('a')
    character_tags = tags.find_all('td', class_='character')

    for character in character_tags:
        clean = re.findall('>[ ]*[\s]*[a-zA-ZÀ-ÿ.\]*[ ]*[a-zA-Z]+', str(character))
        for people in clean:
                characters.append(people.replace('>','').strip())
    for actor in actor_tags:
        try:
            clean = re.search('>[ ]*[\s]*[a-zA-ZÀ-ÿ.\]*[ ]*[a-zA-Z]+', str(actor)).group(0)
            if((clean.replace('>','').strip() not in characters) & (len(actors) <= len(characters))):
                actors.append(clean.replace('>','').strip())
        except:
            pass
    return([actors, characters])

def get_awards(page:str):  
    '''
    retrieves the number of award wins and nomination for a single film
    returns two lists of integers
    '''
    wins = []
    nominations = []
    task_awards = page + '/awards'
    response_awards = requests.get(task_awards)
    data_awards = response_awards.text
    soup_awards = Soup(data_awards,'lxml')
    tags_awards = soup_awards.find('div', class_='desc')

    if tags_awards is None:
        wins = 0
        nominations = 0
    
    else:
        w = re.search('[0-9 ]+ win', str(tags_awards))
        wins = int(w.group(0).replace(' win','').replace('s',''))
        n = re.search('[0-9 ]+ nomination', str(tags_awards))
        nominations = int(n.group(0).replace(' nomination','').replace('s',''))

    return[wins, nominations]

def get_scores(page:str): 
    '''
    retrieves the average critic score for a single film
    '''
    scores = []
    task_score = page + '/criticreviews'
    response_score = requests.get(task_score)
    data_score = response_score.text
    soup_score = Soup(data_score,'lxml')
    check_for_score = str(soup_score.find_all('span', id='noContent'))
    if "There are no Metacritic reviews" in check_for_score:
        scores = -1
    else:
        tags = soup_score.find('div', class_='metascore_wrap')
        s = re.search('>[0-9]+<',str(tags))
        scores = int(s.group(0).replace('>','').replace('<',''))
    return(scores)



if __name__ == "__main__":
    
    # page is the url for a specific film following the format https://www.imdb.com/title/title_code
    # with title_code being the unique identifier for each film obtained from get_ids

    page = 'https://www.imdb.com/title/'

    codes_list = []
    titles_list = []
    years_list = []
    actors_list =[] 
    directors_list = []
    ratings_list = []
    keywords_list = []
    genres_list = []
    budgets_list = []
    gross_list = []
    scores_list = []
    awards_list = []
    broken_list = []
    extended_list = []
    reason_list = []

    
    for i in range (20000,40000):
        code = title_codes[i]
    #failed_codes = []
    #for i in range (0,len(failed_codes)): #title_codes derived from get_ids
        #code = failed_codes[i]

        reasons = []

        try:
            new_page = page + code
            task_main = new_page
            response_main = requests.get(task_main)
            data_main = response_main.text
            soup_main = Soup(data_main, 'lxml')
            try:
                next_budget = (get_budget(soup_main)) #feed soup
            except:
                reasons.append("budget")
                next_budget = 1
                broken_list.append(code)
            try:    
                next_gross = (get_gross(soup_main)) #feed soup
            except:
                reasons.append("gross")
                next_gross = 1
                if code not in broken_list:
                    broken_list.append(code)
            if ((next_budget > 0) & (next_gross > 0)):
                try:
                    next_title = (get_titles(soup_main))
                except:
                    reasons.append("title")
                    if code not in broken_list:
                        broken_list.append(code)
                try:
                    next_year = (get_years(soup_main)) #feed soup
                except:
                    reasons.append("year")
                    if code not in broken_list:
                        broken_list.append(code)
                try:
                    next_actor = (get_actors(soup_main)) #feed soup
                except:
                    reasons.append("actors")
                    if code not in broken_list:
                        broken_list.append(code)
                try:
                    next_director = (get_directors(soup_main)) #feed soup
                except:
                    reasons.append("directors")
                    if code not in broken_list:
                        broken_list.append(code)
                try:
                    next_rating = (get_mpaa_rating(soup_main)) #feed soup
                except:
                    reasons.append("rating")
                    if code not in broken_list:
                        broken_list.append(code)
                try:
                    next_keyword = (get_keywords(soup_main)) #feed soup
                except:
                    reasons.append("keywords")
                    if code not in broken_list:
                        broken_list.append(code)
                try:
                    next_genre = (get_genres(soup_main)) #feed soup
                except:
                    reasons.append("genre")
                    if code not in broken_list:
                        broken_list.append(code)
                try:
                    next_score = (get_scores(new_page)) #feed page
                except:
                    reasons.append("score")
                    if code not in broken_list:
                        broken_list.append(code)
                try:
                    next_award = (get_awards(new_page)) #feed page
                except:
                    reasons.append("awards")
                    if code not in broken_list:
                        broken_list.append(code)

                if code not in broken_list:
                    codes_list.append(code)
                    titles_list.append(next_title)
                    years_list.append(next_year)
                    actors_list.append(next_actor)
                    directors_list.append(next_director)
                    ratings_list.append(next_rating)
                    keywords_list.append(next_keyword)
                    genres_list.append(next_genre)
                    budgets_list.append(next_budget)
                    gross_list.append(next_gross)
                    scores_list.append(next_score)
                    awards_list.append(next_award)

        except:
            broken_list.append(code)
            reasons.append("soup")

        extended_list.append(reasons)

        print(i)

    reason_list = [x for x in extended_list if x != []]
    
    
    
    data = {'Code': codes_list,
            'Title': titles_list,
            'Year': years_list,
            'Actors': actors_list,
            'Rating': ratings_list,
            'Keywords': keywords_list,
            'Genres': genres_list,
            'Budget': budgets_list,
            'Gross': gross_list,
            'Metcritic Score': scores_list,
            'Awards': awards_list}
    compiled_df = pd.DataFrame(data)
    
    
    pd.set_option('display.max_columns',None)
    compiled_df.to_csv(r'compiled_dataframe_2.csv')

    print(broken_list)
    print(reason_list)

    if (len(broken_list) > 0):
        fail_data = {'Code': broken_list,
                    'PoF': reason_list}
        failed_df = pd.DataFrame(fail_data)
        failed_df.to_csv(r'failed_codes_2.csv')
    
 
    
    


    

    
   

