from getpass import getpass

class MemberViews:
  def get_member_registration_details(self):
        print("Please enter your details to register:")
        fname = input("First Name: ")
        lname = input("Last Name: ")
        address = input("Address: ")
        city = input("City: ")
        zip_code = input("Zip Code: ")
        phone = input("Phone Number: ")
        email = input("Email: ")
        password = getpass("Password: ")
        return fname, lname, address, city, zip_code, phone, email, password

  def get_member_login_details(self):
    email = input("Email: ")
    password = getpass("Password: ")
    return email, password