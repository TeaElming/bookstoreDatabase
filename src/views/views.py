import textwrap


class Views:

  def calculate_padding(self, text):
    total_width = 70
    padding = (total_width - len(text) - 6) // 2 # 3 asterixes on each side => 3*2 = 6
    return padding

  def calculate_right_padding(self, text):
    padding = self.calculate_padding(text)
    right_padding = padding if (70 - len(text) - 6) % 2 == 0 else padding + 1
    return right_padding


  def starting_menu(self):
    top_bottom_border = "*" * 70
    empty_line = "*" * 3 + " " * (70 - 6) + "*" * 3
    title = "Welcome to the Online Book Store"
    padding = self.calculate_padding(title)
    right_padding = self.calculate_right_padding(title)
    title_line = "*" * 3 + " " * padding + title + " " * right_padding + "*" * 3

    menu_content = [
    top_bottom_border,
    empty_line,
    title_line,
    empty_line,
    top_bottom_border,
    "1. New Member Registration",
    "2. Member Login",
    "q. Quit\n"
    ]

    return '\n'.join(menu_content)


  def member_menu(self):
    top_bottom_border = "*" * 70
    empty_line = "*" * 3 + " " * (70 - 6) + "*" * 3
    title = "Welcome to the Online Book Store"
    sub_title = "Member Menu"
    padding = self.calculate_padding(title)
    sub_padding = self.calculate_padding(sub_title)
    right_padding = self.calculate_right_padding(title)
    sub_right_padding = self.calculate_right_padding(sub_title)
    title_line = "*" * 3 + " " * padding + title + " " * right_padding + "*" * 3
    sub_title_line = "*" * 3 + " " * sub_padding + sub_title + " " * sub_right_padding + "*" * 3

    menu_content = [
      top_bottom_border,
      empty_line,
      title_line,
      sub_title_line,
      empty_line,
      top_bottom_border,
      "1. Browse by Subject",
      "2. Search by Author/Title",
      "3. Check Out",
      "q. Log Out\n"
    ]
    return '\n'.join(menu_content)

  def print_subjects(self, subjects):
    numbered_subjects = [f"{i+1}. {subject} ({count} books)" for i, (subject, count) in enumerate(subjects)]
    print('\n'.join(numbered_subjects))

  def print_books(self, books):
    header = "{:<12} {:<25} {:<80} {:<10} {}".format("ISBN", "Author", "Title", "Price", "Subject")
    separator = "-" * 145

    print(separator)
    print(header)
    print(separator)

    for book in books:
      isbn, author, title, price, subject = book

      # Wrap long titles separately to fit within the specified width
      wrapped_title = textwrap.wrap(title, width=75)

      # Print each part of the wrapped title separately
      for index, line in enumerate(wrapped_title):
        if index == 0:  # First line of the wrapped title
          book_info = "{:<12} {:<25} {:<80} {:<10} {}".format(isbn, author, line, str(price), subject)
          print(book_info)
        else:  # Subsequent lines of the wrapped title
          book_info = "{:<12} {:<25} {:<80} {:<10} {}".format("", "", line, "", "")
          print(book_info)

      print(separator)

  def search_author_or_title(self):
    print("1. Search by Author")
    print("2. Search by Title")
    print("3. Return to Main Menu")

    choice = input("Enter your choice: ")
    return choice


  def take_book_action(self):
    print("Press 'n' amd ENTER to view the next page of books")
    print("OR")
    print("Type the ISBN of the book you want to add to your cart and press ENTER")
    print("OR)")
    print("Press ENTER to return to the main menu")

    choice = input("Enter your choice: ")
    return choice

  def print_book_details(self, book_details):
        if book_details:
            print("*" * 70)
            print(f"ISBN: {book_details['isbn']}")
            print(f"Title: {book_details['title']}")
            print(f"Author: {book_details['author']}")
            print(f"Price: ${book_details['price']}")
            print(f"Subject: {book_details['subject']}")
            print("*" * 70)
        else:
            print("Book details not available.")