import json

DATA_FILE = "books.json"

def load_books():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_books(books):
    with open(DATA_FILE, "w") as file:
        json.dump(books, file, indent=4)