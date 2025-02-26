import os.path

from ..data_collection.spotify_api import SpotifyClient
import pandas as pd
from ..utils.config import nodes_path,edges_path

class DataScraper:
    def __init__(self,spotify_client, max_artists=5, max_depth=2):

        self.max_artists = max_artists
        self.artists_processed = 0
        self.max_depth = max_depth
        self.spotify = spotify_client

    def obtain_collaborators(self, name_artist):
        """Dado el nombre de un artista, nos devuelve los colaboradores de éste"""
        artist = self.spotify.search_artist(name_artist)
        # Artist data
        artist_data = {
            'id': artist["id"],
            'label': artist['name'],
            'followers': artist['followers']['total'],
            'genres': ', '.join(artist['genres']),
            'popularity': artist['popularity'],
            'image_url': artist['images'][0]['url'] if artist['images'] else None
        }
        # Guardamos el artista en el fichero
        self.send_nodes_file(artist_data)

        collaborators = {}
        albums = self.spotify.get_artist_albums(artist_data["id"])

        for album in albums:
            tracks = self.spotify.get_album_tracks(album['id'])
            for track in tracks:
                for artist in track['artists']:
                    artist_name = artist["name"]
                    artist_id = artist["id"]
                    if artist_name != name_artist and artist_id not in collaborators:
                        collaborators[artist_id] = artist_name

        # Guardamos los datos de los colaboradores en el fichero de aristas
        self.send_edges_file(artist_data['id'],collaborators)

        return collaborators  # Devuelve el diccionario de colaboradores

    def send_edges_file(self,artist_id,collaborators):
        """Guardamos en un fichero csv con quien colabora un artista"""
        if not os.path.exists(edges_path):
            columns = ['source','target']
            df = pd.DataFrame(columns=columns)  # DataFrame vacío con los nombres de las columnas
            df.to_csv(edges_path, index=False)  # Guardamos el archivo vacío con los encabezados

        edges_df = pd.read_csv(edges_path)
        for id,name in collaborators.items():
            new_df = pd.DataFrame([{'source':artist_id,'target':id}])
            edges_df = pd.concat([edges_df,new_df],ignore_index=True)

        edges_df.to_csv(edges_path,index=False)

    def send_nodes_file(self, artist_data):
        """ Guardar datos del artista en el fichero nodo"""
        if not os.path.exists(nodes_path):
            # Crea el archivo inicial con las columnas necesarias
            columns = ['id', 'label', 'followers', 'genres', 'popularity', 'image_url']
            df = pd.DataFrame(columns=columns)  # DataFrame vacío con los nombres de las columnas
            df.to_csv(nodes_path, index=False)  # Guardamos el archivo vacío con los encabezados

        # Lee el archivo CSV existente
        nodes_df = pd.read_csv(nodes_path)

        # Comprueba si el artista ya está incluido en el CSV
        if artist_data['id'] not in nodes_df['id'].values:  # Evitamos duplicados
            # Añade el nuevo artista respetando el formato de columnas
            new_artist_df = pd.DataFrame([artist_data])  # Convierte el diccionario en un DataFrame
            nodes_df = pd.concat([nodes_df, new_artist_df], ignore_index=True)  # Concatenamos

            # Guardamos nuevamente el DataFrame actualizado
            nodes_df.to_csv(nodes_path, index=False)

    def deep_search(self,name_artist, deep=0, visited=None):
        print(f"Searching {name_artist}.... Deep: {deep}, Num Artist: {self.artists_processed}")
        self.artists_processed += 1
        if visited is None:
            visited = set()

        if deep >= self.max_depth or self.artists_processed >= self.max_artists or name_artist in visited:
            return

        visited.add(name_artist)
        collaborators = self.obtain_collaborators(name_artist)

        for _, name in collaborators.items():
            self.deep_search(name, deep + 1, visited)


    def search_collaborator_deep(self,name_artist):
        artist = self.spotify.search_artist(name_artist)
        self.deep_search(artist['name'])