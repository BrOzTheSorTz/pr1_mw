from src.data_collection.spotify_api import SpotifyClient
from src.data_collection.data_scraper import DataScraper


if __name__ == "__main__":
    print("he")
    spotify = SpotifyClient()
    scrapper = DataScraper(spotify)

    col=scrapper.obtain_collaborators("Quevedo")
    for key,value in col.items():
        print(value)



