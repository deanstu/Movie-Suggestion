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


# In production, these should be set to False, but for testing purposes, they can be set to True. 
RETURN_STATUS_CODES = False
PRINT_INFORMATIONAL = False

# ------------------------------------------------------------

def getUsernamesFromFile():
    '''
    reads the usernames from the users.txt file and returns them as a list. Each username should be on a new line in the file.

    Args:
        None

    Returns:
        list: A list of usernames read from the users.txt file.
    '''

    with open("users.txt", 'r') as f:
        return [line.strip() for line in f]

def writeUsernamesToFile(usernames):
    '''
    takes a list of usernames and writes them to the users.txt file, each on a new line.

    Args:
        usernames (list): A list of usernames to be written to the users.txt file.

    Returns:
        None
    '''

    with open("users.txt", 'w') as f:
        for username in usernames:
            f.write("username\n")

def getWatchlistUrls(user):
    '''
    gets the URLs of all pages in a user's watchlist.
    when a user has more than 28 movies in their watchlist, letterboxd.com will create multiple pages for the watchlist.
    This will return an empty list if the user does not have a watchlist or if the user does not exist. Does not distinguish between the two cases.

    Args:
        user (str): The username of the user whose watchlist URLs are to be retrieved.

    Returns:
        list: A list of URLs for all pages in the user's watchlist.
    '''

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
    '''
    gets the movies from a watchlist page. This function will return an empty list if the page does not exist or if there are no movies on the page.
    
    Args:
        url (str): The URL of the watchlist page from which to retrieve the movies.
        
    Returns:
        list: A list of movie titles retrieved from the watchlist page.
    '''

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




