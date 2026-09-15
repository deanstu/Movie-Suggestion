'''
Using this file, you can run test cases to verify that the script is working as expected. 
The test cases are designed to cover various scenarios, including edge cases, to ensure the robustness of the script.

'''
global USE_TEST_WATCHLIST # This global is used as a flag to determine if the script should use the test watchlist or the users.txt file to get the list of users.
global TEST_WATCHLIST # This global is used to store a test watchlist for testing purposes. It contains a dictionary where the keys are usernames and the values are lists of movies in their watchlists.

USE_TEST_WATCHLIST = False
TEST_WATCHLIST = {'deanonfilm': ['Goldfinger (1964)', 'From Russia with Love (1963)', 'Dr. No (1962)', 'Coyote vs. Acme (2026)'], 'emilykaloudis': ['The Big Sick (2017)', 'Thelma (2024)', 'Reservoir Dogs (1992)', 'The Irishman (2019)', 'Taxi Driver (1976)', 'Blade (1998)', 'Bullet Train (2022)', 'Ferrari (2023)', 'The Virgin Suicides (1999)', "One Flew Over the Cuckoo's Nest (1975)", 'A Clockwork Orange (1971)', 'Waiting... (2005)', 'Midsommar (2019)', 'Fresh (2022)', "Bill & Ted's Bogus Journey (1991)", 'Bill & Ted Face the Music (2020)', 'The Good Nurse (2022)', 'My Policeman (2022)', 'Fall (2022)', 'Hook (1991)', 'Robots (2005)', "Molly's Game (2017)", '127 Hours (2010)', 'Passengers (2016)', 'My Own Private Idaho (1991)', 'Loving Vincent (2017)', 'Chernobyl (2019)', 'CODA (2021)', 'Trainspotting (1996)', 'Aftersun (2022)', 'Atomic Blonde (2017)', 'Lucy (2014)', 'Ant-Man and the Wasp: Quantumania (2023)', 'Top Gun (1986)', 'The Marvels (2023)', 'Oppenheimer (2023)']}

from suggestion import *

def testGivenFile(username="", numSuggestions=1):

    userWatchlists = {}
    usernames = getUsernamesFromFile()
    for user in usernames:
        if PRINT_INFORMATIONAL: print(f"Getting watchlist for user: {user}")
        movieList=[]
        urls = getWatchlistUrls(user)
        for url in urls:
            movieList.extend(getWatchlistMovies(url))
        userWatchlists[user] = movieList
    
    print(getRandomMovie(userWatchlists, username, numSuggestions))

def test_cases():
    print("Running test cases for suggestion.py\n================================================\n")
    print("Test case 1: Get a random movie from all users' watchlists")
    testGivenFile()
    print("------------------------------------------------")
    print("\nTest case 2: Get a random movie from a specific user's watchlist")
    testGivenFile("emilykaloudis")
    print("------------------------------------------------")
    print("\nTest case 3: Get 3 random movies from all users' watchlists")
    testGivenFile("", 3)
    print("------------------------------------------------")
    print("\nTest case 4: Get 3 random movies from a specific user's watchlist")
    testGivenFile("emilykaloudis", 3)
    print("------------------------------------------------")
    print("\nTest case 5: Get a random movie from a user with no watchlist")
    testGivenFile("userwithnowatchlist")
    print("\nTest case 6: Get a random movie from a user with a watchlist that has less than the requested number of suggestions")
    testGivenFile("deanonfilm", 100)

test_cases()