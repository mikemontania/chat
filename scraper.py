#scraper.py

from text_utils import *
from save_utils import save_to_csv
from config import CATEGORIES, EXCLUDE_CATEGORIES, MIN_WORDS, POSTS_PER_SUBREDDIT, SENSITIVE_KEYWORDS
import os

# Función para comprobar si el texto contiene palabras clave sensibles (abuso, suicidio, etc.)
def contains_sensitive_content(text):
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in SENSITIVE_KEYWORDS)

# Función principal que procesa los subreddits
def scrape_subreddit(subreddit): 
 
    category = classify_subreddit(subreddit, CATEGORIES)

    
    # Si la categoría está en la lista de categorías a excluir, lo saltamos
    if category in EXCLUDE_CATEGORIES:
        print(f"Saltando subreddit '{subreddit.display_name}' por categoría '{category}'")
        return

    print(f"Procesando subreddit: {subreddit.display_name} (Categoría: {category})")

    output_folder = "01 descargados"  # Aquí pones la ruta relativa o absoluta de tu carpeta

    # Archivo CSV basado en el nombre de la categoría (convertido a minúsculas y sin espacios)
    filename = f"{category.replace(' ', '_').lower()}.csv"
    filepath = os.path.join(output_folder, filename)  # Guardamos el archivo dentro de la carpeta '01 descargados'
      

    all_rows = []

    for submission in subreddit.hot(limit=POSTS_PER_SUBREDDIT):
        try:
            submission.comments.replace_more(limit=0)
            
            for comment in submission.comments.list():
                input_text = clean_text(comment.body)

                # Si el comentario no es válido (menos de MIN_WORDS o marcado como eliminado), lo ignoramos
                if not is_valid_comment(input_text, MIN_WORDS):
                    continue

                # Si contiene contenido sensible, lo saltamos
                if contains_sensitive_content(input_text):
                    continue

                # Detectamos el idioma del comentario
                input_lang = detect_language(input_text)
                # Permitimos solo inglés y español
                if input_lang not in ['en', 'es']:
                    continue

                responses = []
                for reply in comment.replies:
                    output_text = clean_text(reply.body)
                    # Verificamos si la respuesta es válida
                    if is_valid_comment(output_text, MIN_WORDS):
                        # Filtramos respuestas con contenido sensible
                        if contains_sensitive_content(output_text):
                            continue
                        # Detectamos el idioma de la respuesta
                        output_lang = detect_language(output_text)
                        # Permitimos solo inglés y español
                        if output_lang not in ['en', 'es']:
                            continue
                        responses.append(output_text)

                # Añadimos la fila con el comentario original y sus respuestas
                for response in responses:
                    row = [
                        input_text,          # Comentario original
                        response,            # Respuesta
                        clean_text(submission.title),  # Título del post
                        input_lang,          # Idioma del comentario
                        detect_emotion(input_text),  # Emoción del comentario
                        detect_action(input_text)    # Acción del comentario
                    ]
                    all_rows.append(row)

        except Exception as e:
            print(f"Error procesando submission: {e}")

    # Si encontramos filas válidas, las guardamos en el archivo CSV
    if all_rows:
        save_to_csv(filepath, all_rows, mode='a')  # 'a' para agregar (no sobreescribir)
