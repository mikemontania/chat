import praw
import csv
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Conexión con la API de Reddit
reddit = praw.Reddit(
    client_id='bpSZ4KKA-yaCjHU1ZqdhTw',
    client_secret='DCwjgI-rhGJDJMEqcGwNYlE0hRLpJA',
    user_agent='dataset-dialogos/0.1 by Perfect_Step_26'
)

# Obtener los 100 subreddits más populares
subreddits = list(reddit.subreddits.popular(limit=100))

# Diccionario de categorías
categories = {
    'Tecnología': ['python', 'programming', 'programming', 'datascience', 'technology', 'coding'],
    'Ciencia': ['science', 'space', 'biology', 'physics', 'research'],
    'Entretenimiento': ['movies', 'tv', 'gaming', 'music', 'books'],
    'Noticias': ['news', 'worldnews', 'politics', 'currentevents'],
    'Social': ['askreddit', 'advice', 'relationship', 'social']
}

# Función para clasificar los subreddits
def classify_subreddit(subreddit):
    description = subreddit.public_description.lower()
    for category, keywords in categories.items():
        if any(keyword in description for keyword in keywords):
            return category
    return "Otros"  # Si no coincide con ninguna categoría

# Inicializar analizador VADER
analyzer = SentimentIntensityAnalyzer()

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
    elif any(phrase in text_lower for phrase in ['i am', 'i feel', 'i think', 'i believe', 'i know']):
        return "Afirmación"
    elif '!' in text:
        return "Exclamación"
    return "Afirmación"

def clean_text(text):
    return text.replace('\n', ' ').replace('\r', ' ').strip()

def clean_and_filter_comment(comment):
    # Filtrar comentarios eliminados
    if '[removed]' in comment.body or '[deleted]' in comment.body:
        return None
    return clean_text(comment.body)

# Crear carpeta si no existe
output_folder = "01 datos_descargados"
os.makedirs(output_folder, exist_ok=True)

# Procesar cada subreddit
for subreddit in subreddits:
    category = classify_subreddit(subreddit)
    print(f"Procesando subreddit: {subreddit.display_name}")

    # Nombre de archivo para este subreddit
    filename = f"{output_folder}/{subreddit.display_name}.csv"
    
    with open(filename, mode='w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Cabecera del CSV
        writer.writerow(["input", "output", "contexto", "idioma", "emocion", "accion"])

        for submission in subreddit.hot(limit=5):
            submission.comments.replace_more(limit=0)

            for comment in submission.comments.list():
                # Limpiar y filtrar el comentario
                input_text = clean_and_filter_comment(comment)
                if not input_text:
                    continue  # Si el comentario fue filtrado, omitirlo

                # Procesar las respuestas
                responses = []
                for reply in comment.replies:
                    output_text = clean_and_filter_comment(reply)
                    if output_text:
                        # Obtener emociones y acciones para cada respuesta
                        input_emotion = detect_emotion(input_text)
                        input_action = detect_action(input_text)
                        responses.append((output_text, input_emotion, input_action))
                
                # Si hay respuestas, almacenarlas
                if responses:
                    for response in responses:
                        output_text, input_emotion, input_action = response
                        writer.writerow([
                            input_text,
                            output_text,
                            clean_text(submission.title),
                            "en",
                            input_emotion,
                            input_action
                        ])
