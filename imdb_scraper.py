import requests
import urllib
import requests_html
import string
import time
import json
import re

from requests_html import HTMLSession
from bs4 import BeautifulSoup as Soup

if __name__ == "__main__":
    task = 'https://www.imdb.com/title/tt1291150/?ref_=nv_sr_srsg_0'
    response = requests.get(task)
    data = response.text
    soup = Soup(data, 'lxml')

def get_mpaa_rating():
    tags = soup.find('div', id="titleStoryLine")
    mpaa = tags.find_all('span')
    target = "Rated"
    for doodad in mpaa:
        doodad = str(doodad)
        if target in doodad:
            mpaa_rating = doodad.split(' ')
    return mpaa_rating[1]

def get_keywords():  
    tags = soup.find_all('span', class_='itemprop')
    keywords = []
    for item in tags:
        clean = re.findall('[a-zA-Z ]+', str(item))
        keywords.append(clean[2])
    return keywords

def get_genres():
    tags = soup.find_all('div', class_='see-more inline canwrap')
    genre_tag = []
    genre = []
    for catagory in tags:
        catagory = str(catagory)
        if "genre" in catagory:
            genre_tag = catagory
    clean = re.findall('>[ ][a-zA-Z ]+<', str(genre_tag))
    for item in clean:
        item = item.replace('> ','').strip()
        item = item.replace('<','').strip()
        genre.append(item)
    return(genre)

def get_actors():
    tags = soup.find('table', class_= "cast_list")
    actor_tags = tags.find_all('a')
    character_tags = tags.find_all('td', class_='character')

    actors = []
    characters = []
    for character in character_tags:
        clean = re.findall('>[ ]*[\s]*[a-zA-Z.\]*[ ]*[a-zA-Z]+', str(character))
        for boi in clean:
            if(boi.replace('>','').strip() not in characters):
                characters.append(boi.replace('>','').strip())
    for actor in actor_tags:
        try:
            clean = re.search('>[ ]*[\s]*([a-zA-Z.]*[ ]*)*[a-zA-Z]+', str(actor)).group(0)
            if((clean.replace('>','').strip() not in characters) & (len(actors) <= len(characters))):
                actors.append(clean.replace('>','').strip())
        except:
            pass
    noice = [actors,characters]
    return noice