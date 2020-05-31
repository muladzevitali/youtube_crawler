import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from source.configuration import app_config


class SpotifyApi:
    def __init__(self):
        credentials_manager = SpotifyClientCredentials(client_id=app_config.SPOTIFY_CLIENT_ID,
                                                       client_secret=app_config.SPOTIFY_CLIENT_SECRET)

        self.client = spotipy.Spotify(client_credentials_manager=credentials_manager)

    def search_artist(self, name: str) -> dict:
        """Search artist by name. Currently no logic just gets the first artist from that name"""
        artists = self.client.search(name, type='artist')

        if artists['artists']['total']:
            return artists["artists"]["items"][0]

        return {}

    def artist_top_tracks(self, artist_id: str):
        """Get top 10 track of the artist"""
        # Top 10 Tracks in US
        try:
            return self.client.artist_top_tracks(artist_id=artist_id)

        except spotipy.client.SpotifyException:
            return
