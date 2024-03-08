import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
import time

# initialize
scope = "user-read-playback-position user-read-recently-played user-read-currently-playing user-read-playback-state"
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
# sp = spotipy.Spotify(auth_manager=client_credentials_manager)

artist = "Taylor Swift"
name = "exile"
track = sp.search(q="artist:" + artist + " track:" + name, type="track", limit=1)
track_id = track['tracks']['items'][0]['id']

# print(sp.audio_analysis(track_id))
features = sp.audio_features(track_id)
pprint.pprint(features)

#get user
username = "95wri6c1rta5rkso9u7cin56u"
user = sp.user(username)
pprint.pprint(user)

while (True):
    song = sp.currently_playing()
    if song:
        pprint.pprint(song['item']['name'])
    else:
        print("No song playing.")
    time.sleep(1)
