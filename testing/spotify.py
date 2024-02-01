import spotipy
from spotipy.oauth2 import SpotifyOAuth

# initialize
scope = "user-read-playback-position"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

artist = "Taylor Swift"
name = "exile"
track = sp.search(q="artist:" + artist + " track:" + name, type="track", limit=1)
print(track['tracks']['items'][0]['id'])
track_id = track['tracks']['items'][0]['id']

# print(sp.audio_analysis(track_id))
features = sp.audio_features(track_id)
print(features)