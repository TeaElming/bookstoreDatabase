from controllers.connectDB import DB_connection
from mysql.connector import errors as mysql_errors

import datetime
import random
class OrdersDB(DB_connection):
    def add_to_cart(self, userid, isbn):
      qty = int(input("How many do you want to add: "))
      if self.cart_item_exists(userid, isbn):
          self.update_cart_item(userid, isbn, qty)
      else:
          self.cart_query(userid, isbn, qty)

    def cart_item_exists(self, userid, isbn):
      query = "SELECT COUNT(*) FROM cart WHERE userid = %s AND isbn = %s"
      self.cursor.execute(query, (userid, isbn))
      return self.cursor.fetchone()[0] > 0

    def update_cart_item(self, userid, isbn, qty):
      query = "UPDATE cart SET qty = qty + %s WHERE userid = %s AND isbn = %s"
      self.cursor.execute(query, (qty, userid, isbn))
      self.connection.commit()
      print("Cart item quantity updated successfully.")


    def cart_query(self, userid, isbn, qty):
        query = "INSERT INTO cart (userid, isbn, qty) VALUES (%s, %s, %s)"
        try:
            self.cursor.execute(query, (userid, isbn, qty))
            self.connection.commit()
            print("Added to cart successfully.")
        except mysql_errors.Error as e:
            print(f"Database error: {e}")

    def create_order(self, userid):
        ship_address, ship_city, ship_zip = self.get_member_address(userid)
        ono = self.generate_unique_order_number()
        created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.order_query(userid, ono, created, ship_address, ship_city, ship_zip)
        return ono

    def get_member_address(self, userid):
        query = "SELECT address, city, zip FROM members WHERE userid = %s"
        self.cursor.execute(query, (userid,))
        result = self.cursor.fetchone()
        return result if result else (None, None, None)

    def generate_unique_order_number(self):
        while True:
            ono = random.randint(1, 2147483647)
            if not self.order_number_exists(ono):
                return str(ono)

    def order_number_exists(self, ono):
        query = "SELECT COUNT(*) FROM orders WHERE ono = %s"
        self.cursor.execute(query, (ono,))
        return self.cursor.fetchone()[0] > 0


    def order_detail_exists(self, ono, isbn):
        query = "SELECT EXISTS(SELECT 1 FROM odetails WHERE ono = %s AND isbn = %s)"
        self.cursor.execute(query, (ono, isbn))
        exists = self.cursor.fetchone()[0]
        return exists == 1

    def order_query(self, userid, ono, created, ship_address, ship_city, ship_zip):
        query = "INSERT INTO orders (userid, ono, created, shipAddress, shipCity, shipZip) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (userid, ono, created, ship_address, ship_city, ship_zip))
        self.connection.commit()

    def write_order_details(self, ono, cart_items):
        for item in cart_items:
            isbn, qty = item['isbn'], item['quantity']
            amount = self.calculate_amount(isbn, qty)
            if self.order_detail_exists(ono, isbn):
                self.update_order_detail(ono, isbn, qty)
            else:
                self.order_detail_query(ono, isbn, qty, amount)

    def update_order_detail(self, ono, isbn, qty):
      query = "UPDATE odetails SET qty = qty + %s WHERE ono = %s AND isbn = %s"
      try:
          self.cursor.execute(query, (qty, ono, isbn))
          self.connection.commit()
          print("Order detail quantity updated successfully.")
      except mysql_errors.Error as e:
          print(f"Failed to update order detail: {e}")


    def calculate_amount(self, isbn, qty):
        query = "SELECT price FROM books WHERE isbn = %s"
        self.cursor.execute(query, (isbn,))
        result = self.cursor.fetchone()
        return result[0] * qty if result else 0

    def order_detail_query(self, ono, isbn, qty, amount):
        query = "INSERT INTO odetails (ono, isbn, qty, amount) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (ono, isbn, qty, amount))
        self.connection.commit()

    def clear_cart(self, userid):
        query = "DELETE FROM cart WHERE userid = %s"
        self.cursor.execute(query, (userid,))
        self.connection.commit()

    def get_cart_items(self, userid):
        query = "SELECT b.isbn, b.title, c.qty AS quantity, b.price FROM cart c JOIN books b ON c.isbn = b.isbn WHERE c.userid = %s"
        self.cursor.execute(query, (userid,))
        return [{'isbn': row[0], 'title': row[1], 'quantity': row[2], 'price': row[3]} for row in self.cursor.fetchall()]

    def get_order_details(self, ono):
        query = "SELECT b.title, od.qty AS quantity, od.amount, o.shipAddress, o.shipCity, o.shipZip FROM odetails od JOIN books b ON od.isbn = b.isbn JOIN orders o ON od.ono = o.ono WHERE od.ono = %s"
        self.cursor.execute(query, (ono,))
        return [{'title': row[0], 'quantity': row[1], 'amount': row[2], 'shipAddress': row[3], 'shipCity': row[4], 'shipZip': row[5]} for row in self.cursor.fetchall()]

    def process_checkout(self, userid):
      cart_items = self.get_cart_items(userid)
      if not cart_items:
          print("Your cart is empty. Cannot proceed with checkout.")
          return None, "Your cart is empty.", None

      try:
          self.connection.rollback()
          print("Starting transaction for checkout")
          self.connection.start_transaction()

          ono = self.create_order(userid)
          if not ono:
              raise Exception("Failed to create order.")

          self.write_order_details(ono, cart_items)
          self.clear_cart(userid)

          print("Attempting to commit the transaction")
          self.connection.commit()

          order_details = self.get_order_details(ono)
          created_date = datetime.datetime.now()  # Fetch actual creation date if necessary
          total_amount = sum(item['price'] * item['quantity'] for item in cart_items)
          message = f"Checkout complete. Total amount: ${total_amount}. Thank you for your purchase!"
          print(message)
          return order_details, message, created_date
      except Exception as e:
          print(f"Checkout failed due to error: {e}")
          self.connection.rollback()
          return None, "Checkout failed due to a database error.", None
