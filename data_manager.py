import json
from typing import Any
from pathlib import Path


DATA_FILE = Path("books.json")

def load_books() -> list[dict[str, Any]]:
    try:
        return json.loads(DATA_FILE.read_text())
    except FileNotFoundError:
        return []

def save_books(books: list[dict[str, Any]]) -> None:
    DATA_FILE.write_text(json.dumps(books, indent=4, ensure_ascii=False))