import sqlite3
import pandas as pd
from sys import exit
from termcolor import colored


def generate_id(db, cursor):
    """ Function to generate id number for every data entry in ebookstore
    database. Id numbers start from 3000.
    """
    # Select the id number of the last row in the database.
    cursor.execute('''SELECT id FROM ebookstore WHERE id IN
                   (SELECT max(id) FROM ebookstore);''')
    # Assign 3000 in number to 'id_no' variable incase of empty table in the
    # database.
    try:
        id_no = cursor.fetchone()[0]
    except TypeError:
        id_no = 3000
    return id_no


def add_book(db, cursor):
    """ Function to generate add new book in ebookstore database.
    """
    books_ = []
    add_book = 'yes'
    # Get id number of the last row in the database
    book_id = generate_id(db, cursor)
    while add_book == 'yes':
        # Get title, author and quantity of the new book entry in the database.
        title = input("Enter book's title: ")
        author = input("Enter book's author: ")
        qty = int(input("Enter book's quantity: "))
        book_id += 1
        # Append tuple containing new book data to 'books_' list
        books_.append((book_id, title, author, qty))
        add_book = input("Add another book (yes/no): ")
    # Insert new books data from 'books_' list in the database.
    cursor.executemany(''' INSERT INTO ebookstore(id, Title, Author, Qty)
                       VALUES(?,?,?,?)''', books_)
    db.commit()


def update_book(db, cursor):
    """ Function to update existing book's quantities in ebookstore database.
    The book data to be updated can be selected by book title or id.
    """
    # Request user to select if a book data to be updated by book title or id
    user_choice = input('Update by title or id? - ').lower()

    if user_choice == 'title':
        title = '0'
        # While loop if book is to be updated by book title.
        while title != '1':
            try:
                # Request user to enter the title (or a part of the book title)
                # of the book to be updated
                title = input("Enter book's title: ")
                # Go to main menu if 'title' = '1'
                if title == '1':
                    continue
                # select the record from the database where 'title' variable
                # matches a book title or a part of a book title.
                cursor.execute('''SELECT Title, Author, Qty FROM ebookstore
                               WHERE INSTR(Title, ?)>0''', (title, ))
                update_book = cursor.fetchone()
                print('Book found: ', update_book[0])
                # User to provide new quantity of the selected book to update
                # in the database.
                qty_update = int(input("Enter book's quantity: "))
                # Update database with new book quantity info
                cursor.execute('''UPDATE ebookstore SET Qty = ? WHERE
                               Title = ?''', (qty_update, update_book[0]))
                print(f'{update_book[0]} book quantity updated to '
                      f'{qty_update}\n')
                # Set 'title' variable value to '1' to exit while loop
                title = '1'
            except TypeError:
                print(colored('Invalid title. Please try again. Enter 1 to '
                              'exit', 'green'))
                continue
    elif user_choice == 'id':
        book_id = 0
        # While loop if book is to be updated by book id.
        while book_id != 1:
            try:
                # Request user to enter the id of the book to be updated.
                book_id = int(input("Enter book's id: "))
                if book_id == 1:
                    continue
                # select the record from the database where 'book_id' variable
                # matches a book id in the database.
                cursor.execute('''SELECT Title, Author, Qty FROM ebookstore
                               WHERE id=?''', (book_id, ))
                update_book = cursor.fetchone()
                print('Book found: ', update_book[0])
                # User to provide new quantity of the selected book to update
                # in the database.
                qty_update = int(input("Enter book's quantity: "))
                # Update database with new book quantity info
                cursor.execute('''UPDATE ebookstore SET Qty = ? WHERE
                               Title = ?''', (qty_update, update_book[0]))
                print(f'{update_book[0]} book quantity updated to '
                      f'{qty_update}.\n')
                # Set 'book_id' variable value to 1 to exit while loop
                book_id = 1
            except TypeError:
                print(colored('Invalid book id. Please try again. Enter 1 to '
                              'exit', 'green'))
                continue
    else:
        print(colored('Invalid choice. Please try again', 'green'))
    db.commit()


def delete_book(db, cursor):
    """ Function to delete existing book's quantities in ebookstore database.
    The book data to be deleted can be selected by book title or id.
    """
    # Request user to select if a book data to be deleted by book title or id
    user_choice = input('Delete by title or id? - ').lower()
    if user_choice == 'title':
        title = '0'
        # While loop if book is to be deleted by book title.
        while title != '1':
            try:
                # Request user to enter the title (or a part of the book title)
                # of the book to be deleted
                title = input("Enter book's title: ")
                # Go to main menu if 'title' = '1'
                if title == '1':
                    continue
                # select the record from the database where 'title' variable
                # matches books title (or a part of a title) in the database.
                cursor.execute('''SELECT Title, Author, Qty FROM ebookstore
                               WHERE INSTR(Title, ?)>0''', (title, ))
                # Fetch all books info whete 'title' variable matched a part of
                # the book titles.
                delete_book = cursor.fetchall()
                # If a single book record found then value stored in
                # 'delete_book_1' will be used to delete the book data.
                delete_book_1 = delete_book[0][0]
                # If multiple books' recoreds found in the database, then print
                # all books title to allow user to select the correct book
                # title to delete.
                if len(delete_book) > 1:
                    print(colored('Multiple books found. Please select the '
                          'correct title from below.'),
                          'light_magenta')
                    # Set 'del_check' list to store the titles of all books
                    # searched.
                    del_check = []
                    for item in delete_book:
                        print(item[0])
                        del_check.append(item[0])
                    # Request user to enter correct name of the book to be
                    # deleted from the searched books.
                    delete_book_1 = input("Enter correct book's title: ")
                    # Go to main menu if the title entered by user does not
                    # match with any of the searched books titles.
                    print(del_check)
                    if delete_book_1 not in del_check:
                        print(colored('Invalid title. Please try again',
                                      'green'))
                        break
                # Delete the selected book data from the database.
                cursor.execute('''DELETE from ebookstore WHERE Title = ?''',
                               (delete_book_1,))
                print(f'{delete_book_1} book record deleted')
                # Set 'title' variable value to 1 to exit while loop
                title = '1'
            except (TypeError, IndexError):
                print(colored('Invalid title. Please try again. Enter 1 to '
                              'exit', 'green'))
                continue
    elif user_choice == 'id':
        book_id = 0
        # While loop if book is to be deleted by book id.
        while book_id != 1:
            try:
                # Request user to enter the id of the book to be deleted
                book_id = int(input("Enter book's id: "))
                # Go to main menu if 1 is entered by user.
                if book_id == 1:
                    continue
                # select the book title from the database where 'book_id'
                # variable value matches with an Id in the database.
                cursor.execute('''SELECT Title, Author, Qty FROM ebookstore
                               WHERE id=?''', (book_id, ))
                delete_book = cursor.fetchone()
                # Stored book title from 'delete_book' in 'delete_book_1' to
                # use to delete the book data.
                delete_book_1 = delete_book[0]
                # Delete the selected book data from the database.
                cursor.execute('''DELETE from ebookstore WHERE Title = ?''',
                               (delete_book_1,))
                print(f'{delete_book_1} book record deleted')
                # Set 'book_id' variable value to 1 to exit while loop
                book_id = 1
            except TypeError:
                print(colored('Invalid book id. Please try again. Enter 1 to '
                              'exit', 'green'))
                continue
    db.commit()


def search(db, cursor):
    """ Function to search existing book data in ebookstore database.
    The book data to be searched can be selected by search terms or id.
    """
    # Request user to select if a book data to be searched by search terms or
    # book id.
    user_choice = input('Search by terms or id? - ').lower()
    if user_choice == 'terms':
        terms = '0'
        # While loop if the database is to be searched by search terms.
        while terms != '1':
            try:
                search = input('Enter search term: ')
                # In case of multiple search teams, split the 'search' string
                # to carry out search for each word in the search term.
                search_term = search.split()
                # Search in book Title and Author data and select the book
                # records where each word in the search term matches with
                # either a word in the books Titles or Authors' names.
                for words in search_term:
                    cursor.execute('''SELECT Title, Author, Qty FROM
                                   ebookstore WHERE INSTR(Title, ?)>0 OR
                                   INSTR(Author, ?)>0 ''', (words, words))
                    books = cursor.fetchall()
                    # Create an empty list to store searched books data to
                    # create search results dataframe 'books_df'.
                    results = []
                    for elem in books:
                        results.append(list(elem))
                books_df = pd.DataFrame(results, columns=['Title',
                                                          'Author', 'Qty'])
                print(books_df.to_string(index=False))
                # Set 'terms' variable value to '1' to exit while loop
                terms = '1'
            except IndexError:
                print(colored('Invalid search term. Please try again\n',
                              'green'))
                pass
    elif user_choice == 'id':
        book_id = 0
        # While loop if the database is to be searched by book id.
        while book_id != 1:
            try:
                # Request user to enter book id to search book info from
                # database.
                book_id = int(input("Enter book's id: "))
                # results_lst = []
                # Go to main menu if 1 is entered by user.
                if book_id == 1:
                    continue
                cursor.execute('''SELECT Title, Author, Qty FROM ebookstore
                               WHERE id = ? ''', (book_id, ))
                books = cursor.fetchone()
                # Create 'results' vriable and store search results to create
                # dataframe 'books_df'.
                results = [list(books)]
                books_df = pd.DataFrame(results, columns=['Title',
                                                          'Author', 'Qty'])
                print('\n', books_df.to_string(index=False), '\n')
                book_id = 1
            except IndexError:
                print(colored('Invalid id. Please try again\n', 'green'))
                pass


def display_table(db, cursor):
    """ Function to display ebookstore database.
    """
    cursor.execute('''SELECT * from ebookstore''')
    table = cursor.fetchall()
    table_df = pd.DataFrame(table, columns=['id', 'Title', 'Author', 'Qty'])
    print('\n\n', '----------------------------------------------------------'
          '---------', '\n')
    print(table_df.to_string(index=False))
    print('\n', '-------------------------------------------------------------'
          '--------', '\n\n')


def main():
    """ Function to display user menu and execute relevent function based on
    user input.
    """
    print(colored('\nWelcome to ebookstore\n', 'blue', attrs=['bold',
                                                              'underline']))
    db = sqlite3.connect('ebookstore')
    cursor = db.cursor()
    # try and except to handle exception if the data table already exists.
    try:
        # Create a table called ebookstore
        cursor.execute('''CREATE TABLE ebookstore (id INTEGER PRIMARY KEY,
                       Title TEXT,  Author TEXT, Qty INTEGER)''')
        db.commit()
    except Exception as e:
        print(colored('Message:- '+(str(e).capitalize()+'\n'), 'green'))
        pass
    while True:
        menu = input(colored('''Select one of the following Options below:
                    a - Add Book
                    u - Update Book
                    d - Delete Book
                    p - Display Database
                    s - Search Database
                    e - Exit
                    : ''', 'red')).lower()

        if menu == 'a':  # Add a new book
            add_book(db, cursor)

        elif menu == 'u':  # Update book
            update_book(db, cursor)

        elif menu == 'd':  # Delete book
            delete_book(db, cursor)

        elif menu == 'p':  # Display books database
            display_table(db, cursor)

        elif menu == 's':  # Search books database
            search(db, cursor)

        elif menu == 'e':  # Exit program
            print('Goodbye!!!')
            exit()

        else:  # Default case
            print(colored("\nYou have made a wrong choice, Please Try again\n",
                          'green'))


if __name__ == '__main__': main()
