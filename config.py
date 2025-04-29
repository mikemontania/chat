 
# config.py

SENSITIVE_KEYWORDS = [
    "abuse", "sexual abuse", "rape", "molest", "suicide", "kill myself", "racism", "racist",
    "violence", "murder", "assault", "harassment"
]

# Credenciales de Reddit
REDDIT_CLIENT_ID = 'bpSZ4KKA-yaCjHU1ZqdhTw'
REDDIT_CLIENT_SECRET = 'DCwjgI-rhGJDJMEqcGwNYlE0hRLpJA'
REDDIT_USER_AGENT = 'dataset-dialogos/0.1 by Perfect_Step_26'

# Configuración general
OUTPUT_FOLDER = "01_datos_descargados"
POSTS_PER_SUBREDDIT = 5 
SUBREDDITS_LIMIT = 100
MIN_WORDS = 3

# Categorías para clasificación
CATEGORIES = {
    'Tecnología': ['python', 'programming', 'datascience', 'technology', 'coding'],
    'Ciencia': ['science', 'space', 'biology', 'physics', 'research'],
    'Entretenimiento': ['movies', 'tv', 'gaming', 'music', 'books'],
    'Noticias': ['news', 'worldnews', 'politics', 'currentevents'],
    'Social': ['askreddit', 'advice', 'relationship', 'social'],
}

# Categorías que quieres evitar
EXCLUDE_CATEGORIES = []
