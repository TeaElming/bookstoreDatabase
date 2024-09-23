cursor.execute()
connection.commit()

### How to get all the information about the tables
query = """
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
ORDER BY ORDINAL_POSITION
"""
values = ('your_database_name', 'members')  # Replace 'your_database_name' with the name of your database

cursor.execute(query, values)

#### Fetch all rows from the cursor
columns = cursor.fetchall()

#### Display column information
for column in columns:
    print(f"Column Name: {column[0]}, Data Type: {column[1]}, Is Nullable: {column[2]}, Default: {column[3]}")


### How to create new row (example)
query = "INSERT INTO members (fname, lname, email) VALUES (%s, %s, %s)"
values = ("John", "Doe", "john.doe@example.com")
cursor.execute(query, values)
connection.commit()

### How to update a row
query = "UPDATE members SET fname = %s, lname = %s WHERE email = %s"
values = ("Jane", "Doe", "john.doe@example.com")
cursor.execute(query, values)
connection.commit()

### How to search for a (one) member
query = "SELECT * FROM members WHERE email = %s"
values = ("john.doe@example.com",)
cursor.execute(query, values)

member = cursor.fetchone()  # fetchone() retrieves a single row
if member:
    print(member)  # member will be None if there are no rows found
else:
    print("No member found.")

### How to search for all books based on title
query = "SELECT * FROM books WHERE title LIKE %s"
values = ("%partial_book_title%",)  # Replace 'partial_book_title' with the search term, e.g. 'Harry Potter'
cursor.execute(query, values)

books = cursor.fetchall()  # fetchall() retrieves all rows of a query result
for book in books:
    print(book)

