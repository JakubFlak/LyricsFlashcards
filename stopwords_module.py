from nltk.corpus import stopwords as nltk_stopwords


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