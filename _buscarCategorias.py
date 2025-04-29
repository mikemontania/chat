import praw

# Conexión con la API de Reddit
reddit = praw.Reddit(
    client_id='bpSZ4KKA-yaCjHU1ZqdhTw',
    client_secret='DCwjgI-rhGJDJMEqcGwNYlE0hRLpJA',
    user_agent='dataset-dialogos/0.1 by Perfect_Step_26'
)

# Obtener los 200 subreddits más populares
subreddits = reddit.subreddits.popular(limit=200)

# Imprimir las descripciones de los subreddits para explorar sus temas
for subreddit in subreddits:
    print(f"Nombre: {subreddit.display_name}")
    print(f"Descripción: {subreddit.public_description}")
    print("-" * 40)
