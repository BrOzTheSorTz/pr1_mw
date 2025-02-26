import spotipy
import time
from spotipy.oauth2 import SpotifyClientCredentials
from ..utils.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET,SPOTIFY_REDIRECT_URI

class SpotifyClient:
    def __init__(self):

        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET
        ))

    def search_artist(self,artist_name):
        """Obtenemos el artista del nombre del artista pasado"""
        time.sleep(1)
        # Search for artist name
        result = self.sp.search(q='artist:' + artist_name, type='artist')
        items = result['artists']['items']
        if not items:
            return

        # Get only the first result
        artist = items[0]
        return artist


    def get_artist_albums(self, artist_id):
        """Obtiene los álbumes de un artista."""
        time.sleep(1)
        albums = []
        results = self.sp.artist_albums(artist_id, album_type="album,single")
        while results:
            albums.extend(results["items"])
            results = self.sp.next(results) if results["next"] else None
        return albums

    def get_album_tracks(self, album_id):
        """Obtiene las canciones de un álbum."""
        time.sleep(1)
        results = self.sp.album_tracks(album_id)
        return results["items"] if "items" in results else []


