from random import randint, random
from bs4 import BeautifulSoup
from numpy import empty, product
import pandas as pd
from time import sleep
import requests
import os

df = pd.read_csv("etsy_india_search.csv")
df2 = pd.read_csv("Shop_details.csv")

HEADERS = ({
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
    })


listy = ['Guwahati, Assam',  'Ludhiana, Punjab', 
'Jālna, Maharashtra',  'India', 'Khurja, Uttar Pradesh', 'Panchkula, Haryana', 'Haridwar, Uttarakhand',  'Unnāo, Uttar Pradesh', 
'Guntur, Andhra Pradesh', 'Panipat, Haryana', 'Ajmer, Rajasthan','Jalandhar, Punjab', 'Jorhāt, Assam','Nānpāra, Uttar Pradesh',  
'Pindwāra, Rajasthan',  'Jaisalmer, Rajasthan', 'Pune, Maharashtra', 'Kochi, Kerala', 'Ooty, Tamil Nadu', 
'Indore, Madhya Pradesh', 'Yamunanagar, Haryana', 'Tamil Nadu, India', 'Bhubaneswar, Odisha',  'Gurgaon, Haryana', 'Chennai, Tamil Nadu',
'Uttar Pradesh, India',  'West Bengal, India', 'Samrāla, Punjab', 'Thāne, Maharashtra',  'Bhadohi, Uttar Pradesh', 'Khambhāt, Gujarat', 
'Navi Mumbai, Maharashtra', 'Rajkot, Gujarat',  'Mysore, Karnataka', 'Puducherry, India', 
'Hyderabad, Telangana',  'Jaipur, Rajasthan',  'Old Goa, Goa',  'Kollam, Kerala']


name = [url for url in df['Shop Name']]
URL = [url for url in df['product url']]
loc = [location for location in df2['location']]
cnt = [c for c in df["Item Count"].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)]

filename = "GT2000"
os.chdir(filename)
ash = 0
for it in range(len(URL)):
    
    if cnt[it]>= 1000 and cnt[it]<2000 and loc[it] in listy:
        ash = ash + 1
        if ash == 17:
            items = []
            for i in range(1,11):
                URL1 = URL[it] + "?ref=items-pagination&page={0}&sort_order=custom#items".format(i)
                print('Processing {0}...'.format(URL1))
                response = requests.get(URL1, headers= HEADERS)
                soup = BeautifulSoup(response.content, 'html.parser')

                results = soup.find_all('div', {'class': 'js-merch-stash-check-listing'})
                
                for result in results:

                    
                    try:
                        product_url = result.find('a', {'class': 'listing-link wt-display-inline-block wt-transparent-card'})['href']
                    except AttributeError:
                        continue
                    
                    response_item= requests.get(product_url, headers= HEADERS)
                    soup_item = BeautifulSoup(response_item.content, 'html.parser')

                    results_item = soup_item.find_all('main', {'role': 'main'})
                    option0 = []
                    option1 = []
                    for resultItem in results_item:
                        
                        try:
                            product_name = resultItem.find('h1', {'class': 'wt-text-body-03 wt-line-height-tight wt-break-word'}).text
                        except AttributeError:
                            continue

                        try:
                            desc = resultItem.find('p', {'class': 'wt-text-body-01 wt-break-word'}).text
                            desc = desc.strip()
                        except AttributeError:
                            desc = "N/A"

                        try:
                            img_url = resultItem.find('img', {'class': 'wt-max-width-full wt-horizontal-center wt-vertical-center carousel-image wt-rounded'})['src']
                        except AttributeError:
                            img_url = "N/A"

                        # try:
                        #     rating_count = resultItem.find('span', {'class': 'wt-badge wt-badge--status-02 wt-ml-xs-2'}).text
                        # except AttributeError:
                        #     rating_count = 0
                        
                        try:
                            product_price = resultItem.find('p', {'class': 'wt-text-title-03 wt-mr-xs-2'}).text
                        except AttributeError:
                            
                            product_prices = resultItem.find('p', {'class': 'wt-text-title-03 wt-mr-xs-1'}).findAll('span')
                            prs= ""
                            for pr in product_prices:
                                prs += pr.text
                            product_price = 0
                            for m in prs:
                                if m.isdigit():
                                    product_price = product_price*10 + int(m)
                        
                        try:
                            cat = resultItem.find('a', {'class': 'wt-btn wt-action-group__item'}).text
                            cat = cat.strip()
                        except AttributeError:
                            cat = "N/A"

                        #options
                        try:
                            var0 = resultItem.find('select', {'id': 'variation-selector-0'}).findAll('option')
                            for x in var0:
                                y = x.text
                                y = y.strip()
                                option0.append(y)   
                        except:
                            continue

                        try:
                            var1 = resultItem.find('select', {'id': 'variation-selector-1'}).findAll('option')
                            for x in var1:
                                y = x.text
                                y = y.strip()
                                option1.append(y)   
                        except:
                            continue
                        
                    options = [option0, option1]
                    items.append([product_name, product_price, desc, img_url, cat, options, product_url ])   
                    
                    
                sleep(1) #to avoid requesting multiple data per sec and get blacklisted

            df = pd.DataFrame(items, columns=['Produce Name', 'Price', 'Description', 'Image', 'Category', 'Options', "Product URL"])
            df.to_csv('{0}.csv'.format(name[it]), index=False)