from dotenv import load_dotenv
from lyricsgenius import Genius
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

#Get environment variables
load_dotenv()

#Init lyrics genius API worker
genius = Genius(os.getenv("GENIUS_KEY"))

#Set API Settings
genius.timeout = 60
genius.verbose = True
genius.remove_section_headers = True
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]

# Open up safari browser instance
driver = webdriver.Safari()
driver.get("https://genius.com/verified-artists")

# Scroll alllll the way down to get a full set of artists
load_counter = 0
while(load_counter < 1):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
    time.sleep(1)
    load_counter+=1

# Create lists of links where artist name is held
links = driver.find_elements(By.CLASS_NAME, "login")

# Write artists names into a txt file and close it
f = open("artists.txt", "a")

# Go through each artist and get tuple their name and id to a txt file
for artist in links:
    id = genius.search(artist.text)['hits'][0]["result"]['primary_artist']['id']
    f.write(artist.text + '\t' + str(id) + '\n')
f.close()


#This only grabs the artists upong the forst request. We need something that can dynamically load more artists...
'''
import requests
from bs4 import BeautifulSoup
page = requests.get("https://genius.com/verified-artists")
soup = BeautifulSoup(page.content, 'html.parser')
names = []
artists = soup.find_all('a',{"class":"login"})
for artist in artists:
    names.append(artist.get_text())
print(names)'''