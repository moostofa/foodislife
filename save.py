import mysql.connector
from mysql.connector import Error

""" Connect to MySQL database & save restaurants """
def save(restaurants: list):
    print("Saving restaurants to database...")
    conn = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='foodme',
            user='root',
            password='mypassword'   # placeholder
        )
        if conn.is_connected():
            print('Connected to MySQL database')

    except Error as e:
        print(e)

    else:
        db = conn.cursor()

        insert = """
        INSERT INTO restaurants (
            name, 
            restaurant_description, 
            restaurant_location, 
            cuisine, 
            phone
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        # save each restaurant to DB
        for r in restaurants:
            values = tuple(r.values())
            db.execute(insert, values)
            db.commit()

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
        print("Saved restaurants to database.")
