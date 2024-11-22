from dataclasses import dataclass
from enum import Enum
from typing import Any

import data_manager

BOOK_STATUS = {
    0: "выдана",
    1: "в наличии"
}

class BookStatus(Enum):
    BORROWED = "выдана"
    AVAILABLE = "в наличии"

@dataclass
class Book:
    id: str
    title: str
    author: str
    year: int
    status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Book':
        return cls(**data)


class Library:
    def __init__(self):
        self.books: list[Book] = [Book.from_dict(book) for book in data_manager.load_books()]

    @staticmethod
    def print_books(books: list[Book]) -> None:
        if not books:
            print("Книги не найдены.")
            return

        print(f"{'ID':<5}{'Название':<25}{'Автор':<25}{'Год':<10}{'Статус':<10}")
        print("-" * 75)
        for book in books:
            print(f"{book.id:<5}{book.title:<25}{book.author:<25}{book.year:<10}{book.status:<10}")

    def _save_books(self) -> None:
        data_manager.save_books([book.to_dict() for book in self.books])

    def add_book(self, title: str, author: str, year: str) -> None:
        book_id = "1" if not self.books else str(max(int(book.id) for book in self.books) + 1)

        new_book = Book(
            id=book_id,
            title=title,
            author=author,
            year=int(year),
            status=BookStatus.AVAILABLE.value
        )
        self.books.append(new_book)
        self._save_books()

        print(f"\nКнига '{new_book.title}' добавлена в библиотеку.")

    def delete_book(self, book_id: str) -> None:
        book = next((book for book in self.books if book.id == book_id), None)

        if not book:
            print(f"Книга с id {book_id} не найдена.")
            return

        confirm = input(f"Вы уверены, что хотите удалить книгу {book.title} с ID {book_id} (да/нет): ")
        if confirm.lower() in ('да', 'yes', 'д', 'y'):
            self.books.remove(book)
            self._save_books()
            print(f"\nКнига с id {book_id} удалена из библиотеки.")
            return
        else:
            print(f"Удаление книги {book.title} отменено.")

    def search_book(self, search_type: str, search_term: str) -> None:
        search_book_result = [
            book for book in self.books
            if search_term.lower() in str(getattr(book, search_type)).lower()
        ]
        self.print_books(search_book_result)

    def display_books(self) -> None:
        if not self.books:
            print("В данный момент в библиотеке нет ни одной книги.")
            return
        self.print_books(self.books)

    def change_status(self, book_id: str, new_status: str) -> None:
        book = next((book for book in self.books if book.id == book_id), None)
        if not book:
            print(f"Книга с id {book_id} не найдена.")
            return

        if book.status == new_status:
            print(f"У книги {book.title} уже установлен статус '{book.status}' в настоящий момент.")
            return

        book.status = new_status
        self._save_books()
        print(f"Статус книги {book.title} изменен на {new_status}")