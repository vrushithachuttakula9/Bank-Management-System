import mysql.connector

from bank.services.config import *
def db_connection():
    try:
        conn = mysql.connector.connect(
        host = HOST,
        user = USER,
        password = PASSWORD,
        database = DATABASE
        )
        return conn

    except mysql.connector.Error as e:
        print("Database connection error")
        print()

def insertData(tablename, **kwargs):

    conn = db_connection()
    cursor = conn.cursor()

    try:
        if tablename == "users":
            sql = ("INSERT INTO users (first_name, last_name, email, dob, salt, password)"
                   "VALUES (%(first_name)s, %(last_name)s, %(email)s,%(dob)s, %(salt)s,%(password)s)")

        elif tablename == "accounts":
            sql = ("INSERT INTO accounts (user_id, account_number, balance, is_active)"
                   "VALUES (%(user_id)s, %(account_number)s, %(balance)s, %(is_active)s)")

        elif tablename == "transactions":
            sql = ("INSERT INTO transactions (user_id, account_id, amount, from_account, to_account, trans_date, trans_type)"
                   "VALUES (%(user_id)s, %(account_id)s, %(amount)s, %(from_account)s, %(to_account)s, NOW(), %(trans_type)s)")

        else:
            print("Invalid tablename")

        cursor.execute(sql, kwargs)
        conn.commit()
        return
    except:
        print("Error in inserting data into database")
        conn.rollback()
        return
    finally:
        conn.commit()
        cursor.close()
        conn.close()

def fetchData(tablename, **kwargs):
    conn = db_connection()
    cursor = conn.cursor()
    try:
        base_sql = f"SELECT * from {tablename}"

        filters =  "AND".join([f"{key}=%({key})s" for key in kwargs])

        if filters:
            sql = f"{base_sql} WHERE {filters}"
        else:
            sql = base_sql
        cursor.execute(sql, kwargs)

        results = cursor.fetchall()
        return results
    except mysql.connector.Error as e:
        print("Error", e)
        return []
    finally:
        cursor.close()
        conn.close()

def fetchColumnData(tablename, column_name):
    conn = db_connection()
    cursor = conn.cursor()

    try:
        sql = f"SELECT {column_name} FROM {tablename}"
        cursor.execute(sql)
        results = cursor.fetchall()
        return [row[0] for row in results]
    except mysql.connector.Error as e:
        print("Error", e)
        return False
    finally:
        cursor.close()
        conn.close()

def updateData(tablename, values, conditions):
    conn = db_connection()
    cursor = conn.cursor()

    try:
        set_clause = ", ".join([f"{key} = %({key})s" for key in values])
        where_clause = " AND ".join([f"{key}=%({key})s" for key in conditions])

        sql = f"UPDATE {tablename} SET {set_clause} WHERE {where_clause}"
        cursor.execute(sql, {**values, **conditions})

    # Commit the changes to the database
        conn.commit()
    except mysql.connector.Error as e:
        print("Error", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

def update_last_login(user_email):
    try:
        conn = db_connection()
        cursor = conn.cursor()

        update_query = """
            UPDATE users
            SET lastlogin_date = NOW() 
            WHERE email = %s
        """
        cursor.execute(update_query, (user_email,))

        conn.commit()
        cursor.close()
        conn.close()
        return
    except mysql.connection.Error as e:
        print("Error updating last login time:",e)
        return
