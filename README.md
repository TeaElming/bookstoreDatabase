# A3 Book Store
## Project Overview

The A3 Book Store is a terminal-based Python application that allows users to browse, search, and purchase books from an online bookstore. The system provides member registration, login, and checkout functionalities, with a MySQL database backend for managing members, books, and orders. The application follows an MVC (Model-View-Controller) design, ensuring scalability and maintainability of the codebase.

## Core Features

1. Member Registration and Login:
* Users can register as a new member by providing their personal details.
* Registered users can log in using their credentials.
* Once logged in, members have access to additional features such as browsing books, searching, and

2. checking out.
* Book Browsing and Searching:
* Browse by Subject: Users can view a list of books by selecting a subject from the available categories.
* Search by Author/Title: Users can search for books by entering the author’s name or a word in the book's title.

3. Shopping Cart and Checkout:
* Add books to a cart after browsing or searching.
* View and manage items in the cart before proceeding to checkout.
* Proceed through the checkout process, where order details are stored and displayed to the user.

4. Order Management:
* Order details are tracked and stored, including items, shipping address, and total amount.
* Each user’s cart is cleared after a successful checkout.

## Technology Stack

### Backend

* Python: The main programming language used to develop the application.
* MySQL: The relational database used to store member details, book information, cart, and order data.
* Sequelize: An ORM (Object-Relational Mapper) used to manage database interactions.
* bcrypt: A Python library for password hashing to securely store user passwords.

### Key Modules and Components

* DB_connection: Handles database connectivity, using MySQL to interact with members, books, and orders.
* MemberDB: Manages member registration, login, and password hashing.
* OrdersDB: Handles cart management, order creation, and checkout.
* BrowserDB: Handles browsing and searching of books by subject, author, or title.
* Views: Provides a user interface for interaction with the system via the terminal.

## Database Structure

The application uses the following database tables:

1. members: Stores member details.
``userid`` (Primary Key), ``fname``, ``lname``, ``address``, ``city``, ``zip``, ``phone``, ``email``, ``password``

2. books: Stores book details.
``isbn`` (Primary Key), ``author``, ``title``, ``price``, ``subject``

3. orders: Stores order information for users.
``userid`` (Foreign Key), ``ono`` (Primary Key), ``created``, ``shipAddress``, ``shipCity``, ``shipZip``

4. odetails: Stores details for each order.
``ono`` (Foreign Key), ``isbn`` (Foreign Key), ``qty``, ``amount``

5. cart: Stores temporary cart information before checkout.
``userid`` (Foreign Key), ``isbn`` (Foreign Key), ``qty``

## How to Use the Application
1. Set Up the Database:
* Ensure you have a MySQL database configured with the required tables.
* Update the .env file with your MySQL database credentials:
````
DB_HOST=your-db-host
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=your-db-name
````
2. Run the Application
* Run the main Python application to start the terminal-based interface:

````
python app.py
````

3. Member Registration:
* When prompted, select the option to register as a new member by providing your personal details (name, address, etc.).

4. Member Login:
* Log in using your email and password to gain access to the bookstore.

5. Browsing and Searching:
* After login, select the "Browse by Subject" or "Search by Author/Title" options to explore the available books.
* View book details and add books to your cart.

6. Checkout:
* After adding books to your cart, proceed to checkout where you can view order details and complete the purchase.

## Installation

Clone the Repository:

``
git clone https://github.com/your-username/A3_book_store.git
cd A3_book_store
``

2. Install Dependencies: Ensure you have all required dependencies installed. If not, install them using:

``
pip install -r requirements.txt
``

3. Set Up Database: Create and configure the MySQL database, and ensure the necessary environment variables are set in .env.

4. Run the Application: Run the main application:
``
python app.py
``

## Additional Features

* Pagination for Large Datasets: When browsing or searching, results are paginated to show a limited number of items at once, with options to view the next page of results.
* Cart Management: Users can add, view, and manage items in their cart before checking out.
* Secure Password Handling: User passwords are securely hashed using bcrypt before being stored in the database.

## Future Improvements

* Enhanced Search Features: Add advanced filters for searching by price range, publication date, or genre.
* Admin Interface: Implement an administrative interface for managing books and members.
* Email Notifications: Send order confirmation and receipt emails to users after a successful checkout.