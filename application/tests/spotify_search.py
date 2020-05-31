import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


is_on_spotify = False
total_month_listeners = 0
total_streams = 0

credentials_manager = SpotifyClientCredentials(client_id='0dfdffd7c8284cb2a592e86a6c136029',
                                               client_secret='c134357e9b2f4c019819e219f3d51d1e')

spotify_client = spotipy.Spotify(client_credentials_manager=credentials_manager)

artists = spotify_client.search('Pagode da Ofensa na Web - Com o Povão!', type='track')
if artists:
    is_on_spotify = True


# Top 10 Tracks
top_tracks = spotify_client.artist_top_tracks(artists["artists"]["items"][0]["id"])
