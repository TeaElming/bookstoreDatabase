from controllers.connectDB import DB_connection
import bcrypt

class MemberDB(DB_connection):
  def hash_password(self, password):
    """Hash a password for storing."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

  def register_new_member(self, fname, lname, address, city, zip_code, phone, email, password):
    if self.email_exists(email):
      print("Error: This email is already registered.")
      return

    hashed_password = self.hash_password(password)
    query = """
    INSERT INTO members (fname, lname, address, city, zip, phone, email, password)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
      self.cursor.execute(query, (fname, lname, address, city, zip_code, phone, email, hashed_password))
      self.connection.commit()
      print("Member registered successfully.")
    except self.Error as e:
      print(f"Error inserting member into database: {e}")

  def login_member(self, email, password):
    query = "SELECT userid, password FROM members WHERE email = %s"
    self.cursor.execute(query, (email,))
    result = self.cursor.fetchone()

    if result:
        userid, stored_password = result
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            print("Login successful.")
            return userid
        else:
            print("Login failed: Incorrect password.")
    else:
        print("Login failed: User not found.")
    return None


  def email_exists(self, email):
    # Query to check if the email exists in the members table
    query = "SELECT COUNT(*) FROM members WHERE email = %s"
    self.cursor.execute(query, (email,))
    result = self.cursor.fetchone()
    # If the result is greater than 0, the email already exists
    return result[0] > 0