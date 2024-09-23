from controllers.connectDB import DB_connection

class BrowserDB(DB_connection):
  def __init__(self):
    super().__init__()
    self.current_subject = None
    self.current_title_substring = None
    self.current_author_substring = None
    self.page = 0
    self.page_size = 2  # Default page size, can be adjusted as needed

  def reset_pagination(self):
    """Resets pagination settings for a new query."""
    self.page = 0

  def set_pagination_subject(self, subject):
    """Sets the subject for pagination."""
    self.current_subject = subject
    self.reset_pagination()

  def set_pagination_title_substring(self, title_substring):
    """Sets the title substring for pagination."""
    self.current_title_substring = title_substring
    self.reset_pagination()

  def set_pagination_author_substring(self, author_substring):
    """Sets the author substring for pagination."""
    self.current_author_substring = author_substring
    self.reset_pagination()

  def next_page(self):
    """Generic method to move to the next page based on the current query context."""
    if self.current_subject:
      return self.show_books_for_subject(paginate=True)
    elif self.current_title_substring:
      return self.search_title(paginate=True)
    elif self.current_author_substring:
      return self.search_author(paginate=True)

  def list_all_subjects(self):
    query = """
    SELECT subject, COUNT(*) as book_count
    FROM books
    GROUP BY subject
    ORDER BY subject ASC
    """
    self.cursor.execute(query)
    subjects = self.cursor.fetchall()
    return subjects

  def show_books_for_subject(self, subject_index, paginate=False):
    subjects = self.list_all_subjects()

    if not subjects:
      print("No subjects found.")
      return

    if not 0 < subject_index <= len(subjects):
      print("Invalid subject index.")
      return

    # Get the subject from the list based on the index
    chosen_subject = subjects[subject_index - 1][0]

    query = """
    SELECT isbn, author, title, price, subject
    FROM books
    WHERE books.subject = %s
    ORDER BY author ASC
    LIMIT 2 OFFSET %s
    """
    offset = self.page * self.page_size
    self.cursor.execute(query, (chosen_subject, offset))
    books = self.cursor.fetchall()

    count_query = "SELECT COUNT(*) FROM books WHERE subject = %s"
    self.cursor.execute(count_query, (chosen_subject,))
    count_result = self.cursor.fetchone()
    total_books = count_result[0]

    message = f"There are {total_books} books on the subject '{chosen_subject}'."
    self.page += 1
    return message, books

  def search_title(self, paginate=False):
    if not paginate:
      self.set_pagination_title_substring(input("Enter a word to search in the title: "))
    query = """
    SELECT isbn, author, title, price, subject
    FROM books
    WHERE title LIKE %s
    ORDER BY title
    LIMIT 3 OFFSET %s
    """
    offset = self.page * 3
    self.cursor.execute(query, ('%' + self.current_title_substring + '%', offset))
    result = self.cursor.fetchall()
    self.page += 1
    return result

  def search_author(self, paginate=False):
    if not paginate:
      self.set_pagination_author_substring(input("Enter a name to search for the author's name: "))
    query = """
    SELECT isbn, author, title, price, subject
    FROM books
    WHERE author LIKE %s
    ORDER BY author
    LIMIT 3 OFFSET %s
    """
    offset = self.page * 3
    self.cursor.execute(query, ('%' + self.current_author_substring + '%', offset))
    result = self.cursor.fetchall()
    self.page += 1
    return result

  def get_book_details(self, isbn):
    """Retrieves details of a book based on its ISBN."""
    query = """
    SELECT isbn, title, author, price, subject
    FROM books
    WHERE isbn = %s
    """
    self.cursor.execute(query, (isbn,))
    book_details = self.cursor.fetchone()

    if book_details:
      return {
        'isbn': book_details[0],
        'title': book_details[1],
        'author': book_details[2],
        'price': book_details[3],
        'subject': book_details[4]
      }
    else:
      print(f"Book with ISBN {isbn} not found.")
