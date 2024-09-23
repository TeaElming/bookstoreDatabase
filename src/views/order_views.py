from datetime import datetime, timedelta

class OrderViews:
    def print_cart_contents(self, cart_items):
        print("*" * 70)
        if not cart_items:
            print("Your cart is empty.")
        else:
            print("Your cart contents:")
            for item in cart_items:
                print(f"Title: {item['title']} - Quantity: {item['quantity']} - Price per item: ${item['price']}")
            total_price = sum(item['price'] * item['quantity'] for item in cart_items)
            print(f"Total Price: ${total_price}")
        print("*" * 70)

    def display_checkout_confirmation(self, order_details, created_date):
        print("*" * 70)
        print("Thank you for your purchase!")
        print("Order Details:")
        for detail in order_details:
            print(f"Title: {detail['title']} - Quantity: {detail['quantity']} - Total Price: ${detail['amount']}")
        if order_details:
            print(f"Shipping to: {order_details[0]['shipAddress']}, {order_details[0]['shipCity']}, {order_details[0]['shipZip']}")

        estimated_delivery_date = created_date + timedelta(days=7)
        print(f"Estimated Delivery Date: {estimated_delivery_date.strftime('%Y-%m-%d')}")
        print("*" * 70)
