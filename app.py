from random import randint, random
from bs4 import BeautifulSoup
from numpy import empty
import pandas as pd
from time import sleep
import requests
import random
import os


HEADERS = ({
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
    })

#https://www.etsy.com/in-en/search/shops?order=alphabetical&search_type=shops&page=1&ref=pagination&search_query=india
URL1 = "https://www.etsy.com/in-en/search/shops?order=alphabetical&search_type=shops&page="
URL2 = "&ref=pagination&search_query=india"


items =[]
for i in range(357, 358):
    print('Processing {0}...'.format(URL1 + '{0}'.format(i) + URL2))
    response = requests.get(URL1 + '{0}'.format(i) + URL2, headers= HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    results = soup.find_all('div', {'class': 'wt-card wt-card--transparent wt-width-full'})
    
    for result in results:

       

        try:
            shop_name = result.find('p', {'class': 'wt-text-title-01 wt-text-truncate'}).text
            shop_dec = result.find('p', {'class': 'wt-text-caption wt-text-truncate'}).text
            
            product_url = result.a['href']
            item_count = result.find('p', {'class': 'wt-text-caption wt-text-gray wt-pl-xs-1 wt-no-wrap'}).text
            items.append([shop_name, shop_dec, item_count, product_url ])
            print(items.size())
        except AttributeError:
            continue
    sleep(random.uniform(2,4)) #to avoid requesting multiple data per sec and get blacklisted


df = pd.DataFrame(items, columns=['Shop Name', 'Shop Description', 'Item Count',  'product url'])
df.to_csv('{0}.csv'.format('etsy_india_search_lastpage'), index=False)