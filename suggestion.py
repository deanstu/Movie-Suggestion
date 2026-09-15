'''
This script will generate a random movie suggestion from a set of Letterboxd users watchlist.
Each user's username is stored in a text file called "users.txt" and each user should have an update watchlist on letterboxd.com. 
The script will gather all users' watchlists, combine them to a single list, and then randomly select a movie from that list to suggest.
'''

from curl_cffi import requests
import math
from bs4 import BeautifulSoup
from time import time,sleep

# ------------------------------------------------------------
# this will be sent with the request to letterboxd.com to make it look like a real user is making the request, otherwise letterboxd will block the request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://google.com" # Tells the site you found them via Google
}


global RETURN_STATUS_CODES # This global is used as a flag to determine if the script should return the status codes of the requests made to letterboxd.com.
global PRINT_INFORMATIONAL # This global is used as a flag to determine if the script should print informational messages to the console.
global USE_TEST_WATCHLIST # This global is used as a flag to determine if the script should use the test watchlist or the users.txt file to get the list of users.

# In production, these should be set to False, but for testing purposes, they can be set to True. 
# When USE_TEST_WATCHLIST is set to True, 
# the script can be tested without having to make requests to letterboxd.com.
RETURN_STATUS_CODES = False
PRINT_INFORMATIONAL = False
USE_TEST_WATCHLIST = True
# ------------------------------------------------------------

def getUsernamesFromFile():

    with open("users.txt", 'r') as f:
        return [line.strip() for line in f]

def getWatchlistUrls(user):
    
    baseUrl = f'https://letterboxd.com/{user}/watchlist/'
    
    html = requests.get(baseUrl, headers=headers, impersonate="chrome120")
    if html.status_code != 200:
        if PRINT_INFORMATIONAL: print(f"Error getting watchlist for user {user}. Status code: {html.status_code}")
        return []
    if RETURN_STATUS_CODES: print(html.status_code)
    html = html.text

    varStart = html.find('data-num-entries')+18 # data segement in the HTML that contains the number of movies in the watchlist


    if varStart == 17: # if the string is not found, the user does not have a watchlist
        if PRINT_INFORMATIONAL: print(f"User {user} does not have a watchlist.")
        return []
    
    numOfPages = math.ceil(int(html[varStart:html.find('"', varStart)]) / 28) # letterboxed watch list has a seperate page for every 28 movies, so we need to find out how many pages there are in the watchlist

    urls = []
    urls.append(baseUrl) # add the first page of the watchlist to the list of urls, each page after is in the format baseUrl/page/{pageNum}/

    for i in range(2, numOfPages + 1):
        urls.append(f'{baseUrl}page/{i}/') # add the rest of the pages to the list of urls

    return urls

def getWatchlistMovies(url):

    if PRINT_INFORMATIONAL: print(f"Getting movies from {url}")
    html = requests.get(url, headers=headers, impersonate="chrome120")
    if RETURN_STATUS_CODES: print(html.status_code)
    if html.status_code != 200:
        if PRINT_INFORMATIONAL: print(f"Error getting movies from {url}. Status code: {html.status_code}")
        return []
    soup = BeautifulSoup(html.text, 'html.parser').find_all(attrs={"data-component-class": "LazyPoster"})
    movies = []

    for movie in soup:
        varStart = str(movie).find('data-item-full-display-name')+29
        title = str(movie)[varStart:str(movie).find('"', varStart)].replace('&amp;', '&') # replace &amp; with & in the title
        movies.append(title)

    return movies

def getRandomMovie(movies, username, numSuggestions):

    if len(movies) == 0:
        if PRINT_INFORMATIONAL: print("No movies found in the watchlists.")
        return None

    returnText = ""
    if username == "":
        movieList = []
        for userList in movies.values():
            movieList.extend(userList)
        for i in range(numSuggestions if numSuggestions <= len(movieList) else len(movieList)):
            movie=math.floor(time() * 1000) % len(movieList) # get a random movie from the list of movies
            returnText= returnText + f"Suggestion {i+1}: {movieList[movie]}\n" 
            movieList.pop(movie) # remove the movie from the list so it doesn't get suggested again
            
            
        return returnText

    else:
        if username not in movies:
            if PRINT_INFORMATIONAL: print(f"User {username} not found in the watchlists.")
            return None
        for i in range(numSuggestions if numSuggestions <= len(movies[username]) else len(movies[username])):
            movie=math.floor(time() * 1000) % len(movies[username]) # get a random movie from the list of movies for the specified user
            returnText+= f"Suggestion {i+1}: {movies[username][movie]}\n"
            movies[username].pop(movie) # remove the movie from the list so it doesn't get suggested again
        return returnText

def main(username="", numSuggestions=1):
    if not USE_TEST_WATCHLIST:
        userWatchlists = {}
        usernames = getUsernamesFromFile()
        for user in usernames:
            if PRINT_INFORMATIONAL: print(f"Getting watchlist for user: {user}")
            movieList=[]
            urls = getWatchlistUrls(user)
            for url in urls:
                movieList.extend(getWatchlistMovies(url))
            userWatchlists[user] = movieList
    else:
        userWatchlists = {'deanonfilm': ['Goldfinger (1964)', 'From Russia with Love (1963)', 'Dr. No (1962)', 'Coyote vs. Acme (2026)'], 'emilykaloudis': ['The Big Sick (2017)', 'Thelma (2024)', 'Reservoir Dogs (1992)', 'The Irishman (2019)', 'Taxi Driver (1976)', 'Blade (1998)', 'Bullet Train (2022)', 'Ferrari (2023)', 'The Virgin Suicides (1999)', "One Flew Over the Cuckoo's Nest (1975)", 'A Clockwork Orange (1971)', 'Waiting... (2005)', 'Midsommar (2019)', 'Fresh (2022)', "Bill & Ted's Bogus Journey (1991)", 'Bill & Ted Face the Music (2020)', 'The Good Nurse (2022)', 'My Policeman (2022)', 'Fall (2022)', 'Hook (1991)', 'Robots (2005)', "Molly's Game (2017)", '127 Hours (2010)', 'Passengers (2016)', 'My Own Private Idaho (1991)', 'Loving Vincent (2017)', 'Chernobyl (2019)', 'CODA (2021)', 'Trainspotting (1996)', 'Aftersun (2022)', 'Atomic Blonde (2017)', 'Lucy (2014)', 'Ant-Man and the Wasp: Quantumania (2023)', 'Top Gun (1986)', 'The Marvels (2023)', 'Oppenheimer (2023)']}
    print(getRandomMovie(userWatchlists, username, numSuggestions))

def test_cases():
    print("Running test cases for suggestion.py\n================================================\n")
    print("Test case 1: Get a random movie from all users' watchlists")
    main()
    print("------------------------------------------------")
    print("\nTest case 2: Get a random movie from a specific user's watchlist")
    main("emilykaloudis")
    print("------------------------------------------------")
    print("\nTest case 3: Get 3 random movies from all users' watchlists")
    main("", 3)
    print("------------------------------------------------")
    print("\nTest case 4: Get 3 random movies from a specific user's watchlist")
    main("emilykaloudis", 3)
    print("------------------------------------------------")
    print("\nTest case 5: Get a random movie from a user with no watchlist")
    main("userwithnowatchlist")
    print("------------------------------------------------")
    print("\nTest case 6: Get a random movie from a user with a watchlist that has less than the requested number of suggestions")
    main("deanonfilm", 100)

test_cases()

