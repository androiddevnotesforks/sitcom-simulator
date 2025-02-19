import requests
from bs4 import BeautifulSoup
import random
import os
from enum import Enum
import atexit
import tempfile

class MusicCategory(Enum):
    UPBEAT='upbeat'
    EPIC='epic'
    HORROR='horror'
    ROMANTIC='romantic'
    COMEDY='comedy'
    WORLD='world'
    SCORING='scoring'
    ELECTRONIC='electronic'
    MISC='misc'

    @classmethod
    def values(cls):
        return [str(member.value) for name, member in cls.__members__.items()]

def download_random_music(category: MusicCategory) -> str | None:
    # Send a GET request to the website
    url = f"https://freepd.com/{category.value}.php"
    response = requests.get(url)

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the song rows in the table
    song_rows = soup.find_all("tr")[1:]

    # Randomly select a song
    selected_song = random.choice(song_rows)

    # Extract song information
    song_name = selected_song.find("b").text
    download_link = "https://freepd.com" + selected_song.find("a", class_="downloadButton")["href"]

    return download_file(download_link)

def download_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Get the file name from the URL
        file_extension = url.split('.')[-1]
        music_title = url.split('/')[-1].split('.')[0]
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix=f'.{file_extension}', delete=False)
        with open(temp_file.name, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {music_title} successfully.")
        # Register the cleanup function to delete the file at exit
        atexit.register(os.remove, temp_file.name)
        return temp_file.name
    else:
        print("Failed to download the file.")
        return None