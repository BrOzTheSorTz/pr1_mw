import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ..utils.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

class SpotifyClient:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI
        ))

    def get_artist_top_tracks(self, artist_id, country="US"):
        """Obtiene las 10 canciones más populares de un artista."""
        results = self.sp.artist_top_tracks(artist_id, country=country)
        return results["tracks"] if "tracks" in results else []

    def get_artist_albums(self, artist_id):
        """Obtiene los álbumes de un artista."""
        albums = []
        results = self.sp.artist_albums(artist_id, album_type="album")
        while results:
            albums.extend(results["items"])
            results = self.sp.next(results) if results["next"] else None
        return albums

    def get_album_tracks(self, album_id):
        """Obtiene las canciones de un álbum."""
        results = self.sp.album_tracks(album_id)
        return results["items"] if "items" in results else []


    
    def get_album_collaborator(self,album):
        """Obtiene los colaboradores en formato id-name dado un album"""
        collaborators = {}
        album_aux = self.sp.album(album['uri'])                          #        obtengo mediante su URI (identificador) toda la información del album
        
        tracks = album_aux['tracks']['items']                       #        para ese album obtengo su listado de canciones
        for track in tracks:                                        #   BUCLE: Para cada canción del listado
            for artist in track['artists']:                         #       BUCLE: Para cada artista del listado de artistas de cada canción
                if artist['id'] not in collaborators.keys():
                    collaborators[artist['id']]=artist['name']

        return collaborators


