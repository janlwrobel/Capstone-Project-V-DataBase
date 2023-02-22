# Book Inventory

This project is a command-line application for managing a book inventory.

## Installation

To use this program, you will need to have Python 3 installed on your computer. You will also need to install the following libraries:

```bash
pip install spacy
pip install tabulate
```

Or you can: 

1. Clone the repository.
2. Install the required libraries using `pip install -r requirements.txt`.

### Libraries Used

The following libraries are used in this project:

- `sqlite3`: Provides an interface to work with SQLite databases.
- `spacy`: A natural language processing library used for searching books.
- `tabulate`: A library used for displaying the book inventory in a formatted table.

## Download the Source Code

You can download the source code from the GitHub repository.

## Configure Spacy

Before you can use the application, you need to configure the spacy library by downloading the English language model. 
To do this, run the following command:


```bash
python -m spacy download en_core_web_sm
```
## Run the Application

To run the application, navigate to the directory where you downloaded the source code and run the following command:

```bash
python bookstore.py
```

## Usage

Once you have the application running, you will be presented with a menu that allows you to add, update, delete, and search for books in the inventory.

### Adding a Book
To add a book to the inventory, select the "Add a Book" option from the main menu and enter the title, author, and quantity of the book.

### Updating a Book
To update a book in the inventory, select the "Update a Book" option from the main menu and enter the ID of the book you want to update. You will then be presented with a menu that allows you to update the title, author, or quantity of the book.

### Deleting a Book
To delete a book from the inventory, select the "Delete a Book" option from the main menu and enter the ID of the book you want to delete.

### Searching for a Book
To search for a book in the inventory, select the "Search for Books" option from the main menu and enter the keyword you want to search for. The application will search the book's title and author fields for a match and display the results in a table.

### Viewing the Entire Inventory
To view the entire inventory, select the "View Entire Inventory" option from the main menu. The application will display a table with all the books in the inventory.

### Exiting the Application
To exit the application, select the "Exit" option from the main menu.

