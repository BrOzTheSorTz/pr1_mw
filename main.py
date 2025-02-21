from src.data_collection.spotify_api import SpotifyClient
from src.data_collection.data_scraper import DataScraper


if __name__ == "__main__":

    spotify = SpotifyClient()
    max_artist = 1500
    max_deep = 4
    scrapper = DataScraper(spotify,max_artist,max_deep)

    scrapper.search_collaborator_deep("Lola Indigo")



