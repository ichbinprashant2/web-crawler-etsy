from random import randint, random
from bs4 import BeautifulSoup
from numpy import empty
import pandas as pd
from time import sleep
import requests
import random

df = pd.read_csv("etsy_india_search.csv")

HEADERS = ({
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
    })

items= []
URL = [url for url in df['product url']]
for i in range(0,100):
    URL1 = URL[i]
    print('Processing {0}...'.format(URL1))
    response = requests.get(URL1, headers= HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    results = soup.find_all('div', {'class': 'wt-width-full wt-display-flex-xs wt-pl-xs-2'})
    reviews = []
    item_type = []
    sales = 0
    for result in results:

        
        try:
            shop_name = result.find('h1', {'class': 'wt-text-heading-01 wt-text-truncate'}).text
        except AttributeError:
            shop_name = "N/A"

        try:
            owner_res = soup.find('div', {'class': 'img-container', "data-editable-img": "user-avatar"})
            owner = owner_res.a['title']
        except AttributeError:
            owner = "N/A"

        try:
            location = result.find('span', {'class': 'shop-location wt-text-caption wt-text-gray wt-line-height-tight wt-wrap'}).text
            #shop-location wt-text-caption wt-text-gray wt-line-height-tight
        except AttributeError:
            location = "N/A"

        try:
            shop_desc = result.find('p', {'class': 'wt-text-caption wt-hide-xs wt-show-lg wt-wrap'}).text
        
        except AttributeError:
            continue

            ###############################################
        try:
            review = result.find('input', {'name': 'initial-rating'})
            if review is None:
                review = 0
                continue
            review = review['value']
        except AttributeError:
            review = 0

        try:
            #doesnt work
            review_count = result.find('div', {'class': 'display-inline-block vertical-align-middle'}).text
            
        except AttributeError:
            review_count = 0

        try:
            sale = result.find('span', {'class': 'wt-text-caption wt-no-wrap'}).text
            sales = 0
            for m in sale:
                if m.isdigit():
                    sales = sales*10 + int(m)

        except AttributeError:
            sales = 0

        try:
            
            item_types = soup.find_all('button', {'class': 'wt-tab__item wt-ml-md-0 wt-mr-md-0 wt-justify-content-space-between'})
            for a in item_types:
                c = a.find('span', {'class': 'wt-break-word wt-mr-xs-2'}).text
                c = c.strip()
                
                if c != 'On sale' or 'On Sale':
                    item_type.append(c)
            
        except AttributeError:
            item_type = ['N/A']
            
        try:
            review_find = soup.find_all('li', {'class': 'bt-xs-1 pt-xs-2 mb-xs-5'})
            
            
            for rev in review_find:
            
                try:
                    review_rating = rev.find('input', {'name': 'rating'})['value']
                    
                except AttributeError:
                    reviews= "N/A"
                try:
                    rev_name = rev.find('p', {'class': 'shop2-review-attribution'}).a.text
                    
                except AttributeError:
                    rev_name = "N/A"
                try:
                    rev_text = rev.find('p', {'class': 'prose break-word m-xs-0'}).text
                    
                except AttributeError:
                    rev_text = "N/A"

                reviews.append([rev_name, review_rating, rev_text])
        except AttributeError:
            reviews = ["N/A"]

    
    items.append([shop_name, owner, location, shop_desc, review,  sales, item_type, reviews ])
        
    sleep(1) #to avoid requesting multiple data per sec and get blacklisted

#, 'Avg Review Count'
df = pd.DataFrame(items, columns=['Shop Name', 'Owner', 'location', 'Description', 'Review', 'Sales', "Item Types", "Reviews"])
df.to_csv('{0}.csv'.format('sales_loc_debug'), index=False)