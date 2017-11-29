import urllib.parse
import time
import requests
from prettytable import PrettyTable

# the root api URL to be used to call the last.FM API
MAIN_API = "http://ws.audioscrobbler.com/2.0/?"
USERNAME = "agua14"
API_KEY = "94317b4722ec557c591362d8402c4808"


def getUserInfo():
    # This function will return user name along with total song plays
    getInfo = "user.getInfo"
    formatValue = 'json'

    getInfoParameters = {
        'method': getInfo,
        'user': USERNAME,
        'api_key': API_KEY,
        'format': formatValue
        }

    # Create the concatenated URL for API use
    getInfo_url = MAIN_API + urllib.parse.urlencode(getInfoParameters)
    
    # Retrieve the json data from the API
    json_user_data = ''
    while json_user_data == '':
        try:
            json_user_data = requests.get(getInfo_url).json()
        except requests.exceptions.ConnectionError:
            print("Connection refused by server")
            print("Trying again in 5 seconds")
            time.sleep(5)
            continue

    json_userName = json_user_data['user']['name']
   
    return json_userName


def getTopTracks():
    '''This function will print the user's top tracks
    based on the time period the user specifies''' 

    getTopTracksMethod = "user.getTopTracks"
    formatValue = "json"
    input_set = {'overall', '7day', '1month', '3month', '6month', '12month'}
    inputString = "\nInput the time period desired in the following format:\n'overall','7day', '1month', '3month', '6month', '12month'"

    print("\nInput the time period desired in the following format:")
    print("'overall','7day', '1month', '3month', '6month', '12month'")

    # Get user input for the time range
    timePeriod = input()

    while timePeriod not in input_set:
        timePeriod = input("\nInvalid input. Please try again\n" + inputString)
    
    getTopTracksParameters = {
        'method': getTopTracksMethod,
        'user': USERNAME,
        'period': timePeriod,
        'limit': 10,
        'api_key': API_KEY,
        'format': formatValue
        }
    
    getTopTracks_url = MAIN_API + urllib.parse.urlencode(getTopTracksParameters)

    json_track_data = ''
    while json_track_data == '':
        try:
            json_track_data = requests.get(getTopTracks_url).json()
        except requests.exceptions.ConnectionError:
            print("Connection refused by server")
            print("Trying again in 5 seconds")
            time.sleep(5)
            continue

    track_table = PrettyTable(['Title', 'Playcount'])
    track_table.align = 'l'
    for eachTrack in json_track_data['toptracks']['track']:
        track_table.add_row([eachTrack['name'], eachTrack['playcount']])
    
    print(track_table)


def getTopArtists():
    '''This function will print the user's top artists
    based on the time period the user specifies''' 

    getTopArtistsMethod = "user.getTopArtists"
    formatValue = "json"
    input_set = {'overall', '7day', '1month', '3month', '6month', '12month'}

    print("\nInput the time period desired in the following format:")
    print("'overall','7day', '1month', '3month', '6month', '12month'")

    inputString = "\nInput the time period desired in the following format:\n'overall','7day', '1month', '3month', '6month', '12month'"
    # Get user input for the time range
    timePeriod = input()

    while timePeriod not in input_set:
        timePeriod = input("\nInvalid input. Please try again\n" + inputString)
    
    getTopArtistsParameters = {
        'method': getTopArtistsMethod,
        'user': USERNAME,
        'period': timePeriod,
        'limit': 10,
        'api_key': API_KEY,
        'format': formatValue
        }

    getTopArtists_url = MAIN_API + urllib.parse.urlencode(getTopArtistsParameters)

    json_artist_data = ''
    while json_artist_data == '':
        try:
            json_artist_data = requests.get(getTopArtists_url).json()
        except requests.exceptions.ConnectionError:
            print("Connection refused by server")
            print("Trying again in 5 seconds")
            time.sleep(5)
            continue

    artist_table = PrettyTable(['Artist', 'Playcount'])
    artist_table.align = 'l'
    for eachArtist in json_artist_data['topartists']['artist']:
        artist_table.add_row([eachArtist['name'], eachArtist['playcount']])
    
    print(artist_table)

 
def displayFunctions():
    print("The following are available commands:\n")
    print("getTopArtists \t- Displays the top 10 most played artists in a specified time period")
    print("getTopTracks \t- Displays the top 10 most played songs in a specified time period")
    print("getTopAlbums \t- Displays the top 10 most played albums in a specified time period")
    print("'quit' or 'q' \t- Exits the program")
    print("--------------------------\n")


def main():
    print("--------------------------")
    print("Welcome, " + getUserInfo())
    print("--------------------------\n")

    # Get user input and keep program running until quit key is entered
    function_dict = {
        'getTopTracks': getTopTracks,
        'getTopArtists': getTopArtists,
        'q': quit, 
        'quit': quit
        }
    userInput = ''

    displayFunctions()

    while userInput != 'quit' or userInput != 'q':
        userInput = input('Input a command:')
        while userInput not in function_dict:
            userInput = input("Invalid input, please try again:")

        if userInput != 'quit' or userInput != 'q':
            function_dict[userInput]()


if __name__ == '__main__':
    main()