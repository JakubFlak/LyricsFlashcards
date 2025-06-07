#%% Show song lyrics

import api_key
import stopwords
import re
from collections import Counter
from lyricsgenius import Genius
import pandas as pd
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt

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
    
    def song_words_histogram():
        artist = "Damiano David"
        title = "Next Summer"
        
        genius.remove_section_headers = True
        song = genius.search_song(title, artist)
        
        lyrics = '\n'.join(song.lyrics.split('\n')[1:])
        words = re.findall(r"\b\w+\b", lyrics.lower())


        number_of_desired_words = 20

        meaningful_words = [word for word in words if word not in stopwords.english]  
        meaningful_words_counter = Counter(meaningful_words)
        most_frequent_meaningful_words = meaningful_words_counter.most_common(number_of_desired_words)
        
        word_frequency_df = pd.DataFrame(most_frequent_meaningful_words, columns = ['word', 'word_count'])
        word_frequency_df.sort_values(by='word_count').plot(x='word',kind='barh', title=f"{artist} - {title}\n Most Frequent Words")
        print('Plot created!')
    
    
    def song_words_cloud():
        artist = "Damiano David"
        title = "Next Summer"
        
        genius.remove_section_headers = True
        song = genius.search_song(title, artist)
        
        lyrics = '\n'.join(song.lyrics.split('\n')[1:])
        
        words = re.findall(r"\b\w+\b", lyrics.lower())


        number_of_desired_words = 20

        meaningful_words = [word for word in words if word not in stopwords.english]  
        meaningful_words_counter = Counter(meaningful_words)
        most_frequent_meaningful_words = meaningful_words_counter.most_common(number_of_desired_words)
        
        
        wc = WordCloud(background_color='black', colormap='viridis', 
                       width = 800, height = 500).generate_from_frequencies(meaningful_words_counter)
        plt.axis("off")
        plt.imshow(wc)

        print('Plot created!')
    
    
    def exit_program():
        print('-'*30)
        print("Goodbye!")
        print('-'*30)
    
    
    
    actions = {
        "1": show_song_lyrics,
        "2": save_song_lyrics,
        "3": song_words_histogram,
        "4": song_words_cloud,
        "6": exit_program
    }
    
    
    while True:
        print("\n=== Lyrics Flashcard App ===")
        print("Song")
        print(" 1. Show song lyrics")
        print(" 2. Save song lyrics to a file")
        print(" 3. Show song words histogram")
        print(" 4. Show song words cloud")
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
