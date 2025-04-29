import praw
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Configura tus credenciales de Reddit
reddit = praw.Reddit(
    client_id='bpSZ4KKA-yaCjHU1ZqdhTw',
    client_secret='DCwjgI-rhGJDJMEqcGwNYlE0hRLpJA',
    user_agent='dataset-dialogos/0.1 by Perfect_Step_26'
)

# Inicializa el analizador de sentimientos de VADER
analyzer = SentimentIntensityAnalyzer()

# Función para detectar emoción usando VADER
def detect_emotion(text):
    sentiment = analyzer.polarity_scores(text)
    # Usamos el puntaje de 'compound' para determinar la emoción
    if sentiment['compound'] >= 0.05:
        return "Positiva"  # Emoción positiva
    elif sentiment['compound'] <= -0.05:
        return "Negativa"  # Emoción negativa
    else:
        return "Neutral"   # Emoción neutral

# Función para detectar acción (pregunta, afirmación, exclamación)
def detect_action(text):
    # Detectar si es una pregunta
    if '?' in text:
        return "Pregunta"
    # Detectar si es una afirmación
    elif any(word in text.lower() for word in ['i am', 'i feel', 'i think', 'i believe', 'i know']):
        return "Afirmación"
    # Detectar si es una exclamación
    elif '!' in text:
        return "Exclamación"
    return "Afirmación"  # Si no es ni pregunta ni exclamación, lo asumimos como afirmación

# Lista de subreddits a recorrer
subreddits = [
     "Home",
    "AskReddit",
     "NoStupidQuestions",
          "BaldursGate3", 
          "facepalm",
           "interestingasfuck",
              "Damnthatsinteresting",
              "LivestreamFail", 
    "Palworld",
    "relationships",
    "CasualConversation",
    "offmychest"
]

# Función para limpiar texto y evitar caracteres no deseados
def clean_text(text):
    return text.replace('\n', ' ').replace('\r', ' ').strip()

# Crear archivo CSV para guardar los datos
with open('reddit_conversaciones.csv', mode='w', encoding='utf-8', newline='') as csv_file:
    writer = csv.writer(csv_file)
    
    # Cabecera del CSV
    writer.writerow(["input", "output", "contexto", "idioma", "emocion", "accion"])

    for sub_name in subreddits:
        subreddit = reddit.subreddit(sub_name)
        print(f"Procesando subreddit: {sub_name}")

        for submission in subreddit.hot(limit=5):
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                for reply in comment.replies:
                    # Detectamos la emoción y la acción para el input y el output
                    input_emotion = detect_emotion(comment.body)
                    output_emotion = detect_emotion(reply.body)
                    input_action = detect_action(comment.body)
                    output_action = detect_action(reply.body)

                    # Limpiar texto antes de escribirlo en el CSV
                    cleaned_input = clean_text(comment.body)
                    cleaned_output = clean_text(reply.body)
                    cleaned_context = clean_text(submission.title)

                    # Guardamos la conversación en el CSV
                    writer.writerow([
                        cleaned_input,
                        cleaned_output,
                        cleaned_context,
                        "en",               # Idioma (por defecto en inglés)
                        input_emotion,      # Emoción del comentario
                        input_action,       # Acción del comentario
                    ])
                    writer.writerow([
                        cleaned_output,
                        cleaned_input,
                        cleaned_context,
                        "en",               # Idioma (por defecto en inglés)
                        output_emotion,     # Emoción de la respuesta
                        output_action,      # Acción de la respuesta
                    ])
