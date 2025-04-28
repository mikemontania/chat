import praw

# Conexión con la API de Reddit
reddit = praw.Reddit(
    client_id='bpSZ4KKA-yaCjHU1ZqdhTw',
    client_secret='DCwjgI-rhGJDJMEqcGwNYlE0hRLpJA',
    user_agent='dataset-dialogos/0.1 by Perfect_Step_26'
)

# Obtener los 100 subreddits más populares
subreddits = reddit.subreddits.popular(limit=200)
print(subreddits)
# Diccionario de categorías
categories = {
    'Tecnología': ['python', 'learnprogramming', 'technology', 'datascience'],
    'Ciencia': ['science', 'space', 'askscience', 'biology'],
    'Entretenimiento': ['movies', 'television', 'gaming', 'music'],
    'Noticias': ['worldnews', 'news', 'politics']
}

# Función para clasificar los subreddits
def classify_subreddit(subreddit):
    for category, keywords in categories.items():
        if any(keyword.lower() in subreddit.display_name.lower() for keyword in keywords):
            return category
    return "Otros"  # Si no coincide con ninguna categoría

# Clasificar y mostrar los subreddits con su categoría
for subreddit in subreddits:
    category = classify_subreddit(subreddit)
    print(f"Nombre: {subreddit.display_name}")
    print(f"Categoría: {category}")
    print(f"URL: {subreddit.url}")
    print("-" * 40)


