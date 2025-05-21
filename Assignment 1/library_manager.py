import json
from typing import List, Dict, Optional
import os

class Library:
    def __init__(self):
        self.books: List[Dict] = []
        self.filename = "library.txt"
        self.load_library()

    def add_book(self, title: str, author: str, year: int, genre: str, read_status: bool) -> None:
        """Add a new book to the library."""
        book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read_status
        }
        self.books.append(book)
        print("Book added successfully!")

    def remove_book(self, title: str) -> bool:
        """Remove a book from the library by title."""
        initial_length = len(self.books)
        self.books = [book for book in self.books if book["title"].lower() != title.lower()]
        if len(self.books) < initial_length:
            print("Book removed successfully!")
            return True
        print("Book not found in the library.")
        return False

    def search_books(self, search_term: str, search_by: str) -> List[Dict]:
        """Search for books by title or author."""
        search_term = search_by.lower()
        if search_by == "title":
            return [book for book in self.books if search_term in book["title"].lower()]
        elif search_by == "author":
            return [book for book in self.books if search_term in book["author"].lower()]
        return []

    def display_all_books(self) -> None:
        """Display all books in the library."""
        if not self.books:
            print("Your library is empty!")
            return

        print("\nYour Library:")
        for i, book in enumerate(self.books, 1):
            status = "Read" if book["read"] else "Unread"
            print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")

    def get_statistics(self) -> Dict:
        """Calculate and return library statistics."""
        total_books = len(self.books)
        if total_books == 0:
            return {"total": 0, "percentage_read": 0.0}

        read_books = sum(1 for book in self.books if book["read"])
        percentage_read = (read_books / total_books) * 100

        return {
            "total": total_books,
            "percentage_read": percentage_read
        }

    def save_library(self) -> None:
        """Save the library to a file."""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.books, f, indent=4)
            print("Library saved to file.")
        except Exception as e:
            print(f"Error saving library: {e}")

    def load_library(self) -> None:
        """Load the library from a file."""
        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, 'r') as f:
                self.books = json.load(f)
        except Exception as e:
            print(f"Error loading library: {e}")
            self.books = []

def get_valid_year() -> int:
    """Get a valid publication year from user input."""
    while True:
        try:
            year = int(input("Enter the publication year: "))
            if 1000 <= year <= 2024:  # Reasonable year range
                return year
            print("Please enter a valid year between 1000 and 2024.")
        except ValueError:
            print("Please enter a valid number for the year.")

def get_valid_yes_no() -> bool:
    """Get a valid yes/no response from user input."""
    while True:
        response = input("Have you read this book? (yes/no): ").lower()
        if response in ['yes', 'y']:
            return True
        if response in ['no', 'n']:
            return False
        print("Please enter 'yes' or 'no'.")

def main():
    library = Library()
    
    while True:
        print("\nWelcome to your Personal Library Manager!")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search for a book")
        print("4. Display all books")
        print("5. Display statistics")
        print("6. Exit")
        
        try:
            choice = int(input("\nEnter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            title = input("Enter the book title: ").strip()
            author = input("Enter the author: ").strip()
            year = get_valid_year()
            genre = input("Enter the genre: ").strip()
            read_status = get_valid_yes_no()
            
            if title and author and genre:  # Basic validation
                library.add_book(title, author, year, genre, read_status)
            else:
                print("Please fill in all book details.")

        elif choice == 2:
            title = input("Enter the title of the book to remove: ").strip()
            if title:
                library.remove_book(title)
            else:
                print("Please enter a valid title.")

        elif choice == 3:
            print("\nSearch by:")
            print("1. Title")
            print("2. Author")
            try:
                search_choice = int(input("Enter your choice: "))
                if search_choice not in [1, 2]:
                    raise ValueError
                
                search_by = "title" if search_choice == 1 else "author"
                search_term = input(f"Enter the {search_by}: ").strip()
                
                if search_term:
                    results = library.search_books(search_term, search_by)
                    if results:
                        print("\nMatching Books:")
                        for i, book in enumerate(results, 1):
                            status = "Read" if book["read"] else "Unread"
                            print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
                    else:
                        print("No matching books found.")
                else:
                    print("Please enter a valid search term.")
            except ValueError:
                print("Please enter a valid choice (1 or 2).")

        elif choice == 4:
            library.display_all_books()

        elif choice == 5:
            stats = library.get_statistics()
            print(f"\nTotal books: {stats['total']}")
            print(f"Percentage read: {stats['percentage_read']:.1f}%")

        elif choice == 6:
            library.save_library()
            print("Goodbye!")
            break

        else:
            print("Please enter a valid choice (1-6).")

if __name__ == "__main__":
    main() 