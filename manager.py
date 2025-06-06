#%% Show song lyrics

import api_key
from lyricsgenius import Genius

token = api_key.your_client_access_token
genius = Genius(token)
genius.verbose = False # Turn off status messages
genius.remove_section_headers = True # Remove section headers (e.g. [Chorus]) from lyrics when searching


artist = "Damiano David"
title = "Next Summer"


song = genius.search_song(title, artist)

lyrics = '\n'.join(song.lyrics.split('\n')[1:])

with open(f"{artist.replace(" ", "_")}-{title.replace(" ", "_")}.txt",'w') as f:
    f.write(lyrics)
    


#song.save_lyrics(extension = "txt")

#'title',
#'to_dict',
#'to_json',
#'to_text',


if __name__ == "__main__":
    main()

