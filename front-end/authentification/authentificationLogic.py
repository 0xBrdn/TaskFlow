# auth_logic.py
import mysql.connector
import bcrypt
from mysql.connector import Error

def login_user(username, password):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='database_name',
            user='your_user',
            password='your_password'
        )

        cursor = conn.cursor()

        # Récupérer le mot de passe hashé
        cursor.execute("SELECT password FROM users WHERE email=%s", (username,))
        record = cursor.fetchone()

        if record:
            hashed_password = record[0].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                return True

        return False

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return False

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
