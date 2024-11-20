import data_manager

BOOK_STATUS = {
    0: "выдана",
    1: "в наличии"
}


class Library:
    def __init__(self):
        self.books = data_manager.load_books()

    @staticmethod
    def print_books(books_list):
        print(f"{'ID':<5}{'Название':<25}{'Автор':<25}{'Год':<10}{'Статус':<10}")
        print("-" * 75)
        for book in books_list:
            print(f"{book['id']:<5}{book['title']:<25}{book['author']:<25}{book['year']:<10}{book['status']:<10}")


    def add_book(self, title, author, year):
        if not self.books:
            book_id = "1"
        else:
            max_id = max(int(book["id"]) for book in self.books)
            book_id = str(max_id + 1)

        new_book = {
            "id": book_id,
            "title": title,
            "author": author,
            "year": year,
            "status": BOOK_STATUS[1],
        }
        self.books.append(new_book)
        data_manager.save_books(self.books)
        print(f"\nКнига '{new_book["title"]}' добавлена в библиотеку.")

    def delete_book(self, book_id):
        for book in self.books:
            if book["id"] == book_id:
                confirm = input(f"Вы уверены, что хотите удалить книгу {book["title"]} с ID {book_id} (да/нет): ")
                if confirm.lower() in ('да', 'yes', 'д', 'y'):
                    self.books.remove(book)
                    data_manager.save_books(self.books)
                    print(f"\nКнига с id {book_id} удалена из библиотеки.")
                    return
                else:
                    print(f"Удаление книги {book["title"]} отменено.")

        print(f"Книга с id {book_id} не найдена.")

    def search_book(self, search_type, search_term):
        search_book_result = [book for book in self.books if search_term.lower() in str(book[search_type]).lower()]

        if search_book_result:
            self.print_books(search_book_result)
        else:
            print("Книга не найдена.")

    def display_books(self):
        if self.books:
            self.print_books(self.books)
        else:
            print("В данный момент в библиотеке нет ни одной книги.")


    def change_status(self, book_id, new_status):
        for book in self.books:
            if book["id"] == book_id:
                if new_status != book["status"]:
                    book["status"] = new_status
                    data_manager.save_books(self.books)
                    print(f"Статус книги {book["title"]} изменен на {new_status}")
                    return
                else:
                    print(f"У книги {book["title"]} уже установлен статус '{book["status"]}' в настоящий момент.")
                    return
        print(f"Книга с id {book_id} не найдена.")
