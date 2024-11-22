from dataclasses import dataclass
from enum import Enum
from typing import Any

from data_manager import DataManager


class BookStatus(Enum):
    BORROWED = "выдана"
    AVAILABLE = "в наличии"


@dataclass
class Book:
    """
    Класс Книга для упрощения получения (from_dict) и передачи (to_dict) данных о книгах.
    """
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
    """
    Класс Библиотека для обработки данных о книгах и взаимодействия с менеджером данных
    """
    def __init__(self, datamanager: DataManager = DataManager()):
        self.data_manager = datamanager
        self.books: list[Book] = [Book.from_dict(book) for book in self.data_manager.load_books()]

    @staticmethod
    def print_books(books: list[Book]) -> None:
        """Выводит на экран информацию о каждой книге из полученного списка"""
        if not books:
            print("Книги не найдены.")
            return

        print(f"{'ID':<5}{'Название':<25}{'Автор':<25}{'Год':<10}{'Статус':<10}")
        print("-" * 75)
        for book in books:
            print(f"{book.id:<5}{book.title:<25}{book.author:<25}{book.year:<10}{book.status:<10}")

    def _save_books(self) -> None:
        """Передает список всех хранящихся в библиотеке книг для дальнейшей обработки. """
        self.data_manager.save_books([book.to_dict() for book in self.books])

    def add_book(self, title: str, author: str, year: str) -> None:
        """
        Сохраняет данные о новой книге, присваивает новый уникальный ID и устанавливает статус 'в наличии'.
        :param title: Название книги
        :param author: Автор книги
        :param year: Год издания
        """
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
        """
        Удаляет книгу с переданным параметром ID.
        В случае, если книга есть в библиотеке - просит подтверждения на удаление и удаляет её.
        :param book_id: ID книги, которую надо удалить.
        """
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
        """
        Производит поиск книг по выбранному параметру поиска и значениям для поиска.
        В случае, если несколько книг соответствуют значениям для поиска - выводит все эти книги.
        :param search_type: Параметры поиска (по умолчанию: 'название', 'автор' и 'год').
        :param search_term: Значение для поиска в выбранном параметре.
        """
        search_book_result = [
            book for book in self.books
            if search_term.lower() in str(getattr(book, search_type)).lower()
        ]
        if search_book_result:
            print("\nВот что удалось найти по вашему запросу:\n")
        self.print_books(search_book_result)

    def display_books(self) -> None:
        """Выводит на экран все книги, находящиеся в данный момент в библиотеке."""
        if not self.books:
            print("В данный момент в библиотеке нет ни одной книги.")
            return
        self.print_books(self.books)

    def change_status(self, book_id: str, new_status: str) -> None:
        """
        Изменяет статус книги с переданным ID.
        В случае, если ID книги есть в библиотеке и текущий статус отличается от переданного -
        заменяет значение статуса на переданный.
        :param book_id: ID книги, у которой надо изменить статус.
        :param new_status: Новый статус книги.
        """
        book = next((book for book in self.books if book.id == book_id), None)
        if not book:
            print(f"Книга с id {book_id} не найдена.")
            return

        if book.status == new_status:
            print(f"У книги '{book.title}' уже установлен статус '{book.status}' в настоящий момент.")
            return

        book.status = new_status
        self._save_books()
        print(f"Статус книги '{book.title}' изменен на '{new_status}'")