import pandas as pd
import os
import re

def check_files():
    if os.path.exists('books.csv'):
        dfBooks = pd.read_csv('books.csv')
    else:
        dfBooks = pd.DataFrame({
            'bookID': [],
            'title': [],
            'authors': [],
            'status': []
        })

        dfBooks.to_csv('books.csv', index=False)

    if os.path.exists('booksIssued.csv'):
        dfBooksIssued = pd.read_csv('booksIssued.csv')
    else:
        dfBooksIssued = pd.DataFrame({
            'bookID': [],
            'issuedTo': []
        })

        dfBooksIssued.to_csv('booksIssued.csv', index=False)

def read_dataframe(file_path):
    """
    Read a CSV file and return the DataFrame.

    Parameters:
    - file_path (str): The path to the CSV file.

    Returns:
    - pd.DataFrame: The DataFrame read from the CSV file.
    """
    try:
        dataframe = pd.read_csv(file_path)
        return dataframe
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return pd.DataFrame()    

class Library:
    def __init__(self, df_books, df_books_issued):
        """Initialize the Library with book and issued book DataFrames."""

        self.df_books = df_books

        self.df_books_issued = df_books_issued

        self.available_status = 'Available'
        self.issued_status = 'Issued'

    def save_books_to_csv(self):
        """Save books DataFrame to 'books.csv' file."""
        self.df_books.to_csv('books.csv', index=False)


    def save_issued_books_to_csv(self):
        """Save issued books DataFrame to 'booksIssued.csv' file."""
        self.df_books_issued.to_csv('booksIssued.csv', index=False)


    def validate_book_id(self, book_id):
        """Check if book_id contains only digits."""
        return book_id.isdigit()


    def validate_issued_to(self, issued_to):
        """Check if issued_to contains only alphanumeric characters and spaces."""
        return bool(re.match(r'^[a-zA-Z0-9\s]+$', issued_to))


    def clean_input(self, user_input):
        """Clean user input by stripping extra spaces and converting to lowercase."""
        return user_input.strip().lower()


    def is_unique_book_id(self, book_id):
        """Check if the book ID is unique within the library."""
        idBook = self.df_books[self.df_books.bookID.astype(str) == book_id]
        return idBook.empty


    def process_add_book(self):
        """Add a new book to the library."""
        book_id = input('Enter book id: ')

        if not self.validate_book_id(book_id):
            print('Invalid book ID. Please enter a numeric value.')
            return
        else:
            if not self.is_unique_book_id(book_id):
                print('Book with this ID already exists. Please enter a unique ID.')
                return
            else:
                book_id = book_id
                title = self.clean_input(input('Enter title of book: '))
                author = self.clean_input(input('Enter author name: '))
                status = self.available_status

                new_book = pd.DataFrame({
                    'bookID': [book_id],
                    'title': [title],
                    'authors': [author],
                    'status': [status]
                })

                print('\n Printing added data \n\n', new_book, '\n')
                self.df_books = pd.concat([self.df_books, new_book], ignore_index=True)

        self.df_books = self.df_books.drop_duplicates(subset='bookID')  # Ensure uniqueness
        self.save_books_to_csv()


    def process_view_books(self):
        """Display the books table."""
        print(self.df_books)

    def process_delete_book(self):
        """Delete a book from the library."""
        book_id_to_delete = input('Enter book id to delete: ')
        

        if not self.validate_book_id(book_id_to_delete):
            print('Invalid book ID. Please enter a numeric value.')
            return

        book_id_to_delete = int(book_id_to_delete)

        matching_books = self.df_books[self.df_books['bookID'] == book_id_to_delete]
        if not matching_books.empty:
            self.df_books = self.df_books[self.df_books['bookID'] != book_id_to_delete]
            self.df_books_issued = self.df_books_issued[
                self.df_books_issued['bookID'] != book_id_to_delete
            ]
            self.save_books_to_csv()
            self.save_issued_books_to_csv()
        else:
            print('Error: Book not found.')

    def process_view_issued_books(self):
        """Display the issued books table."""
        print(self.df_books_issued)

    def process_issue_book(self):
        """Issue a book to a reader."""
        book_id = self.clean_input(input('Enter book id: '))

        if not self.validate_book_id(book_id):
            print('Invalid book ID. Please enter a numeric value.')
            return

        book_id = int(book_id)

        id_book = self.df_books[self.df_books['bookID'] == book_id]
        if not id_book.empty:
            avail = id_book[id_book['status'] == self.available_status]
            if not avail.empty:
                print(self.available_status)
                issued_to = self.clean_input(input('Issue To: '))

                if not self.validate_issued_to(issued_to):
                    print('Invalid issuedTo. Please enter only alphanumeric characters and spaces.')
                    return

                boolean_condition = (self.df_books['bookID'] == book_id)
                column_name = 'status'
                new_value = self.issued_status

                self.df_books.loc[boolean_condition, column_name] = new_value

                new_issue = pd.DataFrame({
                    'bookID': [book_id],
                    'issuedTo': [issued_to]
                })

                print('\n Printing added data \n', new_issue, '\n')
                self.df_books_issued = pd.concat([self.df_books_issued, new_issue], ignore_index=True)

                self.save_books_to_csv()
                self.save_issued_books_to_csv()

            else:
                print('Book already issued')

        else:
            # self.df_books = self.df_books.reset_index(drop=False)
            print('Book not available')

    def process_return_book(self):
        """Return a book to the library."""
        book_id = self.clean_input(input('Enter book id: '))

        if not self.validate_book_id(book_id):
            print('Invalid book ID. Please enter a numeric value.')
            return
        
        book_id = int(book_id)

        id_book = self.df_books[self.df_books['bookID'] == book_id]
        if not id_book.empty:

            issu = id_book[id_book['status'] == self.issued_status]
            if not issu.empty:

                print(self.issued_status)

                boolean_condition = (self.df_books['bookID'] == book_id)
                column_name = 'status'
                new_value = self.available_status

                self.df_books.loc[boolean_condition, column_name] = new_value

                self.df_books_issued = self.df_books_issued[self.df_books_issued['bookID'] != book_id]

                self.save_books_to_csv()
                self.save_issued_books_to_csv()

            else:
                print('Book not issued')

        else:
            # self.df_books = self.df_books.reset_index(drop=False)
            print('Book not available')


if __name__ == '__main__':

    os_info = os.uname().sysname

    check_files()

    df_books = read_dataframe('books.csv')
    df_books_issued = read_dataframe('booksIssued.csv')

    lib = Library(df_books, df_books_issued)

    while True:
        print('1. Add book')
        print('2. Show books table')
        print('3. Delete book')
        print('4. Issue book')
        print('5. Show Issued books table')
        print('6. Return book')
        print('7. Exit')

        x = str(input('Enter your choice : '))

        try:
            if os_info == 'Windows':
                os.system('cls')
            elif os_info == 'Linux':
                os.system('clear')
        except Exception as e:
            print(f'Error clearing screen: {e}')

        print('You entered ' + x)
        print('\n')

        if x == '1':
            lib.process_add_book()
        elif x == '2':
            lib.process_view_books()
        elif x == '3':
            lib.process_delete_book()
        elif x == '4':
            lib.process_issue_book()
        elif x == '5':
            lib.process_view_issued_books()
        elif x == '6':
            lib.process_return_book()
        elif x == '7':
            break
        else:
            print('Please give valid input')

        print('-' * 40)

    quit()
    exit()
