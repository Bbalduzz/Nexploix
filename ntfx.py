from utils import exploit
import json
import requests
from bs4 import BeautifulSoup
from colorama import Fore

class NetflixError(Exception):
    pass
class NetflixItemTypeError(NetflixError):
    """Netflix ID is not valid for object."""
class Movie:
    def __init__(self, netflix_id, fetch_instantly=True):
        self.netflix_id = netflix_id
        self.name = None
        self.description = None
        self.genre = None
        self.image_url = None
        self.metadata = None

        if fetch_instantly:
            self.fetch()
            self.is_fetched = True
        else:
            self.is_fetched = False

    def __str__(self):
        return self.name or self.netflix_id

    def __repr__(self):
        return "<Netflix Movie: {name}>".format(name=self.__str__())

    def fetch(self):
        url = "https://www.netflix.com/it-it/title/{netflix_id}".format(netflix_id=self.netflix_id)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        metadata_script_tag = soup.find("script", type="application/ld+json")
        metadata = json.loads(metadata_script_tag.string)
        if metadata["@type"] != "Movie":
            raise NetflixItemTypeError()

        self.name = metadata["name"]
        self.description = metadata["description"]
        self.genre = metadata["genre"]
        self.image_url = metadata["image"]

        self.metadata = metadata


class TVShow:
    def __init__(self, netflix_id, fetch_instantly=True):
        self.netflix_id = netflix_id
        self.name = None
        self.description = None
        self.genre = None
        self.image_url = None
        self.metadata = None

        if fetch_instantly:
            self.fetch()
            self.is_fetched = True
        else:
            self.is_fetched = False

    def __str__(self):
        return self.name or self.netflix_id

    def __repr__(self):
        return "<Netflix TVShow: {name}>".format(name=self.__str__())

    def fetch(self):
        url = "https://www.netflix.com/it-it/title/{netflix_id}".format(netflix_id=self.netflix_id)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        metadata_script_tag = soup.find("script", type="application/ld+json")
        metadata = json.loads(metadata_script_tag.text)
        if metadata["@type"] != "TVSeries":
            raise NetflixItemTypeError()

        self.name = metadata["name"]
        self.description = metadata["description"]
        self.genre = metadata["genre"]
        self.image_url = metadata["image"]

        self.metadata = metadata

if __name__ == '__main__':
    dl = exploit.AltadefinizioneExploit()
    tag = input(f'{Fore.YELLOW}●{Fore.RESET} Enter netflix url: ').split('?')[0].removeprefix('https://www.netflix.com/watch/')
    movie = Movie(tag)
    slug,media = dl.search_content(movie.name)
    dl.download(f'https://altadefinizionecommunity.{dl.updated_domain}/p/{slug}')