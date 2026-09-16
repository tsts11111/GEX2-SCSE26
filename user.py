## This module contains the user interface for the library system.
# It allows users to search for books, borrow books, and return books.

## Import the necessary functions from the admin module.
from admin import (
    find_book,
    load_library,
    save_library,
)


## Search books by category.
## This function should return book IDs that match the given category.
def books_in_category(
    books,
    category
):
    target = str(category).strip().lower()

    if target == "":
        return []

    result = []

    for book_id, book in books.items():
        book_category = str(book.get("category", "")).strip().lower()
        if book_category == target:
            result.append(book_id)

    return result


## Search books by full or partial title.
## This function should return book IDs that match the given title or part of the title.
def search_by_title(
    books,
    search_text
):
    target = str(search_text).strip().lower()

    if target == "":
        return []

    result = []

    for book_id, book in books.items():
        title = str(book.get("title", "")).lower()
        if target in title:
            result.append(book_id)

    return result


## Create logic to let users borrow books.
## The function should check if the book is available or on loan, or if the borrower name is provided.
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not available, then return "NOT_AVAILABLE"
## If the book is successfully borrowed, then return "OK"
def borrow_book(
    books,
    loans,
    search_text,
    borrower
):
    if not isinstance(borrower, str) or borrower.strip() == "":
        return "EMPTY_NAME"

    book_id = find_book(books, search_text)

    if book_id is None:
        return "BOOK_NOT_FOUND"

    book = books[book_id]

    if not book.get("available"):
        return "NOT_AVAILABLE"

    book["available"] = False
    loans.append({
        "book_id": book_id,
        "borrower": borrower.strip()
    })

    return "OK"


## Create logic to let users return books.
## The function should check if the book is on loan, or if the borrower name is provided
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not on loan, then return "NOT_ON_LOAN"
## If the book is successfully returned, then return "OK"
def return_book(
    books,
    loans,
    book_title,
    borrower
):
    if not isinstance(borrower, str) or borrower.strip() == "":
        return "EMPTY_NAME"

    book_id = find_book(books, book_title)

    if book_id is None:
        return "BOOK_NOT_FOUND"

    book = books[book_id]

    if book.get("available"):
        return "NOT_ON_LOAN"

    borrower_key = borrower.strip().lower()

    for loan in loans:
        if (
            loan.get("book_id") == book_id
            and str(loan.get("borrower", "")).strip().lower() == borrower_key
        ):
            book["available"] = True
            loans.remove(loan)
            return "OK"

    return "NOT_ON_LOAN"


## The main function that runs the user interface for the library system.
## The function must first load the library data from a JSON file, then display a menu for the user to select options.
## The options include searching for books by title or category, borrowing a book, returning a book, and exiting the program.
## When the user selects an option, the corresponding function is called to perform the action.
## The program continues to display the menu until the user chooses to exit, at which point the library data is saved back to the JSON file.
## The main function should also handle invalid selections by displaying an error message and prompting the user to select again.
def main():
    data = load_library("library.json")

    books = data.get("books", {})
    loans = data.get("loans", [])

    while True:
        print("LIBRARY USER SYSTEM")
        print("1. Search books by title")
        print("2. Search books by category")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            text = input("Enter title or part of title: ")
            found = search_by_title(books, text)
            if not found:
                print("No matching books found.")
            else:
                for book_id in found:
                    print(f"{book_id} | {books[book_id].get('title', '')}")

        elif choice == "2":
            category = input("Enter category: ")
            found = books_in_category(books, category)
            if not found:
                print("No books in that category.")
            else:
                for book_id in found:
                    print(f"{book_id} | {books[book_id].get('title', '')}")

        elif choice == "3":
            text = input("Enter book ID or title: ")
            borrower = input("Enter your name: ")
            result = borrow_book(books, loans, text, borrower)
            if result == "OK":
                print("Book borrowed successfully.")
            else:
                print(f"Could not borrow the book: {result}")

        elif choice == "4":
            text = input("Enter book ID or title: ")
            borrower = input("Enter your name: ")
            result = return_book(books, loans, text, borrower)
            if result == "OK":
                print("Book returned successfully.")
            else:
                print(f"Could not return the book: {result}")

        elif choice == "5":
            save_library(data, "library.json")
            break

        else:
            print("Invalid selection, please try again.")


if __name__ == "__main__":
    main()
