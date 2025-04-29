# save_utils.py

import csv
import os
from datetime import datetime

from config import OUTPUT_FOLDER


def create_output_folder(subreddit_name):
    today = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join(OUTPUT_FOLDER, today, subreddit_name)
    os.makedirs(path, exist_ok=True)
    return path

  

def save_to_csv(filepath, rows, mode='w'):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, mode=mode, encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
        if mode == 'w':
            writer.writerow(["input", "output", "contexto", "idioma", "emocion", "accion"])
        for row in rows:
            writer.writerow(row)
