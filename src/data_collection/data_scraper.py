from ..data_collection.spotify_api import SpotifyClient

class DataScraper:
    def __init__(self,spotify_client, max_artists=1500, max_depth=2):

        self.max_artists = max_artists
        self.max_depth = max_depth
        self.spotify = spotify_client

    def obtain_collaborators(self, name_artist):
        """Dado el nombre de un artista, nos devuelve los colaboradores de éste"""
        artist_id = self.spotify.search_artist(name_artist)
        if artist_id is None:
            raise ValueError(f"No se encontró el artista: {name_artist}")

        collaborators = {}
        albums = self.spotify.get_artist_albums(artist_id)

        for album in albums:
            tracks = self.spotify.get_album_tracks(album['id'])
            for track in tracks:
                for artist in track['artists']:
                    artist_name = artist["name"]
                    artist_id = artist["id"]
                    if artist_name != name_artist and artist_id not in collaborators:
                        collaborators[artist_id] = artist_name

        return collaborators  # Devuelve el diccionario de colaboradores


