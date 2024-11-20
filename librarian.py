from curses.ascii import isdigit

from library import Library
from datetime import datetime

def validate_input(prompt, error_message, validator, cancel_word="stop"):
    while True:
        value = input(f"{prompt} (введите '{cancel_word}' для отмены): ")
        if value.lower() == cancel_word.lower():
            return None

        if validator(value):
            return value

        print(error_message)

class Librarian:
    def __init__(self):
        self.library = Library()
        self.current_year = datetime.now().year

    def add_book(self):
        title = validate_input(
            "Введите название книги",
            "Название книги не может быть пустым.",
            lambda x: bool(x.strip()),
        )

        if title is None:
            print("Добавление книги отменено.")
            return

        author = validate_input(
            "Введите автора книги",
            "Название книги не может быть пустым.",
            lambda x: bool(x.strip()),
        )

        if author is None:
            print("Добавление книги отменено.")
            return

        year = validate_input(
            "Введите год издания",
            f"Год издание должен быть числом и быть не больше {self.current_year}",
            lambda x: x.isdigit() and int(x) <= self.current_year,
        )

        if year is None:
            print("Добавление книги отменено.")
            return

        self.library.add_book(title, author, int(year))
        return f"Книга '{title}' успешно добавлена в библиотеку."

    def delete_book(self):
        delete_book_id = validate_input(
            "Введите ID книги для удаления",
            "ID книги должен быть целым числом",
            lambda x: isdigit(x) and int(x) > 0,
        )

        if delete_book_id is None:
            print("Удаление книги отменено.")
            return

        self.library.delete_book(delete_book_id)

    def search_book(self):
        search_type = validate_input(
            "Введите параметр поиска (название, автор, год)",
            "Введите параметр поиска.",
            lambda x: bool(x.strip()),
        )

        if search_type is None:
            print("Поиск книги отменен.")
            return

        elif search_type not in ['название', 'автор', 'год']:
            print("Неверный параметр поиска.")
            return

        search_term = validate_input(
            "Введите значение для поиска",
            "Значение для поиска не может быть пустым",
            lambda x: bool(x.strip()),
        )
        self.library.search_book(search_type, search_term)

    def display_books(self):
        self.library.display_books()

    def change_status(self):
        book_id = validate_input(
            "Введите ID книги для изменения статуса",
            "ID книги должен быть целым числом",
            lambda x: x.isdigit() and int(x) > 0,
        )

        if book_id is None:
            print("Изменение статуса отменено.")
            return

        new_status = validate_input(
            "Введите новый статус ('выдана', 'в наличии')",
            "Статус книги не может только 'выдана' или 'в наличии'",
            lambda x: x.strip() in ['выдана', 'в наличии'],
        )

        if new_status is None:
            print("Изменение статуса отменено.")
            return

        self.library.change_status(book_id, new_status)