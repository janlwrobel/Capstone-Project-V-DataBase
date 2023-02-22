'''
╔═══════════════ HyperionDev - DfE Software Engineering December - Bootcamp ══════════════╗
║####                         Jan Lukasz Wrobel - JL22110005141                       ####║
║####                                 Capstone Project V                              ####║
╚═════════════════════════════════════════════════════════════════════════════════════════╝'''
# Resources for the project
    # filter() function in search_books(self):
        # https://www.programiz.com/python-programming/methods/built-in/filter
        # https://www.w3schools.com/python/ref_func_filter.asp


# ══════════════════════ Libraries ════════════════════════
import sqlite3
import spacy
from tabulate import tabulate
import os

# Colours
WHITE = '\033[0m'
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BOLD = '\033[1m'

# ══════════════════════ Classes ════════════════════════
# The Book class is used to represent a single book.
class Book:
    # Class book variables definition
    def __init__(self, title, author, qty):
        # Set the title of the book
        self.title = title
        # Set the author of the book
        self.author = author
        # Set the quantity of the book
        self.qty = qty
# ─────────────────────────────────────────────────────────

#This is a class definition for a Store object.
class Store:
    # Class store variable definitioin
    def __init__(self, store_database):
        # The store_database attribute represents the name of the SQLite database file used to store the books data.
        self.store_database = store_database
        # The constructor method then calls the get_database() method, which establishes a connection
        # to the database and creates the books table if it does not exist already.
        self.get_database(self.store_database)

    # The get_database method checks if the given database_name exists in the current working directory
    # using os.path.isfile() method. If the database file does not exist, it creates a new database by calling
    # create_table() and populate_database() methods, which are responsible inserting initial data into the table.
    def get_database(self, database_name):
        if not os.path.isfile(database_name):
            self.create_table()
            self.populate_database()
        # If the database file already exists, it simply prints a message that it is working on the existing database.
        else:
            print(f"Working on {database_name} database.")

    # The connection_db method establishes a connection to the SQLite database specified by the store_database attribute
    # of the Store class. It returns a connection object if the connection is successful, and raises an error if the connection fails.
    def  connection_db(self): #[^]
        # The method initializes the connection variable to None, and then attempts to establish a connection using
        # the sqlite3.connect() function. If the connection is successful, the method returns the connection object.
        # If the connection fails, it raises an error and prints an error message.
        connection = None
        # Excemption for connecting to database
        try:
            connection = sqlite3.connect(self.store_database)
            return connection
        except sqlite3.Error as e:
            print(f"Unable to connect to database {e}")
            raise e
        # The second return statement ensures that the method always returns a value,
        # whether or not an error occurs during the connection attempt.
        # Even though the try block did not execute successfully.
        return connection

    # creates a new SQLite database table named "books" if it does not already exist in the database.
    # The table has four columns: id (primary key), title, author , and quantity (with a default value of 0).
    def create_table(self):
        connection = self.connection_db()
        # The method first calls the connection_db() method to establish a connection to the database.
        # It then uses a try-except block to execute a CREATE TABLE SQL statement using a cursor object.
        # If the execution is successful, the method calls the commit() method of the connection object to save
        # the changes to the database. If there is an error, the method prints an error message and raises the exception.
        try:
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS books 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            author TEXT NOT NULL,
                            quantity INTEGER NOT NULL DEFAULT 0)''')
            connection.commit()
        except sqlite3.Error as e:
            print(f"Unable to create table {e}")
        # Calls the close() method of the connection object to close the connection to the database.
        connection.close()

    # This method populates the books table in the database with initial data when the Store object is created.
    # It creates a list of tuples called compulsory_books, with each tuple representing a book with its ID, title,
    # author, and quantity. The method then uses the connection_db method to establish a database connection and
    # creates a cursor object.
    def populate_database(self):
        # Populates the database table with initial data. It is called when the Database object is created.
        compulsory_books = [(3001, "A Tale of Two Cities", "Charles Dickens", 30),
                            (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
                            (3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25),
                            (3004, "The Lord of the Rings", "J.R.R. Tolkien", 37),
                            (3005, "Alice in Wonderland", "Lewis Carroll", 12),]
        connection = self.connection_db()
        cursor = connection.cursor()
        # SELECT statement to see if the table already has any data. If there is no data in the table, it uses a
        # for loop to iterate through the compulsory_books list and inserts each book into the table using an
        # INSERT statement. Finally, the method commits the changes to the database and closes the connection.
        try:
            cursor.execute('''SELECT id FROM books''')
            for book in compulsory_books:
                cursor.execute("INSERT INTO books(id, title, author, quantity) VALUES (?, ?, ?, ?)", book)
                connection.commit()
        # If an error occurs during the database interaction, the method prints the error message
        # and closes the connection.
        except sqlite3.Error as e:
            print(e)
        finally:
            connection.close()

    # The add_book method adds a new book object to the database. It first establishes a connection to the database,
    # and then inserts the title, author, and quantity of the book using a SQL INSERT statement. If the insertion
    # is successful, it prints a message to the console indicating that the book was added successfully.
    # If the insertion fails, it prints an error message and rolls back the transaction.
    def add_book(self, book_to_add):
        connection = self.connection_db()
        cursor = connection.cursor()
        try:
            connection.execute('''INSERT INTO books (title, author, quantity) VALUES (?, ?, ?)''',
                                        (book_to_add.title, book_to_add.author, book_to_add.qty))
            connection.commit()
            print("─────────────────────────────────────────────────────────")
            print(f"{YELLOW}Book added to database succesfully.{WHITE}")
        except sqlite3.Error as e:
            print(f"Unable to add {book_to_add.title} to {e}")
            connection.rollback()
            raise e
        connection.close()


    #T his method updates the record of a book in the database by allowing the user to select which column to
    # update (Title, Author or Quantity) and providing a new value for that column.
    def update_book(self, id):
        connection = self.connection_db()
        cursor = connection.cursor()
        loop_boolean = True
        # Fetching book of certain id from database
        cursor.execute('''SELECT * FROM books WHERE id=?''', (id,))
        content = cursor.fetchall()
        # If the SELECT statement returns no record, prints a message indicating that no book was found under that id.
        if not content:
            print("─────────────────────────────────────────────────────────")
            print(f"{YELLOW}No book found under ID:{WHITE} {GREEN}({id}){WHITE}")
        # Printing results using tabulate libary
        # If a record is found, the method enters an infinite loop that displays the current record using the
        # tabulate library and prompts the user to select which column to update.
        else:
            while loop_boolean:
                cursor.execute('''SELECT * FROM books WHERE id=?''', (id,))
                content = cursor.fetchall()
                headers = ['ID', 'Title', 'Author', 'Qty']
                print(tabulate(content, headers=headers, tablefmt='fancy_grid'))

                print("Which row do you want to edit?: ")
                print(f"{YELLOW}1{WHITE} - Title")
                print(f"{YELLOW}2{WHITE} - Author")
                print(f"{YELLOW}3{WHITE} - Quantity")
                print(f"{YELLOW}0{WHITE} - Main Menu")
                user_input = user_int_input("1")
                # method prompts for a new value for the book title, updates the record, commits the changes,
                # prints a success message and exits the infinite loop.
                if user_input == 1:
                    print("─────────────────────────────────────────────────────────")
                    new_value = input(f"Enter the new title {BOLD}(leave blank to keep current value){WHITE}: ")
                    if new_value:
                        cursor.execute('''UPDATE books SET title=? WHERE id=?''', (new_value,id))
                        connection.commit()
                        print("─────────────────────────────────────────────────────────")
                        print(f"{GREEN}Reckord updateed successfully.{WHITE}")
                # method prompts for a new value for the book author, updates the record, commits the changes,
                # rints a success message and exits the infinite loop.
                elif user_input == 2:
                    print("─────────────────────────────────────────────────────────")
                    new_value = input(f"Enter the new author {BOLD}(leave blank to keep current value){WHITE}: ")
                    if new_value:
                        cursor.execute('''UPDATE books SET author=? WHERE id=?''', (new_value,id))
                        connection.commit()
                        print("─────────────────────────────────────────────────────────")
                        print(f"{GREEN}Reckord updateed successfully.{WHITE}")
                # method prompts for a new value for the book author, updates the record, commits the changes,
                # prints a success message and exits the infinite loop.
                elif user_input == 3:
                    while True:
                        try:
                            print("─────────────────────────────────────────────────────────")
                            new_value = int(input("Enter the new 'Quantity': "))
                            if new_value:
                                cursor.execute('''UPDATE books SET quantity=? WHERE id=?''', (new_value, id))
                                connection.commit()
                                print("─────────────────────────────────────────────────────────")
                                print(f"{GREEN}Reckord updateed successfully.{WHITE}")
                            else:
                                connection.rollback()
                                break
                        except ValueError:
                            print("─────────────────────────────────────────────────────────")
                            print(f"{RED}Wrong input. Please try again.{WHITE}")
                            break
                elif user_input == 0:
                    print("─────────────────────────────────────────────────────────")
                    print(f"{YELLOW}Procedure abandoned, return to Main Menu.{WHITE}")
                    main_menu()
                else:
                    print("─────────────────────────────────────────────────────────")
                    print(f"{RED}Wrong input. Please try again.{WHITE}")
        connection.close()

    # etrieves the book from the database and displays it in a table using the tabulate library, then prompts
    # the user to confirm deletion before executing the SQL DELETE command to remove the book from the database.
    # It also handles exceptions and rolls back the transaction if there's an error.
    def delete_book(self, id):
        # Establish a connection to the database and create a cursor object.
        connection = self.connection_db()
        cursor = connection.cursor()
        try:
            # Establish a connection to the database and create a cursor object.
            cursor.execute('''SELECT * FROM books WHERE id=?''', (id,))
            content = cursor.fetchall()
            # If no books are found, print a message to the user and exit the method.
            if not content:
                print("─────────────────────────────────────────────────────────")
                print(f"{YELLOW}No book found under ID:{WHITE} {GREEN}({id}){WHITE}")
            # If books are found, print their details using the tabulate library, and delete the book from the database.
            else:
                headers = ['ID', 'Title', 'Author', 'Qty']
                print(tabulate(content, headers=headers, tablefmt='fancy_grid'))
                connection.execute('''DELETE FROM books WHERE id=?''', (id,))
                connection.commit()
                print(f"{GREEN}Book record #({id}) deleted succesfully.{WHITE}")
        # If an error occurs, print an error message and roll back the transaction..
        except sqlite3.Error as e:
            print(f"{RED}Unable to delete record #({id}) : {e}{WHITE}")
            connection.rollback()
            raise e
        # Close the database connection.
        connection.close()


    # The search_books method is responsible for searching for books in the database. It first takes user input
    # and uses spaCy to process the input for better matching. It filters out stop words and takes only nouns,
    # proper nouns, adjectives, verbs and adpositions from the input.
    def search_books(self):
        user_input = user_string_input(0)
        temporary_words = []

        connection = self.connection_db()
        cursor = connection.cursor()

        # Usimg spacy for betther match
        nlp = spacy.load('en_core_web_sm')
        phrase = nlp(user_input)

        for word in phrase:
            # Spacys english model treats "the" as a stop word and does not assign a part of speech tag to it.
            if word.pos_ in ['NOUN', 'PROPN', 'ADJ', 'VERB', 'ADP'] or word.text.lower()== 'the':
                temporary_words.append(word.text.lower())

        # Then, it checks whether the input contains any digits. If it does, it searches for books with a matching ID,
        # otherwise it searches for books with matching titles or authors. The search query is built by concatenating a
        # list of search conditions using the join() method with " OR " as the separator.
        if any(char.isdigit() for char in user_input):
            looking_for = "SELECT * FROM books WHERE id=?"
            # The filter() method is used to filter out non-digit characters from the string user_input.
            # Creates an iterator that filters out elements from a sequence that do not satisfy a certain condition.
            # In this case, the condition is checking if the character is a digit using the str.isdigit() method.
            # The filter() function returns an iterator with only the digits in the string.
            cursor.execute(looking_for, (int(''.join(filter(str.isdigit, user_input))),))
        else:
            looking_for = "SELECT * FROM books WHERE " + " OR ".join([
                f"LOWER(title) LIKE '%{word}%' OR LOWER(author) LIKE '%{word}%'" for word in temporary_words])
            cursor.execute(looking_for)
        results = cursor.fetchall()
        # Printing results using tabulate library
        headers = ['ID', 'Title', 'Author', 'Qty']
        print(tabulate(results, headers=headers, tablefmt='fancy_grid'))
        connection.close()

    # It is being used to ensure that the database connection is properly closed.
    # The method first attempts to establish a connection to the database and then closes it using the close() method.
    # If an error occurs while attempting to close the database, the method raises an exception.
    def __del__(self):
        try:
            connection = self.connection_db()
            connection.close()
        except sqlite3.Error as e:
            print(f"Unable to close database {e}")
            raise e
#──────────────────────────────────────────────────────

# ═════════════════════ Functions ═════════════════════
# function that prompts the user for information to create a new Book object. The function is taking the user input
# for the book's title, author, and qty and returning a new Book object with that information.
# The user_string_input function is being used to get the title and author,
# while the user_int_input function is being used to get the quantity.
def enter_book():
    new_book = Book(title=user_string_input(1),
                    author=user_string_input(2),
                    qty = user_int_input("4"))
    return new_book
#──────────────────────────────────────────────────────

# This function takes a string argument menu_string which is used as a key to retrieve the prompt and error messages
# from a dictionary dict_of_strings. It then prompts the user to enter an integer value using the prompt message,
# validates the input to ensure it is an integer, and returns the integer value. If the input is not a valid integer,
# it displays the error message from the dict_of_strings dictionary and calls the back_to_menu() function to prompt the
# user to return to the main menu.
def user_int_input(menu_string):
    dict_of_strings = {
        "1" : ["Enter your choice: ", "Invalid choice. Please enter a number."],
        "2" : ["Enter the ID of the item you wish to update: ", "Invalid entry. Please enter book ID."],
        "3" : ["Enter the ID of the item you wish to delete: ", "Invalid entry. Please enter book ID."],
        "4" : ["Enter the quantity of the book: ", "Wrong input. Please try again"]
    }
    while True:
        try:
            print("─────────────────────────────────────────────────────────")
            user_choice = int(input(f"{dict_of_strings[menu_string][0]}"))

            return user_choice
        except ValueError:
            print("─────────────────────────────────────────────────────────")
            print(f"{RED}{dict_of_strings[menu_string][1]}{WHITE}")
            back_to_menu()
        except TypeError:
            print("─────────────────────────────────────────────────────────")
            print(f"{RED}{dict_of_strings[menu_string][1]}{WHITE}")
            back_to_menu()
#──────────────────────────────────────────────────────

# The function continuously prompts the user to enter the input until the user provides a non-empty string.
# If the user enters an empty string, the back_to_menu() function is called to bring the user back to the main menu.
def user_string_input(to_insert):
    # The insert_string list contains messages that prompt the user to enter input of the appropriate type.
    insert_string = ["What would you like to find",
                     "Enter the title",
                     "Enter the author"]
    #user_counter = 0
    while True:
        print("─────────────────────────────────────────────────────────")
        user_input = input(f"{insert_string[to_insert]}: ")
        if user_input != "":
            break
        else:
            back_to_menu()
    # The function returns the user input string.
    return user_input
#──────────────────────────────────────────────────────

# The back_to_menu() function is used to prompt the user whether they would like to return to the main menu, and
# if yes, to call the main_menu() function. If the user inputs 'Y' or 'YES', the function prints a message indicating
# that the procedure has been abandoned and returns to the main menu.
def back_to_menu():
    print("─────────────────────────────────────────────────────────")
    user_input = input(f"Would you like to back to Main Menu ({YELLOW}Y{WHITE}es / {YELLOW}N{WHITE}o)?: ").upper()
    if user_input == 'Y' or user_input == 'YES':
        print("─────────────────────────────────────────────────────────")
        print(f"{YELLOW}Procedure abandoned, return to Main Menu.{WHITE}")
        main_menu()
#──────────────────────────────────────────────────────

# This function connects to a specified SQLite database, retrieves all the books in the 'books' table,
# and then uses the tabulate library to print the table in a nicely formatted grid format with headers.
# It takes one argument, which is the path to the SQLite database.
def print_from_database(database):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    cursor.execute('''SELECT * FROM books''')
    content = cursor.fetchall()

    # Printing results using tabulate libary
    headers = ['ID', 'Title', 'Author', 'Quantity']
    print(tabulate(content, headers=headers, tablefmt='fancy_grid'))
    connection.close()
#──────────────────────────────────────────────────────

# Main Menu function
def main_menu():
    while True:
        print("─────────────────────────────────────────────────────────")
        print(f"{YELLOW}1{WHITE} - Enter book")
        print(f"{YELLOW}2{WHITE} - Update book")
        print(f"{YELLOW}3{WHITE} - Delete book")
        print(f"{YELLOW}4{WHITE} - Search books")
        print(f"{YELLOW}5{WHITE} - Show books")
        print(f"{YELLOW}0{WHITE} - Exit")
        menu = user_int_input("1")
        if menu == 1:
            store_database.add_book(enter_book())
        if menu == 2:
            store_database.update_book(user_int_input("2"))
        elif menu == 3:
            store_database.delete_book(user_int_input("3"))
        elif menu == 4:
            store_database.search_books()
        elif menu == 5:
            print_from_database('ebookstore.db')
        elif menu == 0:
            print(f"{YELLOW}Good Bye!{WHITE}")
            exit()
        else:
            pass
#──────────────────────────────────────────────────────

# ═════════════════════ Main Prog ═════════════════════
store_database = Store('ebookstore.db')
main_menu()






