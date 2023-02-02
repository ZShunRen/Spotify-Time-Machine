Spotify-Time-Machine
Description
A script in Python 3 that when provided with a user's credentials, as well as a date all the way back till 04/08/1958, will scrap Billboard's Hot 100(https://www.billboard.com/charts/hot-100/) and save the song in a txt file, 'top_songs.txt'. It will then save these songs in a spotify playlist in the format "Billboard Top 100: YY-MM-DD". You will be prompted to enter urls in the format of https://example.com/{KEY} which will be opened on your browser. Just copy and paste it in the terminal window.
Getting Started
Dependencies
BeautifulSoup 4, Spotipy
Executing program
Just run the .py file and the script should start.
Help
Edit the main.py file and insert your client secret and id values in the fields in the code. Can be found @ https://developer.spotify.com/dashboard. You need to create an app after logging into developer.spotify, and then enter the two values displayed under client secret and client id.
Make sure to include https://example.com as the redirect url or you can use something else, it doesn't matter.
Acknowledgements
Created as a project for Day 46 of the 100 Days of Code by Dr Angela Yu: https://www.udemy.com/course/100-days-of-code/
Relied only on hints from the course videos, documentation of BS4 and Spotipy, ChatGPT and Google to complete this project.
