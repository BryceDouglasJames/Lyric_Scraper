from lyricsgenius import Genius
from dotenv import load_dotenv
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
genius.excluded_terms = ["(Remix)", "(Live)", "Single"]
names = []
try:
    with open("artists.txt") as artists:
       for line in artists:
        names.append(str(line))

    for artist in names:
        # Path 
        formatted = artist.split('\t')
        name = formatted[0]
        id = formatted[1]

        path = os.path.join("./", name) 
        if not os.path.exists(path):
           os.mkdir(path)
        os.chdir(path)      

        all_lyrics_from_artist = ""
        all_lyrics_from_album = ""
        all_lyrics_from_song = ""
        all_albums = {}


        albums_search = genius.artist_albums(id)['albums']
        for key in albums_search:
            #TODO to be safe, we should instead grab the id for the album instead of the title...
            album = str(key['name'])
            print(album)
            if not os.path.exists(album):
                os.mkdir(album)
            os.chdir(album)

            songs = genius.search_album(key['name'])
           
            #Keep for debug
            #for t in songs.to_dict()['tracks'][0]['song']:
            #    print(t)   
            #print(songs.to_dict()['tracks']['song']['lyrics'])

            album_dict = songs.to_dict()['tracks']
            for songs_info in album_dict:
                index = int(songs_info['number']) - 1
                
                temp_map = album_dict[index]['song']
                song_name = temp_map['title']
                song_lyrics = temp_map['lyrics']

                if "/" in song_name: 
                    temp = song_name.split("/")
                    new_name = ""
                    for s in temp:
                        new_name = s + "\\"
                    song_file = open(new_name + ".txt", "a")
                    song_file.write(song_lyrics)
                else:
                    song_file = open(song_name + ".txt", "a")
                    song_file.write(song_lyrics)
                song_file.close()

            all_lyrics_from_album = open("_albumall.txt" , "a")
            all_lyrics_from_album.write(songs.to_text())
            all_lyrics_from_album.close()

            os.chdir("..")
            #TODO write txt file for all the artists lyrics
    
except:
    raise RuntimeError("There was a problem when reading from artists file!")



#Search song
#song = genius.search_song("The Motto", "Drake")
#lyr = song.lyrics

#Print lyrics of song
#print(lyr)