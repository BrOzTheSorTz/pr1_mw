from src.data_collection.spotify_api import SpotifyClient
from src.data_collection.data_scraper import DataScraper
from src.utils.config import nodes_path,edges_path

def crear_grafo(max_artist,max_deep,name_artist="Melendi"):
    spotify = SpotifyClient()
    scrapper = DataScraper(spotify,max_artist,max_deep)
    scrapper.search_collaborator_deep(name_artist)


if __name__ == "__main__":

    crear_grafo(1500,2,"Melendi")
