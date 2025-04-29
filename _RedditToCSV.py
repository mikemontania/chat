import praw
import csv

# Configura tus credenciales
reddit = praw.Reddit(
    client_id='bpSZ4KKA-yaCjHU1ZqdhTw',
    client_secret='DCwjgI-rhGJDJMEqcGwNYlE0hRLpJA',
    user_agent='dataset-dialogos/0.1 by Perfect_Step_26'
)

# Lista de subreddits a recorrer
subreddits = ['AskReddit', 'AskScience', 'AskHistorians', 'AskWomen', 'AskMen', 'AskAcademia']

# Abrir el archivo CSV para escritura
with open('reddit_dialogos.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # Escribir la fila de encabezados
    writer.writerow(['Subreddit', 'Título del Post', 'Comentario'])

    # Recorrer cada subreddit
    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        # Obtener los 5 posts más populares
        for submission in subreddit.hot(limit=5):
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                # Escribir los datos en el archivo CSV
                writer.writerow([subreddit_name, submission.title, comment.body])
