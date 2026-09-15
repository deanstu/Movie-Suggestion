'''
This script will generate a random movie suggestion from a set of Letterboxd users watchlist.
Each user's username is stored in a text file called "users.txt" and each user should have an update watchlist on letterboxd.com. 
The script will gather all users' watchlists, combine them to a single list, and then randomly select a movie from that list to suggest.
'''

import requests
import math
import sys
import re
from bs4 import BeautifulSoup
from pprint import pprint
import json
from time import time
from time import sleep, time
#import argparse #might want to use later if needed complexity increases

def getUsernamesFromFile():
    with open("users.txt", 'r') as f:
        return [line.strip() for line in f]

def getWatchlistUrls(user):
    
    baseUrl = f'https://letterboxd.com/{user}/watchlist/'
    html = requests.get(baseUrl).text

    varStart = html.find('data-num-entries!!')+18 # data segement in the HTML that contains the number of movies in the watchlist

    if varStart == 17: # if the string is not found, the user does not have a watchlist
        print(f"User {user} does not have a watchlist.")
        return []
    
    numOfPages = math.ceil(int(html[varStart:html.find('"', varStart)]) / 28) # letterboxed watch list has a seperate page for every 28 movies, so we need to find out how many pages there are in the watchlist

    urls = []
    urls.append(baseUrl) # add the first page of the watchlist to the list of urls, each page after is in the format baseUrl/page/{pageNum}/

    for i in range(2, numOfPages + 1):
        urls.append(f'{baseUrl}page/{i}/') # add the rest of the pages to the list of urls

    return urls
    #soup = BeautifulSoup(html, 'html.parser')
    #pageDiv = str(soup.find("div", {'class': "pagination"}))

urls = getWatchlistUrls("deanonfilm")

for url in urls:
    print(url)
r=requests.get('https://letterboxd.com/').text
#print(r)