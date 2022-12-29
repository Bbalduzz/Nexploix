from utils import exploit
import json
import requests
from bs4 import BeautifulSoup

from colorama import Fore
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich import box, print

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

    def fetch(self):
        url = f"https://www.netflix.com/it-it/title/{self.netflix_id}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        metadata_script_tag = soup.find("script", type="application/ld+json")
        metadata = json.loads(metadata_script_tag.string)
        if metadata["@type"] != "Movie":
            raise NetflixItemTypeError()

        self.url = metadata["url"]
        self.content_rating = metadata["contentRating"]
        self.director = metadata["director"][0]["name"]
        self.actors = metadata["actors"]
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

    def fetch(self):
        url = f"https://www.netflix.com/it-it/title/{self.netflix_id}"
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
    matches, slugs ,types = dl.search_content(movie.name)

    # ui #
    def match_panel(matches, types) -> Panel:
        table = Table(expand=True, box=box.SIMPLE_HEAD)
        table.add_column("ID",justify="right", style="cyan", no_wrap=True)
        table.add_column('Type', justify="right", style="white")
        table.add_column("Title", justify="center")
        for i,match in enumerate(matches):
            table.add_row(str(i), types[i], match)
        displayed_matches = Panel(table)
        return displayed_matches

    def wich_lang(lang) -> Panel:
        used_lang = Panel(
            Align.center(Text(f'{lang}')), 
            box=box.ROUNDED,
        )
        return used_lang

    def movie_desc() -> Layout:
        def movie_layout():
            layout = Layout(name="desc")
            layout.split(
                Layout(name="main", ratio=1)
            )
            layout["main"].split(
                Layout(name="url", size=3),
                Layout(name="description"),
                Layout(name="contentrating", size=3),
                Layout(name="director", size=4),
                Layout(name="cast"),
            )
            cast = ' '.join(f'{actor["name"]},' for actor in movie.actors)
            layout["url"].update(Panel(Align.center(Text(f'{movie.url}')), box=box.ROUNDED, title="[b red] url",))
            layout["description"].update(Panel(Align.center(Text(f'{movie.description}')), box=box.ROUNDED, title="[b red] description"))
            layout["contentrating"].update(Panel(Align.center(Text(f'{movie.content_rating}')), box=box.ROUNDED, title="[b red] content rating"))
            layout["director"].update(Panel(Align.center(Text(f'{movie.director}')), box=box.ROUNDED, title="[b red] director"))
            layout["cast"].update(Panel(Align.center(Text(f'{cast}')), box=box.ROUNDED, title="[b red] cast"))

            return layout
        movie_desc = Panel(
            movie_layout(),
            box=box.ROUNDED,
            padding=(1, 2),
            border_style="blue",
        )
        return movie_desc

    def MakeLayout() -> Layout:
        layout = Layout(name="root")
        layout.split(
            Layout(name="main", ratio=1),
        )
        layout["main"].split_row(
            Layout(name="ita", ratio=2),
            Layout(name="infos"),
        )
        layout["ita"].split(
            Layout(name="language1", size=3),
            Layout(name="content1"),
        )
        layout["infos"].split(
            Layout(name="move_title", size=3),
            Layout(name="movie_description"),
        )
        return layout

    layout = MakeLayout()
    layout["language1"].update(wich_lang("italian"))
    layout["content1"].update(match_panel(matches,types))
    layout["move_title"].update(Panel(Align.center(Text(f'{movie.name}')), box=box.ROUNDED, title="[b red] Movie"))
    layout["movie_description"].update(movie_desc())
    print(layout)
    # end ui #
    
    c = int(input(f'{Fore.YELLOW}●{Fore.RESET} Enter ID: '))
    dl.download(f'https://altadefinizionecommunity.{dl.updated_domain}/p/{slugs[c]}')
