from random import randint, random
from bs4 import BeautifulSoup
from numpy import empty, product
import pandas as pd
from time import sleep
import requests

df = pd.read_csv("Shop_details.csv")
df2 = pd.read_csv("etsy_india_search.csv")

HEADERS = ({
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
    })

# listy = ['Blue River, Canada', 'Bedford, United Kingdom', 'Guwahati, Assam', 'New York, United States', 'Ludhiana, Punjab', 
# 'Jālna, Maharashtra', 'Buenos Aires, Argentina', 'India', 'Khurja, Uttar Pradesh', 'Panchkula, Haryana', 'Colorado, United States', 
# 'Uxbridge, Canada', 'Haridwar, Uttarakhand', 'Florida, United States', 'Unnāo, Uttar Pradesh', 'Guntur, Andhra Pradesh', 
# 'Birmingham, United Kingdom', 'Kentucky, United States', 'Panipat, Haryana', 'Ajmer, Rajasthan', 'Utah, United States',
#  'Camberley, United Kingdom', 'Oklahoma, United States', 'Barcelona, Spain', 'Nevada, United States', 'Massachusetts, United States',
#   'Richmond Hill, Canada', 'Bristol, United Kingdom', 'Leicester, United Kingdom', "Bishop's Stortford, United Kingdom", 'Jalandhar, Punjab',
#    'Jorhāt, Assam', 'Maine, United States', 'Glasgow, United Kingdom', 'Oxford, United Kingdom', 'Leeds, United Kingdom', 'Espoo, Finland', 
#    'Nānpāra, Uttar Pradesh', 'Chesham, United Kingdom', 'Pindwāra, Rajasthan', 'Balearic Islands, Spain', 'Brisbane, Australia', 
#    'Newcastle upon Tyne, United Kingdom', 'Ashford, United Kingdom', 'Cologne, Germany', 'Jaisalmer, Rajasthan', 'Cambridge, United Kingdom', 
#    'Pune, Maharashtra', 'Kochi, Kerala', 'Ooty, Tamil Nadu', 'Indore, Madhya Pradesh', 'Yamunanagar, Haryana', 'Tamil Nadu, India', 
#    'North Carolina, United States', 'Bhubaneswar, Odisha', 'Sunshine Coast, Australia', 'Gurgaon, Haryana', 'Chennai, Tamil Nadu',
#     'Lancaster, United Kingdom', 'City of London, United Kingdom', 'Billericay, United Kingdom', 'Pennsylvania, United States', 
#     'Ponce, Puerto Rico', 'Gweek, United Kingdom', 'Uttar Pradesh, India', 'South Carolina, United States', 'West Bengal, India', 
#     'Samrāla, Punjab', 'Thāne, Maharashtra', 'Shipton under Wychwood, United Kingdom', 'Bhadohi, Uttar Pradesh', 'Georgia, United States', 
#     'Khambhāt, Gujarat', 'Calgary, Canada', 'Navi Mumbai, Maharashtra', 'Maple Ridge, Canada', 'Ottawa, Canada', 'Bruges, Belgium', 
#     'Rajkot, Gujarat', 'Connecticut, United States', 'Mysore, Karnataka', 'Puducherry, India', 'Alabama, United States', 
#     'Hyderabad, Telangana', 'Virginia, United States', 'Washington, D.C., United States', 'Salisbury, United Kingdom', 'Jaipur, Rajasthan', 
#     'Illinois, United States', 'Waterloo, Canada', 'Rochea', 'Old Goa, Goa', 'Bath, United Kingdom', 'Kollam, Kerala']


listy = ['Guwahati, Assam',  'Ludhiana, Punjab', 
'Jālna, Maharashtra',  'India', 'Khurja, Uttar Pradesh', 'Panchkula, Haryana', 'Haridwar, Uttarakhand',  'Unnāo, Uttar Pradesh', 
'Guntur, Andhra Pradesh', 'Panipat, Haryana', 'Ajmer, Rajasthan','Jalandhar, Punjab', 'Jorhāt, Assam','Nānpāra, Uttar Pradesh',  
'Pindwāra, Rajasthan',  'Jaisalmer, Rajasthan', 'Pune, Maharashtra', 'Kochi, Kerala', 'Ooty, Tamil Nadu', 
'Indore, Madhya Pradesh', 'Yamunanagar, Haryana', 'Tamil Nadu, India', 'Bhubaneswar, Odisha',  'Gurgaon, Haryana', 'Chennai, Tamil Nadu',
'Uttar Pradesh, India',  'West Bengal, India', 'Samrāla, Punjab', 'Thāne, Maharashtra',  'Bhadohi, Uttar Pradesh', 'Khambhāt, Gujarat', 
'Navi Mumbai, Maharashtra', 'Rajkot, Gujarat',  'Mysore, Karnataka', 'Puducherry, India', 
'Hyderabad, Telangana',  'Jaipur, Rajasthan',  'Old Goa, Goa',  'Kollam, Kerala']

name = [url for url in df2['Shop Name']]
loc = [url for url in df['location']]
cnt = [c for c in df2["Item Count"].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)]
c=0
for it in range(len(loc)):
    myset = set(loc)
newloc = list(myset)

for i in range(len(name)):
    if loc[i] in listy and cnt[i] > 1000 and cnt[i]<2000:
        
        print(name[i])

