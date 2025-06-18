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
    
    artist = "Ed Sheeran"
    title = "Perfect"
    
    ## HELPER FUNCTIONS
    
    def fetch_song_lyrics(artist, title):
        song = genius.search_song(title, artist)
        return song.lyrics
    
    def extract_sectioned_lyrics(lyrics):
        match = re.search(r"\[.*?\]", lyrics)
        lyrics = lyrics[match.start():] if match else lyrics
        return lyrics.strip()
    
    def extract_clean_lyrics(lyrics):
        lyrics = re.sub(r"\[.*?\]", "", lyrics)
        return lyrics  
   
   ## CORE FUNCTIONS ## 
   
    def show_song_lyrics():     
        raw_lyrics = fetch_song_lyrics(artist, title)
        sectioned_lyrics = extract_sectioned_lyrics(raw_lyrics)
        print(f"\n{sectioned_lyrics}")
        return sectioned_lyrics
        
    def save_song_lyrics():
        raw_lyrics = fetch_song_lyrics(artist, title)
        sectioned_lyrics = extract_sectioned_lyrics(raw_lyrics)
        file_name = f"{artist.replace(" ", "_")}-{title.replace(" ", "_")}.txt".lower()      
        with open(file_name,'w') as f:
            f.write(sectioned_lyrics)        
        print(f"File {file_name} created!")  
    
    def song_words_flashcards():
        raw_lyrics = fetch_song_lyrics(artist, title)
        sectioned_lyrics = extract_sectioned_lyrics(raw_lyrics)
        clean_lyrics = extract_clean_lyrics(sectioned_lyrics)
        words = re.findall(r"\b\w+\b", clean_lyrics.strip().lower())

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
                print(f"Failed to add: {word}")
            else:
                print(f"Added: {word} → {translation}")

    
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
        print("1. Show song lyrics")
        print("2. Save song lyrics to a file")
        print("3. Generate song flashcards")
        print("4. Exit\n")
    
        choice = input("Choose an option: ").strip()
        action = actions.get(choice)
        if action:
            if choice == "4":
                action()
                break
            else:
                action()
        else:
            print('-'*30)
            print("Invalid option. Please choose 1-4.")
            print('-'*30)

if __name__ == "__main__":
    main()

#langdetect
#basic gui
#Flashcard practice GUI using tkinter or streamlit
#Track known words and skip translating them again
