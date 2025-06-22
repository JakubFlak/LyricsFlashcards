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
import stopwords_module

try:
    stopwords_list = nltk_stopwords.words("english")  # try to access
except LookupError:
    nltk.download("stopwords")


def main():
    
    genius = Genius(api_key.your_client_access_token)

    last_lyrics = {"artist": "", "title": "", "sectioned": ""}


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
            last_lyrics["artist"] = artist
            last_lyrics["title"] = title
            last_lyrics["sectioned"] = sectioned
            output_box.insert("end", sectioned)
        else:
            output_box.insert("end", "❌ Lyrics not found!")
        
            
    def save_lyrics():
        artist, title = get_inputs()

        output_box.delete("1.0", "end")
    
        if (last_lyrics["artist"] == artist and last_lyrics["title"] == title):
            sectioned = last_lyrics["sectioned"]
        else:
            output_box.delete("1.0", "end")
            output_box.insert("end", "🔍 Searching for lyrics...\n")
            output_box.update_idletasks()
            lyrics = fetch_lyrics(artist, title)
            
            if not lyrics:
                output_box.delete("1.0", "end")
                output_box.insert("end", "❌ Lyrics not found!")
                return
            sectioned = extract_sectioned_lyrics(lyrics)
    
        filename = f"{artist.replace(' ', '_')}-{title.replace(' ', '_')}.txt".lower()
        with open(filename, 'w', encoding="utf-8") as f:
            f.write(sectioned)
    
        output_box.delete("1.0", "end")
        output_box.insert("end", f"💾 Lyrics saved to `{filename}`")
   
    
    def generate_flashcards():
        artist, title = get_inputs()
        output_box.delete("1.0", "end")
    
        if (last_lyrics["artist"] == artist and last_lyrics["title"] == title):
            sectioned = last_lyrics["sectioned"]
        else:
            output_box.delete("1.0", "end")
            output_box.insert("end", "🔍 Searching for lyrics...\n")
            output_box.update_idletasks()
            lyrics = fetch_lyrics(artist, title)
            
            if not lyrics:
                output_box.delete("1.0", "end")
                output_box.insert("end", "❌ Lyrics not found!")
                return
            sectioned = extract_sectioned_lyrics(lyrics)     
        clean = extract_clean_lyrics(sectioned)
        
        try:
            source_lang = detect(clean)
        except:
            source_lang = "auto"
        
        words = re.findall(r"\b\w+\b", clean.lower())
        stopword_list = stopwords_module.stopwords_map.get(source_lang, set())
        filtered = [w for w in words if w not in stopword_list]
        unique_words = list(set(filtered))
        
        output_box.insert("end", f"🌍 Detected language: {stopwords_module.reverse_lang_map.get(source_lang, source_lang.upper())}\n")
        output_box.update_idletasks()
        target_lang_name = lang_var.get()
        target_lang_code = stopwords_module.lang_map.get(target_lang_name, "pl")
        
        deck_name = f"{artist} - {title} [{source_lang.upper()} → {target_lang_code.upper()}]"
        
        if deck_exists(deck_name):
            if not confirm_overwrite(deck_name):
                output_box.insert("end", "⚠️ Deck creation cancelled by user.\n")
                return
            delete_deck(deck_name)

        create_deck(deck_name)
        
        output_box.insert("end", f"📖 Translating to: {target_lang_name}...\n")
        output_box.update_idletasks()
        
        try:
            translated = GoogleTranslator(source=source_lang, target=target_lang_code).translate_batch(unique_words)
        except Exception as e:
            messagebox.showerror("Translation Error", str(e))
            return
        
        add_flashcards(deck_name, zip(unique_words, translated))

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
    
    def deck_exists(deck_name):
        response = requests.post("http://localhost:8765", json={
            "action": "deckNames",
            "version": 6
        })
        return deck_name in response.json().get("result", [])
    
    def confirm_overwrite(deck_name):
        return messagebox.askyesno(
            "Deck Exists",
            f"The deck '{deck_name}' already exists.\nDo you want to overwrite it?"
    )

    def delete_deck(deck_name):
        requests.post("http://localhost:8765", json={
            "action": "deleteDecks",
            "version": 6,
            "params": {"decks": [deck_name], "cardsToo": True}
        })


    def create_deck(deck_name):
        requests.post("http://localhost:8765", json={
            "action": "createDeck",
            "version": 6,
            "params": {"deck": deck_name}
        })
    
    
    def add_flashcards(deck_name, word_pairs):
        
        output_box.insert("end", "📚 Adding flashcards...\n")
        output_box.update_idletasks()
        
        notes = [{
            "deckName": deck_name,
            "modelName": "Basic",
            "fields": {"Front": w, "Back": t.lower()},
            "options": {"allowDuplicate": False}
        } for w, t in word_pairs if w != t.lower()]
    
        try:
            response = requests.post("http://localhost:8765", json={
                "action": "addNotes",
                "version": 6,
                "params": {"notes": notes}
            })
            result = response.json().get("result", [])
            success = sum(1 for r in result if r is not None)
            output_box.insert("end", f"🃏 Added {success} flashcards to Anki.\n")
            output_box.see("end")
        except Exception as e:
            output_box.insert("end", f"❌ Failed to add flashcards: {e}\n")
    

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
    
    lang_options = list(stopwords_module.lang_map.keys())
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
