import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

class DB_connection:
  def __init__(self):
    load_dotenv()
    try:
      self.connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
      )
      self.cursor = self.connection.cursor()
      print("Successfully connected to the database.")
    except Error as e:
      print(f"Error connecting to the database: {e}")
      exit(1)

  def close_connection(self):
    if self.connection.is_connected():
      self.cursor.close()
      self.connection.close()
      print("MySQL connection is closed.")