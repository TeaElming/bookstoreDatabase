members: fname, lname, address, city, zip, phone, email, userid (PK), password

books: isbn (PK), auhtor, title, price, subject

orders: userid (FK), ono (PK), created, shipAddress, shipCity, shipZip

odetails: ono (FK), isbn (FK), qty, amount

cart: userid (FK), isbn (FK), qty