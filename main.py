from librarian import Librarian
import sys

def configure_io() -> None:
    """Настройка ввода-вывода для поддержки UTF-8"""
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')


def display_menu() -> None:
    """Отображение меню действий"""
    print("\nВыберите действие")
    menu_items = {
        1: "Добавить книгу",
        2: "Удалить книгу",
        3: "Найти книгу",
        4: "Отобразить все книги",
        5: "Изменить статус книги",
        6: "Выйти"
    }
    for key, value in menu_items.items():
        print(f"{key}. {value}")

def main():
    configure_io()
    librarian = Librarian()
    while True:
        display_menu()
        choice = input("\nВведите номер действия: ")

        actions = {
            "1": librarian.add_book,
            "2": librarian.delete_book,
            "3": librarian.search_book,
            "4": librarian.display_books,
            "5": librarian.change_status,
        }

        if choice == "6":
            print("Всего доброго! Ждем вас снова в нашей библиотеке!")
            break

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()