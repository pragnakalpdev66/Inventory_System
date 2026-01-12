#       # product
# from operations import add_or_update_product

# print(" Inventory System")
# print("\n Add Or Update product")

# name = input("Enter product name: ")
# price = float(input("Enter price: "))
# stock = int(input("Enter stock: "))

# add_or_update_product(name, price, stock)

#       # supplier
# from operations import add_supplier

# print(" Manage Supplier ")

# name = input("Enter supplier name: ")
# email = input("Enter email (optional): ")

# add_supplier(name, email)

        # record purchase
from operations import record_purchase

print(" Record Inventory Purchases ")

product = input("Enter product name: ")
supplier = input("Enter supplier name: ")
quantity = int(input("Enter quantity: "))

record_purchase(product, supplier, quantity)

#        # create order
# from operations import create_order

# print(" Customer Orders")

# product = input("Enter product name: ")
# quantity = int(input("Enter quantity: "))

# create_order(product, quantity)

#         #order summary
# from operations import daily_order_summary

# daily_order_summary()

        #supplier summary
from operations import supplier_purchase_summary

supplier_purchase_summary()

#         #cleanup old orders
# from operations import cleanup_old_orders

# cleanup_old_orders()
