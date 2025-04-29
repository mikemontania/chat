# text_utils.py

from langdetect import detect, LangDetectException
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def clean_text(text):
    return text.replace('\n', ' ').replace('\r', ' ').strip()

def is_valid_comment(text, min_words):
    if not text or text in ['[removed]', '[deleted]']:
        return False
    if len(text.split()) < min_words:
        return False
    return True

def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except LangDetectException:
        return "unknown"

def detect_emotion(text):
    sentiment = analyzer.polarity_scores(text)
    if sentiment['compound'] >= 0.05:
        return "Positiva"
    elif sentiment['compound'] <= -0.05:
        return "Negativa"
    else:
        return "Neutral"

def detect_action(text):
    text_lower = text.lower()
    if '?' in text:
        return "Pregunta"
    elif '!' in text:
        return "Exclamación"
    elif any(phrase in text_lower for phrase in ['i am', 'i feel', 'i think', 'i believe', 'i know']):
        return "Afirmación"
    return "Afirmación"
  
def classify_subreddit(subreddit, categories):
    desc = (subreddit.public_description + " " + subreddit.display_name).lower()
    for category, keywords in categories.items():
        if any(keyword in desc for keyword in keywords):
            return category
    return "Otros"

