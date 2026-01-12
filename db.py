import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="inventory_db",
        user="postgres",
        password="postgre123"
    )

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("Database connected successfully")
        conn.close()
    except Exception as e:
        print("Database connection failed")
        print(e)
