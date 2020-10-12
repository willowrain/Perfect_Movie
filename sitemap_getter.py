import requests
import urllib
import requests_html
import string
import time
import json
import re

from requests_html import HTMLSession
from bs4 import BeautifulSoup as Soup

def addTask(data):
    resp = requests.post('https://us-central1-jawn-finder.cloudfunctions.net/api/task', json=data)
    #print(resp)
    return resp.status_code == 200
    
if __name__ == "__main__":
    # Gets the sitemap and formats it into lxml for BeautifulSoup, check robots.txt to find sitemap sometimes
    sitemapIndexURL = "https://www.imdb.com/sitemap/title-1888.xml.gz"
    session = HTMLSession()
    sitemapIndexReq = session.get(sitemapIndexURL)
    soup = Soup(sitemapIndexReq.text, 'lxml')
    print(soup.find_all('loc'))
    # Finds all urls
    # for sitemap in soup.find_all('loc'):
    #     sitemapReq = session.get(sitemap.text)
    #     sitemapSoup = Soup(sitemapReq.text, 'lxml')

    #     Filters so only how to urls are checked
    #     for url in sitemapSoup.find_all('loc'):
    #         tasks.append(url.text)  
