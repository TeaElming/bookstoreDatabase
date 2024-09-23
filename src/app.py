from views.views import Views
from views.member_views import MemberViews
from views.order_views import OrderViews
from controllers.connectDB import DB_connection
from controllers.ordersDB import OrdersDB
from controllers.memberDB import MemberDB
from controllers.browseDB import BrowserDB
import os
from getpass import getpass


class App:
  def __init__(self):
    self.views = Views()
    self.membersView = MemberViews()
    self.orderViews = OrderViews()
    self.logged_in_user_id = None

  def setup_database_connection(self):
        print("Please enter your database connection details.")
        host = input("Database Host: ")
        user = input("Database User: ")
        password = input("Database Password: ")
        database = input("Database Name: ")

        # Set environment variables
        os.environ['DB_HOST'] = host
        os.environ['DB_USER'] = user
        os.environ['DB_PASSWORD'] = password
        os.environ['DB_NAME'] = database

  def initialize_database_connections(self):
        # Now that environment variables are set, initialize DB connections
        self.db = DB_connection()  # DB_connection must connect in a method called after env vars are set
        self.orders = OrdersDB()
        self.members = MemberDB()
        self.browser = BrowserDB()

  def run(self):
    self.setup_database_connection()
    self.initialize_database_connections()
    app_running = True
    while app_running:
        logged_in = False
        print(self.views.starting_menu())
        choice = input("Enter your choice: ")
        if choice == "1":
            registration_credentials = self.membersView.get_member_registration_details()
            self.members.register_new_member(*registration_credentials)

        elif choice == "2":
            login_credentials = self.membersView.get_member_login_details()
            user_id = self.members.login_member(*login_credentials)
            if user_id:
                logged_in = True
                self.logged_in_user_id = user_id
                print("User id: ", user_id)

        elif choice == "q":  # Option to quit the application
            print("Exiting the application.")
            app_running = False
            break  # Immediately exit the while loop

        while logged_in:
            print(self.views.member_menu())
            choice = input("Enter your choice: ")
            if choice == "1":
                self.view_books_by_subject()
            elif choice == "2":
                choice = self.views.search_author_or_title()
                if choice in ["1", "2"]:
                    print("Your choice was: ", choice)
                    if choice == "1":
                        books = self.browser.search_author()
                    elif choice == "2":
                        books = self.browser.search_title()
                    self.view_and_paginate_books(books)
            elif choice == "3":
                print("Check Out Time!")
                self.checkout()
            elif choice == "q":  # Log out
                if self.logged_in_user_id is not None:
                    self.orders.clear_cart(self.logged_in_user_id)
                    print("Your cart has been cleared.")
                logged_in = False
                self.logged_in_user_id = None
                print("You are now logged out.")
                break  # Added to ensure exiting the inner loop does not immediately exit the application

  def view_books_by_subject(self):
    subjects = self.browser.list_all_subjects()
    self.views.print_subjects(subjects)
    subject_index = int(input("Enter the number of the subject: "))
    message, books = self.browser.show_books_for_subject(subject_index, paginate=True)
    print(message)
    self.view_and_paginate_books(books)

  def view_and_paginate_books(self, books):
    while True:
      self.views.print_books(books)
      see_next = self.views.take_book_action()
      if see_next.lower() == 'n':
        books = self.view_next_page(books)
      elif see_next.isdigit() and len(see_next) in [10, 13]:
        self.handle_selected_book(see_next)
      else:
        break

  def handle_selected_book(self, isbn):
    book_details = self.browser.get_book_details(isbn)
    self.views.print_book_details(book_details) 
    action = input("Enter 'a' to add to cart, or any other key to return: ")
    if action.lower() == 'a':
      if self.logged_in_user_id is not None:
        self.orders.add_to_cart(self.logged_in_user_id, isbn)
        print("Book added to cart.")
      else:
        print("No user is currently logged in.")


  def view_next_page(self, books):
    if len(books) < 3:
      print("No more pages available.")
      return books
    return self.browser.next_page()

  def checkout(self):
    # Fetch cart items first to display them
    cart_items = self.orders.get_cart_items(self.logged_in_user_id)
    if not cart_items:
        print("Your cart is empty. Cannot proceed with checkout.")
        return

    # Display cart contents
    self.orderViews.print_cart_contents(cart_items)

    # Proceed with checkout process
    order_details, message, created_date = self.orders.process_checkout(self.logged_in_user_id)
    if not order_details:
        print("Checkout failed.")
        return

    # Display checkout confirmation with order details
    self.orderViews.display_checkout_confirmation(order_details, created_date)
    print(message)




mainApp = App()

mainApp.run()