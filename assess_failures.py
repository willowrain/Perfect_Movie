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

if __name__ == "__main__":

    page = 'https://www.imdb.com/title/'

    failed_data = pd.read_csv('failed_data.csv')

    codes_list = failed_data["Code"].tolist()
    

    results = []
    cause = []
    i=0

    for code in codes_list:
        result = 'FAIL'
        reasons = []
        
        try:
            new_page = page + code
            task_main = new_page
            response_main = requests.get(task_main)
            data_main = response_main.text
            soup_main = Soup(data_main, 'lxml')
            try:
                tags = soup_main.find('div', class_='credit_summary_item')
                string = "in development"
                if (string) in str(tags):
                    result = 'PASS'
                    reasons.append('in progress')
            except:
                pass
                
            try:
                tags = soup_main.find('div', id='titleDetails')
                country = tags.find('div', class_='txt-block')
                if 'United States' not in country:
                    result = 'PASS'
                    reasons.append('foreign')
            except:
                pass
            
            try:
                tags = soup_main.find_all('div', class_='see-more inline canwrap')
                for category in tags:
                    category = str(category)
                    if "genre" in category:
                        genre_tag = category
                if "Documentary" in genre_tag:
                    result = 'PASS'
                    reasons.append('documentary')
            except:
                pass
            
        except:
            result = ('FAIL')
            reasons.append('soup')

        if reasons == []:
            result = ('FAIL')
            reasons.append('unknown')
            
        results.append(result)
        cause.append(reasons)

        print(i)
        i += 1

    failed_data['P/F'] = results
    failed_data['Cause'] = cause

    failed_data.to_csv(r'failed_data_processed.csv')
