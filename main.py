from librarian import Librarian
import sys


sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


def main():
    librarian = Librarian()
    while True:
        print()
        print("Выберите действие:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")
        choice = input("Введите номер действия: ")
        print()
        match choice:
            case "1":
                librarian.add_book()
            case "2":
                librarian.delete_book()
            case "3":
                librarian.search_book()
            case "4":
                librarian.display_books()
            case "5":
                librarian.change_status()
            case "6":
                print("Всего доброго! Ждем вас снова в нашей библиотеке!")
                break
            case _:
                print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()