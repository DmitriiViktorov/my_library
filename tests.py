import unittest
import random
from unittest.mock import patch, Mock
import tempfile
from pathlib import Path
from data_manager import DataManager
from library import Library, BookStatus
from librarian import Librarian



class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.temp_file_path = Path(self.temp_file.name)
        self.data_manager = DataManager(self.temp_file_path)


    def tearDown(self):
        self.temp_file_path.unlink(missing_ok=True)


    def test_load_file_not_found(self):
        self.temp_file_path.unlink()
        books = self.data_manager.load_books()
        self.assertEqual(books, [])

    def test_save_and_load_book(self):
        book = [{"id": "1", "title": "Book1", "author": "Author 1", "year": 1991, "status": "выдана"}]
        self.data_manager.save_books(book)
        loaded_books = self.data_manager.load_books()
        self.assertEqual(loaded_books, book)

    def test_load_books_empty_file(self):
        self.temp_file_path.write_text("")
        loaded_books = self.data_manager.load_books()
        self.assertEqual(loaded_books, [])

    def test_load_invalid_json(self):
        self.temp_file_path.write_text("string data")
        books = self.data_manager.load_books()
        self.assertEqual(books, [])


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.temp_file_path = Path(self.temp_file.name)
        self.data_manager = DataManager(self.temp_file_path)
        self.library = Library(self.data_manager)

    def tearDown(self):
        self.temp_file_path.unlink(missing_ok=True)

    def test_add_book(self):
        with patch('builtins.print') as mock_print:
            self.library.add_book("Book1", "Author 1", "1991")
            self.assertEqual(len(self.library.books), 1)
            self.assertEqual(self.library.books[0].title, "Book1")
            self.assertEqual(self.library.books[0].author, "Author 1")
            self.assertEqual(self.library.books[0].year, 1991)
            self.assertEqual(self.library.books[0].status, BookStatus.AVAILABLE.value)
        mock_print.assert_called_once_with("\nКнига 'Book1' добавлена в библиотеку.")

    def test_delete_book_confirm(self):
        with patch('builtins.print'):
            self.library.add_book("Book1", "Author 1", "1991")
        book = self.library.books[0]

        with patch('builtins.input', return_value=random.choice(['да', 'yes', 'д', 'y'])):
            with patch('builtins.print') as mock_print:
                self.library.delete_book("1")
                self.assertNotIn(book, self.library.books)
                self.assertEqual(len(self.library.books), 0)


            mock_print.assert_called_once_with("\nКнига с id 1 удалена из библиотеки.")

    def test_delete_book_deny(self):
        with patch('builtins.print'):
            self.library.add_book("Book1", "Author 1", "1991")
        book = self.library.books[0]

        with patch('builtins.input', return_value=random.choice(['нет', 'No', '4', 'ЧЕТВЕРГ'])):
            with patch('builtins.print') as mock_print:
                self.library.delete_book("1")
                self.assertIn(book, self.library.books)
                self.assertEqual(len(self.library.books), 1)

            mock_print.assert_called_once_with("Удаление книги Book1 отменено.")

    def test_delete_missing_book(self):
        with patch('builtins.print'):
            self.library.add_book("Book1", "Author 1", "1991")
        book = self.library.books[0]

        with patch('builtins.input', return_value=random.choice(['нет', 'No', '42', 'ЧЕТВЕРГ'])):
            with patch('builtins.print') as mock_print:
                self.library.delete_book("2")
                self.assertIn(book, self.library.books)
                self.assertEqual(len(self.library.books), 1)

            mock_print.assert_called_once_with("Книга с id 2 не найдена.")

    def test_search_book(self):
        with patch('builtins.print'):
            self.library.add_book("1984", "George Orwell", "1949")

        search_cases = (('title', '1984'), ('author', 'George Orwell'), ('year', '1949'))
        for case in search_cases:
            with patch('builtins.print') as mock_print:
                self.library.search_book(*case)
                bottom_line = mock_print.call_args_list[-1][0][0]
                self.assertIn(case[1], bottom_line)

    def test_search_two_books(self):
        with patch('builtins.print'):
            self.library.add_book("1984", "George Orwell", "1949")
            self.library.add_book("Animal Farm", "George Orwell", "1945")

        with patch('builtins.print') as mock_print:
            self.library.search_book('author', 'Orwell')
        output_lines = [call.args[0] for call in mock_print.call_args_list][-2:]
        self.assertTrue(any('1984' in line for line in output_lines))
        self.assertTrue(any('Animal Farm' in line for line in output_lines))

    def test_search_book_not_found(self):
        with patch('builtins.print'):
            self.library.add_book("1984", "George Orwell", "1949")

        with patch('builtins.print') as mock_print:
            self.library.search_book('title', 'Animal Farm')

        mock_print.assert_called_once_with("Книги не найдены.")

    def test_display_books(self):
        with patch('builtins.print'):
            self.library.add_book("1984", "George Orwell", "1949")

        with patch('builtins.print') as mock_print:
            self.library.display_books()
            output_lines = [call.args[0] for call in mock_print.call_args_list][-1]
        for book_data in ("1984", "George Orwell", "1949"):
            self.assertIn(book_data, output_lines)

    def test_display_book_empty_library(self):
        with patch('builtins.print') as mock_print:
            self.library.display_books()
        mock_print.assert_called_once_with("В данный момент в библиотеке нет ни одной книги.")

    def test_change_book_status(self):
        with patch('builtins.print'):
            self.library.add_book("1984", "George Orwell", "1949")

        with patch('builtins.print') as mock_print:
            self.library.change_status("1", "выдана")
        mock_print.assert_called_once_with("Статус книги '1984' изменен на 'выдана'")
        book = self.library.books[0]

        self.assertEqual(book.status, 'выдана')

    def test_change_book_not_found(self):
        with patch('builtins.print'):
            self.library.add_book("1984", "George Orwell", "1949")

        with patch('builtins.print') as mock_print:
            self.library.change_status("2", "выдана")
        mock_print.assert_called_once_with("Книга с id 2 не найдена.")

    def test_change_book_same_status(self):
        with patch('builtins.print'):
            self.library.add_book("1984", "George Orwell", "1949")

        with patch('builtins.print') as mock_print:
            self.library.change_status("1", "в наличии")
        mock_print.assert_called_once_with("У книги '1984' уже установлен статус 'в наличии' в настоящий момент.")


class TestLibrarian(unittest.TestCase):
    def setUp(self):
        self.mock_library = Mock(spec=Library)
        self.librarian = Librarian(self.mock_library)


    def test_add_book_success(self):
        with patch('librarian.validate_input', side_effect=['Book Title', 'Author', '2022']):
            self.librarian.add_book()
            self.mock_library.add_book.assert_called_once_with('Book Title', 'Author', '2022')

    def test_add_book_cancel(self):
        with patch('librarian.validate_input', return_value=None):
            with patch('builtins.print') as mock_print:
                self.librarian.add_book()
                self.mock_library.add_book.assert_not_called()
                mock_print.assert_called_with("Добавление книги отменено.")

    def test_delete_book_success(self):
        with patch('librarian.validate_input', return_value='1'):
            self.librarian.delete_book()
            self.mock_library.delete_book.assert_called_once_with('1')

    def test_delete_book_cancel(self):
        with patch('librarian.validate_input', return_value=None):
            with patch('builtins.print') as mock_print:
                self.librarian.delete_book()
                self.mock_library.delete_book.assert_not_called()
                mock_print.assert_called_with("Удаление книги отменено.")

    def test_search_book_success(self):
        with patch('librarian.validate_input', side_effect=['название', 'Python']):
            self.librarian.search_book()
            self.mock_library.search_book.assert_called_once_with('title', 'Python')

    def test_search_book_cancel(self):
        with patch('librarian.validate_input', side_effect=[None, None]):
            with patch('builtins.print') as mock_print:
                self.librarian.search_book()
                self.mock_library.search_book.assert_not_called()
                mock_print.assert_called_with("Поиск книги отменен.")

    def test_display_books(self):
        self.librarian.display_books()
        self.mock_library.display_books.assert_called_once()

    def test_change_status_success(self):
        with patch('librarian.validate_input', side_effect=['1', 'выдана']):
            self.librarian.change_status()
            self.mock_library.change_status.assert_called_once_with('1', 'выдана')

    def test_change_status_cancel(self):
        with patch('librarian.validate_input', side_effect=['stop', None]):
            with patch('builtins.print') as mock_print:
                self.librarian.change_status()
                self.mock_library.change_status.assert_not_called()
                mock_print.assert_called_with("Изменение статуса отменено.")

if __name__ == '__main__':
    unittest.main()