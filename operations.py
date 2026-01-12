from db import get_connection

def log_error(e):
    with open("db_errors.log", "a") as f:
        f.write(str(e) + "\n")

# 1 Products
def add_or_update_product(name, price, stock=None):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT product_id FROM products WHERE name ILIKE %s", (name,))
        result = cur.fetchone()

        if result:
            cur.execute("UPDATE products SET price=%s WHERE name ILIKE %s", (price, name))
            print("Product price updated!")
        else:
            cur.execute("INSERT INTO products(name, price, stock) VALUES (%s,%s,%s)", (name, price, stock))
            print("Product added!!")

        conn.commit()
        conn.close()

    except Exception as e:
        log_error(e)
        print("Error saving product!!")

# 2 Suppliers
def add_supplier(name, email=None):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT supplier_id FROM suppliers WHERE name ILIKE %s", (name,))
        result = cur.fetchone()

        if result:
            print("Supplier already exists!")
        else:
            cur.execute("INSERT INTO suppliers(name, contact_email) VALUES (%s, %s)", (name, email))
            print("Supplier added successfully!!")

        conn.commit()
        conn.close()

    except Exception as e:
        log_error(e)
        print("Error occurred during Supplier adding!")

# 3 Record Inventory Purchase
def record_purchase(product_name, supplier_name, quantity):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # fetch product id
        cur.execute("SELECT product_id FROM products WHERE name ILIKE %s", (product_name,))
        product = cur.fetchone()
        # print(product)

        if not product:
            print("product does not exist!")
            conn.close()
            return

        # fetch supplier id
        cur.execute("SELECT supplier_id FROM suppliers WHERE name ILIKE %s", (supplier_name,))
        supplier = cur.fetchone()
        # print(supplier)
        
        if not supplier:
            print("supplier does not exist!")
            conn.close()
            return
        
        product_id = product[0]
        supplier_id = supplier[0]

        # add purchase
        cur.execute("INSERT INTO purchases (supplier_id, product_id, quantity) VALUES (%s, %s, %s)", (supplier_id, product_id, quantity))

        # update stock
        cur.execute("UPDATE products SET stock = stock - %s WHERE product_id = %s", (quantity, product_id))


        conn.commit()
        cur.close()
        conn.close()

        print("Purchase recorded and stock updated!")

    except Exception as e:
        log_error(e)
        print("Error recording purchase!")

# 4 Create Customer Order
def create_order(product_name, quantity):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # 
        cur.execute("UPDATE products SET stock = stock - %s WHERE name = %s AND stock >= %s RETURNING product_id, stock;", (quantity, product_name, quantity))

        result = cur.fetchone()
        print(result)

        product_id, remaining_stock = result
        if not result:
            print("Product does not exist!!")
            conn.rollback()
            conn.close()
            return
        elif remaining_stock < 0:
            print("Insufficient stock!")
            conn.rollback()
            conn.close()
            return
        elif remaining_stock < quantity:
            print("Insufficient stock!")
            conn.rollback()
            conn.close()
            return

        # insert order
        cur.execute("INSERT INTO orders (product_id, quantity) VALUES (%s, %s)",(product_id, quantity))

        conn.commit()
        cur.close()
        conn.close()

        print("Order placed successfully")

    except Exception as e:
        log_error(e)
        print("Error creating order!")

# 5 Daily Order Summary
def daily_order_summary():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT p.name, SUM(o.quantity) AS total_quantity, SUM(o.quantity * p.price) AS total_revenue FROM orders o JOIN products p ON o.product_id = p.product_id WHERE o.order_date = CURRENT_DATE GROUP BY p.name")

        rows = cur.fetchall()

        if not rows:
            print("No orders!")
        else:
            print("\nDaily Order Summary")
            for r in rows:
                print(f"Product: {r[0]}, Quantity: {r[1]}, Revenue: {r[2]}")

        cur.close()
        conn.close()

    except Exception as e:
        log_error(e)
        print("Error generating daily summary!!")

# 6 Supplier Purchase Summary
def supplier_purchase_summary():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT s.name, COUNT(p.purchase_id) AS total_transactions, SUM(p.quantity) AS total_units FROM purchases p JOIN suppliers s ON p.supplier_id = s.supplier_id GROUP BY s.name")

        rows = cur.fetchall()

        if not rows:
            print("No purchases found!!")   
        else:
            print("\nSupplier Purchase Summary")
            for r in rows:
                print(f"Supplier: {r[0]}, Transactions: {r[1]}, Units: {r[2]}")

        cur.close()
        conn.close()

    except Exception as e:
        log_error(e)
        print("Error generating supplier summary!!")

# 7 Cleanup old orders
def cleanup_old_orders():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM orders WHERE order_date < CURRENT_DATE - INTERVAL '30 days'")

        deleted_rows = cur.rowcount

        conn.commit()
        cur.close()
        conn.close()

        print(f"Deleted {deleted_rows} old orders!")

    except Exception as e:
        log_error(e)
        print("Error cleaning old orders!!")