# 🎵 Lyrics Flashcard App

A GUI tool that fetches lyrics using the Genius API, saves lyrics, translates vocabulary and generates Anki flashcards — all with a modern CustomTkinter interface.

## 🚀 Features

-  Fetch lyrics from any song using [Genius](https://genius.com)
-  Display and save lyrics to a `.txt` file
-  Cleanly extract only lyrical content (omitting section headers and metadata)
-  Detect language and filter stopwords
-  Translate unique words into selected target language
-  Automatically generate and add flashcards to [Anki](https://apps.ankiweb.net/)
-  Detect duplicate Anki decks and offer overwrite confirmation
-  Built with a modern dark-themed GUI using `customtkinter`

## 📸 Screenshot

```
![screenshot](https://github.com/user-attachments/assets/391d6b5e-51db-4aa2-84c4-da84bd2c77c9)

```

## 📦 Prerequisites

- **Python 3.8+**
- [Anki Desktop App](https://apps.ankiweb.net/) with [AnkiConnect](https://github.com/FooSoft/anki-connect) plugin installed and running
- A **Genius API token**  
  → Get one by creating a free account and registering an app at: https://genius.com/api-clients
- Required Python libraries (see below)


## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/JakubFlak/LyricsFlashcards.git
cd LyricsFlashcards
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Your Genius API Token

Open `api_key.py` and paste your token:

```python
your_client_access_token = 'YOUR_GENIUS_API_TOKEN'
```

## ▶️ Getting Started

Run the app:

```bash
python manager.py
```

Then:

* Enter an artist and song title
* Choose the action:

  * 🎵 Show Lyrics
  * 💾 Save Lyrics
  * 🃏 Generate Flashcards

Flashcards are added directly to your Anki desktop app!

---

## 🗂 File Structure

```
LyricsFlashcards/
├── manager.py              # Main app and GUI
├── api_key.py              # Genius API key (user-provided)
├── stopwords_module.py     # Stopword lists and language mapping
├── images/                 # screenshot for README
└── README.md               # Project documentation
```

## 📜 License

**MIT License**

## 🤝 Contributions

Pull requests and feedback are welcome!
If you use this tool, let me know — I'd love to hear how it helped your learning!

