#%% Show song lyrics

import api_key
import re
from lyricsgenius import Genius
from deep_translator import GoogleTranslator
import requests
import customtkinter as ctk
from tkinter import messagebox
import sys
from langdetect import detect
import nltk
from nltk.corpus import stopwords as nltk_stopwords

try:
    stopwords_list = nltk_stopwords.words("english")  # try to access
except LookupError:
    nltk.download("stopwords")


lang_map = {
    "Polish": "pl",
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it"
}

reverse_lang_map = {v: k for k, v in lang_map.items()}


stopwords_map = {
    "en": set(nltk_stopwords.words("english")),
    "es": set(nltk_stopwords.words("spanish")),
    "fr": set(nltk_stopwords.words("french")),
    "de": set(nltk_stopwords.words("german")),
    "it": set(nltk_stopwords.words("italian")),
}


def main():
    
    genius = Genius(api_key.your_client_access_token)

    ## HELPER FUNCTIONS

    def fetch_lyrics(artist, title):
        song = genius.search_song(title, artist)
        return song.lyrics if song else None
    
    def extract_sectioned_lyrics(lyrics):
        match = re.search(r"\[.*?\]", lyrics)
        lyrics = lyrics[match.start():] if match else lyrics
        return lyrics.strip()
    
    def extract_clean_lyrics(lyrics):
        lyrics = re.sub(r"\[.*?\]", "", lyrics)
        return lyrics  
   
   ## CORE FUNCTIONS ## 
   
    def show_lyrics():
        artist, title = get_inputs()
        output_box.delete("1.0", "end")
        output_box.insert("end", "🔍 Searching for lyrics...")
        output_box.update_idletasks()
        
        lyrics = fetch_lyrics(artist, title)
        output_box.delete("1.0", "end")
    
        if lyrics:
            sectioned = extract_sectioned_lyrics(lyrics)
            output_box.insert("end", sectioned)
        else:
            output_box.insert("end", "❌ Lyrics not found!")
        return sectioned
        
            
    def save_lyrics():
        artist, title = get_inputs()
        output_box.delete("1.0", "end")
        output_box.insert("end", "🔍 Searching for lyrics...")
        output_box.update_idletasks()
        
        lyrics = fetch_lyrics(artist, title)
        output_box.delete("1.0", "end")
    
        if lyrics:
            sectioned = extract_sectioned_lyrics(lyrics)
            file_name = f"{artist.replace(' ', '_')}-{title.replace(' ', '_')}.txt".lower()
            with open(file_name, 'w', encoding="utf-8") as f:
                f.write(sectioned)
            output_box.insert("end", f"💾 Lyrics saved to {file_name}")
        else:
            output_box.insert("end", "❌ Lyrics not found!")
    
    
    def generate_flashcards():
        artist, title = get_inputs()
        output_box.delete("1.0", "end")
        output_box.insert("end", "🔍 Searching for lyrics...\n")
        output_box.update_idletasks()
        
        lyrics = fetch_lyrics(artist, title)
    
        if lyrics:      
            clean = extract_clean_lyrics(extract_sectioned_lyrics(lyrics))
            
            try:
                source_lang = detect(clean)
            except:
                source_lang = "auto"
            
            words = re.findall(r"\b\w+\b", clean.lower())
            stopword_list = stopwords_map.get(source_lang, set())
            filtered = [w for w in words if w not in stopword_list]
            unique_words = list(set(filtered))

            target_lang_name = lang_var.get()
            target_lang_code = lang_map.get(target_lang_name, "pl")
            
            output_box.insert("end", f"🌍 Detected language: {reverse_lang_map.get(source_lang, source_lang.upper())}\n")
            output_box.insert("end", f"📖 Translating to: {target_lang_name}...\n")
            output_box.update_idletasks()
            
            try:
                translated = GoogleTranslator(source=source_lang, target=target_lang_code).translate_batch(unique_words)
            except Exception as e:
                messagebox.showerror("Translation Error", str(e))
                return
        
            deck_name = f"{artist} - {title}"
            requests.post("http://localhost:8765", json={
                "action": "createDeck",
                "version": 6,
                "params": {"deck": deck_name}
            })
        
            output_box.insert("end", "📚 Adding flashcards...\n")
            output_box.update_idletasks()
        
            notes = []
            for word, trans in zip(unique_words, translated):
                if word != trans:
                    notes.append({
                        "deckName": deck_name,
                        "modelName": "Basic",
                        "fields": {"Front": word, "Back": trans},
                        "options": {"allowDuplicate": False}
                    })
            
            try:
                response = requests.post("http://localhost:8765", json={
                    "action": "addNotes",
                    "version": 6,
                    "params": {"notes": notes}
                })
                
                if "error" in response:
                    raise Exception(response["error"])
                                
                result = response.json().get("result", [])
                success = sum(1 for r in result if r is not None)
                output_box.insert("end", f"🃏 Added {success} flashcards to Anki.\n")
                output_box.see("end")
            except Exception as e:
                output_box.delete("1.0", "end")
                output_box.insert("end", f"Failed to add flashcards.\n{e}")
            
        else:
            output_box.insert("end", "❌ Lyrics not found!")
    
        
            

    def on_closing():
        print("Closing the app...")
        app.destroy()  # Properly destroy the GUI window and end the mainloop
        sys.exit()

    def get_inputs():
        artist = artist_entry.get().strip()
        title = title_entry.get().strip()
        if not artist or not title:
            output_box.delete("1.0", "end")
            output_box.insert("end", "⚠️ Please enter both artist and song title!")
            return
        return artist, title

    # === GUI Setup === #
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    app = ctk.CTk()
    app.title("Lyrics Flashcard App")
    app.geometry("700x600")
    
    # Inputs
    artist_label = ctk.CTkLabel(app,text = "Artist Name")
    artist_label.grid(row=0, column=0,
                      padx=20, pady=0)
    
    artist_entry = ctk.CTkEntry(app, placeholder_text="")
    artist_entry.grid(row=0, column=1, columnspan=4,
                      padx=50, pady=20, sticky="ew")
    
    title_label = ctk.CTkLabel(app,text = "Song Title")
    title_label.grid(row=1, column=0,
                      padx=20, pady=20, sticky="ew")
    
    title_entry = ctk.CTkEntry(app, placeholder_text="")
    title_entry.grid(row=1, column=1, columnspan=3,
                      padx=50, pady=20, sticky="ew")
    
    # Language selection
    lang_label = ctk.CTkLabel(app, text="Target Language")
    lang_label.grid(row=2, column=0, padx=20, pady=0)
    
    lang_options = list(lang_map.keys())
    lang_var = ctk.StringVar(value="Polish")
    lang_menu = ctk.CTkOptionMenu(app, variable=lang_var, values=lang_options)
    lang_menu.grid(row=2, column=1, padx=50, pady=10, sticky="ew")
    
    
    # Output box
    output_box = ctk.CTkTextbox(app, width=660, height=250)
    output_box.insert("end", "Fill the inputs and click one of the buttons")
    #output_box.configure(state="disabled")
    output_box.grid(padx=20, pady=20,row=3, column=0, columnspan=3, sticky = "nsew")
    
    ctk.CTkButton(app, text="🎵 Show Lyrics", command=show_lyrics).grid(row=4, column=0, padx=20, pady=10, sticky="ew")
    ctk.CTkButton(app, text="💾 Save Lyrics", command=save_lyrics).grid(row=4, column=1, padx=20, pady=10, sticky="ew")
    ctk.CTkButton(app, text="🃏 Generate Flashcards", command=generate_flashcards).grid(row=4, column=2, padx=20, sticky="ew")
    
    exiting = ctk.CTkButton(app, text="Exit", command=on_closing)
    exiting.grid(row=5, column=0, padx=20, pady=20, sticky="ew", columnspan=3)
    

    app.protocol("WM_DELETE_WINDOW", on_closing)

    app.mainloop()


if __name__ == "__main__":
    main()

# jak wyswietlanie i zapisywanie to zeby nie dwa razy to
# info ze jak taki zestaw jest to override albo ze istnieje
# 
