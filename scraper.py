from lyricsgenius import Genius
from dotenv import load_dotenv
import os

#Get environment variables
load_dotenv()

#Init lyrics genius API worker
genius = Genius(os.getenv("GENIUS_KEY"))

#Set API Settings
genius.verbose = True
genius.remove_section_headers = True
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]

#Search song
song = genius.search_song("The Motto", "Drake")
lyr = song.lyrics

#Print lyrics of song
print(lyr)