# 1. Inventory Management System
# Usecase:
# For small to medium-sized retail stores, keeping track of product inventory.

# Features:
# Classes for Products, Categories, and Transactions.
# Methods for adding/removing products, calculating total inventory value, and processing transactions.
# Use constructors to initialize product and transaction objects.
# Implement access modifiers to protect sensitive data like product cost.

print("Welcome to the Inventory Management System")

# define Product class
class Product:
    
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    # add quantity to product
    def add_quantity(self, quantity):
        self.quantity += quantity
        print(f"{quantity} {self.name} added to inventory")
    
    # remove quantity from product
    def remove_quantity(self, quantity):
        if self.quantity >= quantity:
            self.quantity -= quantity
            print(f"{quantity} {self.name} removed from inventory")
        else:
            print(f"Insufficient {self.name} in inventory")


# initialize empty list to store products
inventory = []

# create inventory class to manage products
class Inventory:
    def __init__(self):
        self.items = []
    
    # add product to inventory
    def add_product(self, product):
        self.items.append(product)
        print(f"{product.name} added to inventory")

    # remove product from inventory
    def remove_product(self, product):
        self.items.remove(product)
        print(f"{product.name} removed from inventory")

# create product objects
apple = Product("Apple", 0.50, 100)
banana = Product("Banana", 0.75, 100)
orange = Product("Orange", 1.00, 100)

print(f"{apple.price}")

# add quantity to products
apple.add_quantity(50)
# remove quantity from products
banana.remove_quantity(25)

# add products to inventory
inventory.append(apple)
inventory.append(banana)
inventory.append(orange)

# show inventory
for product in inventory:
    print(f"Product: {product.name} | Price: ${product.price} | Quantity: {product.quantity}")