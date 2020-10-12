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
    print(noice)