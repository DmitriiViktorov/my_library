from typing import Callable, Optional

from library import Library
from datetime import datetime

CANCEL_WORD = "stop"
VALID_SEARCH_TYPES = ["название", "автор", "год"]
VALID_STATUSES = ["выдана", "в наличии"]

SEARCH_TYPES_MAPPING = {
    "название": "title",
    "автор": "author",
    "год": "year"
}

def validate_input(
        prompt: str,
        error_message: str,
        validator: Callable[[str], bool],
        cancel_word: str = CANCEL_WORD
) -> Optional[str]:
    while True:
        value = input(f"{prompt} (введите '{cancel_word}' для отмены): ")
        if value.lower() == cancel_word.lower():
            return None

        if validator(value):
            return value

        print(error_message)

def is_not_empty(value: str) -> bool:
    return bool(value and value.strip())

def is_valid_year(value: str) -> bool:
    current_year = datetime.today().year
    return value.isdigit() and int(value) <= current_year

def is_positive_integer(value: str) -> bool:
    return value.isdigit() and int(value) >= 0

def is_valid_status(value: str) -> bool:
    return value in VALID_STATUSES

def is_valid_search_type(value: str) -> bool:
    return value in VALID_SEARCH_TYPES


class Librarian:
    def __init__(self):
        self.library = Library()
        self.current_year = datetime.now().year

    def add_book(self) ->  None:
        title = validate_input(
            "Введите название книги",
            "Название книги не может быть пустым.",
            is_not_empty,
        )

        if title is None:
            print("Добавление книги отменено.")
            return

        author = validate_input(
            "Введите автора книги",
            "Название книги не может быть пустым.",
            is_not_empty,
        )

        if author is None:
            print("Добавление книги отменено.")
            return

        year = validate_input(
            "Введите год издания",
            f"Год издание должен быть числом и быть не больше {self.current_year}",
            is_valid_year,
        )

        if year is None:
            print("Добавление книги отменено.")
            return

        self.library.add_book(title, author, year)

    def delete_book(self) -> None:
        delete_book_id = validate_input(
            "Введите ID книги для удаления",
            "ID книги должен быть целым числом",
            is_positive_integer,
        )

        if delete_book_id is None:
            print("Удаление книги отменено.")
            return

        self.library.delete_book(delete_book_id)

    def search_book(self) -> None:
        search_type = validate_input(
            "Введите параметр поиска (название, автор, год)",
            "Введите корректный параметр поиска - 'название', 'автор' или 'год'.",
            is_valid_search_type,
        )

        if search_type is None:
            print("Поиск книги отменен.")
            return

        search_term = validate_input(
            "Введите значение для поиска",
            "Значение для поиска не может быть пустым",
            is_not_empty,
        )
        search_type = SEARCH_TYPES_MAPPING[search_type]
        self.library.search_book(search_type, search_term)

    def display_books(self) -> None:
        self.library.display_books()

    def change_status(self) -> None:
        book_id = validate_input(
            "Введите ID книги для изменения статуса",
            "ID книги должен быть целым числом",
            is_positive_integer
        )

        if book_id is None:
            print("Изменение статуса отменено.")
            return

        new_status = validate_input(
            "Введите новый статус ('выдана', 'в наличии')",
            "Статус книги не может только 'выдана' или 'в наличии'",
            is_valid_status,
        )

        if new_status is None:
            print("Изменение статуса отменено.")
            return

        self.library.change_status(book_id, new_status)