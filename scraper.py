from lyricsgenius import Genius
from dotenv import load_dotenv
import os
import re

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
except:
    raise RuntimeError("There was a problem when reading from artists file!")
for artist in names:
    try:
        # Path 
        formatted = artist.split('\t')
        name = formatted[0]
        id = formatted[1]
        path = os.path.join("./", name.lower()) 
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
            if not os.path.exists(album.lower()):
                os.mkdir(album.lower())
            os.chdir(album.lower())
            songs = genius.search_album(key['name'])
        
            #Keep for debug
            #for t in songs.to_dict()['tracks'][0]['song']:
            #    print(t)   
            #print(songs.to_dict()['tracks']['song']['lyrics'])
            album_dict = songs.to_dict()['tracks']
            for songs_info in album_dict:
                try:
                    index = int(songs_info['number']) - 1
                    
                    temp_map = album_dict[index]['song']
                    song_name = temp_map['title']
                    song_lyrics_list = temp_map['lyrics'].split('\n')
                    song_lyrics_list.pop(0)
                    song_lyrics = ""
                    for line in song_lyrics_list:
                        song_lyrics += line + '\n'

                    if "/" in song_name: 
                        temp = song_name.split("/")
                        new_name = ""
                        for s in temp:
                            new_name = s + "\\"

                    
                        song_file = open(new_name.lower() + ".txt", "a")
                        song_file.write(song_lyrics.lower())
                    else:
                        temp = song_name.split("/n")
                        temp.pop(0)
                        song_file = open(song_name.lower() + ".txt", "a")
                        song_file.write(song_lyrics)
                    song_file.close()
                except:
                    continue
                
            all_lyrics_from_album = open(album.lower()+ "_album_all_songs.txt" , "a")
            all_lyrics_from_album.write(songs.to_text())
            all_lyrics_from_album.close()
            all_lyrics_from_artist += songs.to_text()
            os.chdir("..")
        artist_lyrics = open(name.lower() + "_all_songs.txt", 'a')
        artist_lyrics.write(all_lyrics_from_artist.lower())
        artist_lyrics.close()
        os.chdir("..")
        os.system("aws s3 sync \"" + name + "\" s3://artistlyricsdata/" + name + "/")
    except Exception as e:
        if e == KeyboardInterrupt:
            print('User interrupt!')

print('Done partitioning artist data!! :)')



#Search song
#song = genius.search_song("The Motto", "Drake")
#lyr = song.lyrics

#Print lyrics of song
#print(lyr)