from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
#known issues: 1.problems with accuracy of songs found 2.doesn't work with collaborating covers of existing songs
#1. There's an accuracy issue with songs with collaborating artists, where we have to remove the other artists name if not spotify cannot find the track
#has been fixed with two methods, recursive_remove_collab_words and remove_collab_word
class TopSongsCompiler():
    def __init__(self):
        self.date=None
        #self.client_id="<YOUR CLIENT ID>" 
        #self.client_secret="<YOUR CLIENT SECRET>"
        self.redirect_url="https://example.com"
        self.track_ids=[]
        self.top_songs={}
        self.collab_words=['Featuring',',','&','With','X']
        #can modify the collab words list to include more common terms
        self.artist_names=[]
    def start_request(self):
        """Starts the request for the songs, by saving it to a txt then adding a playlist to the user's account """
        self.date=input("Which date would you want to return back to? in YYYY-MM-DD format:")
        reply=requests.get(url=f"https://billboard.com/charts/hot-100/{self.date}/")
        soup=BeautifulSoup(reply.text,"html.parser")
        unrefined=soup.find_all(name="div", class_="o-chart-results-list-row-container")
        for element in unrefined:
            title=element.find(name="h3", id="title-of-a-story")
            working_title=(title.getText()).strip()
            unrefined_name=title.find_next_sibling('span')
            artist_name=(unrefined_name.getText()).strip()
            self.artist_names.append(artist_name)
            artist=self.recursive_remove_collab_words(artist_name)
            self.top_songs[working_title]=artist
        with open("top_songs.txt","w") as f:
            for song,artist in self.top_songs.items():
                f.write(f"artist:{artist} track:{song}\n")
        self.find_track_ids()
    def recursive_remove_collab_words(self,artist):
        """Uses a while condition and a variable sum to make sure that artists who have no collab words do not get looped and added again"""
        artist_collab_word=True
        sum=0
        while artist_collab_word:
            for word in self.collab_words:
                #the if will trigger if any of the words in the list are found in the string, to prevent repeated looping
                if any(word in artist for word in self.collab_words):
                    artist=self.remove_collab_word(word,artist)
                    sum+=1
                elif sum==0:
                    #to skip over artist names with no collaborations
                    artist_collab_word=False
                elif sum>=len(self.collab_words):
                    artist_collab_word=False
                    #to allow the program to exit the while loop when there are no more collab words to remove
                else:
                    #works together with the above condition
                    sum+=1
        return artist
    def remove_collab_word(self,word,artist):
        """Removes the collab word from the artist name to allow spotify to accurately search for the track"""
        try:
            artist_1,artist_2=artist.split(word)
            return artist_1
        except ValueError:
            return artist
    def find_track_ids(self):
        """Searches for the track id of the song and then returns the number 1 search result, which is often the right one"""
        scope = "user-library-read"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id,
        client_secret=self.client_secret,
        redirect_uri=self.redirect_url,
        scope=scope))
        for song, artist in self.top_songs.items():
            try:
                result=sp.search(q=f"{artist} {song}",type="track",limit=1)
                self.track_ids.append(result['tracks']['items'][0]['uri'])
            except IndexError:
                print(f"{artist}, {song} not found.")
        self.add_tracks()
    def create_playlist(self):
        """Creates a public playlist that contains all of the songs"""
        scope = "playlist-modify-public"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id,
        client_secret=self.client_secret,
        redirect_uri=self.redirect_url,
        scope=scope))
        user_id=sp.me()['id']
        playlist=sp.user_playlist_create(user=user_id,name=f"Billboard Top 100 {self.date}")
        playlist_id=playlist['id']
        return playlist_id
    def add_tracks(self):
        scope = 'playlist-modify-public'
        redirect_url="https://example.com"
        sp= spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id,
        client_secret=self.client_secret,
        redirect_uri=redirect_url,
        scope=scope))
        sp.playlist_add_items(playlist_id=self.create_playlist(),items=self.track_ids)
tp=TopSongsCompiler()
tp.start_request()