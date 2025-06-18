#%% Show song lyrics

import api_key
import stopwords
import re
from lyricsgenius import Genius
from deep_translator import GoogleTranslator
import requests

def main():
    
    token = api_key.your_client_access_token
    genius = Genius(token)
 #   genius.verbose = False # Turn off status messages
 #   genius.remove_section_headers = True # Remove section headers (e.g. [Chorus]) from lyrics when searching
    
    def show_song_lyrics():
        
        artist = "Damiano David"
        title = "Born with a broken heart"
        
        song = genius.search_song(title, artist)
        
        pattern = r"\[.*?\]"
        match = re.search(pattern, song.lyrics)
    
        if match:
            start_index = match.start()
            cleaned_lyrics = song.lyrics[start_index:]
        else:
            cleaned_lyrics = '\n'.join(song.lyrics.split('\n')[1:])        
        print(f"\n{cleaned_lyrics}")
        
    def save_song_lyrics():
        artist = "Damiano David"
        title = "Born with a broken heart"
        
        song = genius.search_song(title, artist)
        
        pattern = r"\[.*?\]"  # matches [Verse 1], [Intro], etc.
        match = re.search(pattern, song.lyrics)
    
        if match:
            start_index = match.start()
            cleaned_lyrics = song.lyrics[start_index:]
        else:
            cleaned_lyrics = '\n'.join(song.lyrics.split('\n')[1:])
        
        file_name = f"{artist.replace(" ", "_")}-{title.replace(" ", "_")}.txt".lower()
        
        with open(file_name,'w') as f:
            f.write(cleaned_lyrics)
        
        print(f"File {file_name} created!")  
    
    def song_words_flashcards():
        artist = "Ed Sheeran"
        title = "Perfect"
        
     #   genius.remove_section_headers = False
        song = genius.search_song(title, artist)
        
        pattern = r"\[.*?\]"  # matches [Verse 1], [Intro], etc.
        match = re.search(pattern, song.lyrics)
    
        if match:
            start_index = match.start()
            cleaned_lyrics = song.lyrics[start_index:]
        else:
            cleaned_lyrics = '\n'.join(song.lyrics.split('\n')[1:])
        
        
        removed_sections = re.sub(r"\[.*?\]", "", cleaned_lyrics)
        words = re.findall(r"\b\w+\b", removed_sections.strip().lower())

        meaningful_words = [word for word in words if word not in stopwords.english]  
        words_list = list(set(meaningful_words))
        translated_list = [word.lower() for word in GoogleTranslator(source='en', target='pl').translate_batch(words_list)]

        deck_name = f"{artist} - {title}"
        requests.post("http://localhost:8765", json={
            "action": "createDeck",
            "version": 6,
            "params": {"deck": deck_name}
        })

        notes = []
        for word, translation in zip(words_list, translated_list):
            if word != translation:
                notes.append({
                            "deckName": deck_name,
                            "modelName": "Basic",
                            "fields": {
                                "Front": word,
                                "Back": translation
                            },
                            "options": {
                                "allowDuplicate": False
                            },
                        }
                    )

        response = requests.post("http://localhost:8765", json={
        "action": "addNotes",
        "version": 6,
        "params": {
            "notes": notes
        }
    })

        result = response.json().get("result", [])
        for i, res in enumerate(result):
            word = notes[i]["fields"]["Front"]
            translation = notes[i]["fields"]["Back"]
            if res is None:
                print(f"⚠️ Failed to add: {word}")
            else:
                print(f"✅ Added: {word} → {translation}")

    
    def exit_program():
        print('-'*30)
        print("Goodbye!")
        print('-'*30)
    
    
    
    actions = {
        "1": show_song_lyrics,
        "2": save_song_lyrics,
        "3": song_words_flashcards,
        "6": exit_program
    }
    
    
    while True:
        print("\n=== Lyrics Flashcard App ===")
        print("Song")
        print(" 1. Show song lyrics")
        print(" 2. Save song lyrics to a file")
        print(" 3. Generate song flashcards")
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



#ogarnac zeby dobrze jednak wczytywalo fiszki do anki
#pounifikowac funkcje
#dorobic dla albumow
#dorobic dla artystow

#langdetect
#basic gui
#Flashcard practice GUI using tkinter or streamlit
#Track known words and skip translating them again
