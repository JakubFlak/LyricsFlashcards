#%% Show song lyrics

import api_key
from lyricsgenius import Genius

def main():
    
    token = api_key.your_client_access_token
    genius = Genius(token)
 #   genius.verbose = False # Turn off status messages
 #   genius.remove_section_headers = True # Remove section headers (e.g. [Chorus]) from lyrics when searching
    
    def show_song_lyrics():
        
        artist = "Damiano David"
        title = "Next Summer"
        
        song = genius.search_song(title, artist)
        
        lyrics = '\n'.join(song.lyrics.split('\n')[1:])
        
        print(f"\n{lyrics}")
        
    def save_song_lyrics():
        artist = "Damiano David"
        title = "Next Summer"
        
        song = genius.search_song(title, artist)
        
        lyrics = '\n'.join(song.lyrics.split('\n')[1:])
        
        file_name = f"{artist.replace(" ", "_")}-{title.replace(" ", "_")}.txt"
        
        with open(file_name,'w') as f:
            f.write(lyrics)
        
        print(f"File {file_name} created!")
    
    
    def exit_program():
        print('-'*30)
        print("Goodbye!")
        print('-'*30)
    
    
    
    actions = {
        "1": show_song_lyrics,
        "2": save_song_lyrics,
        "6": exit_program
    }
    
    
    while True:
        print("\n=== Lyrics Flashcard App ===")
        print("1. Show song lyrics")
        print("2. Save song lyrics to a file")
        print("3. Create song flashcards")
        print("6. Exit\n")
    
        choice = input("Choose an option: ").strip()
        action = actions.get(choice)
        if action:
            if choice == "6":
                action()
                break
            else:
                action()
        else:
            print('-'*30)
            print("Invalid option. Please choose 1-5.")
            print('-'*30)

if __name__ == "__main__":
    main()

#word cloud z piosenki
