# auth_logic.py
import mysql.connector

DB_USER = "379290_user"
DB_PASSWORD = "&Y37tMHYrC9J&G7SC7R4mRS?6KBBHD8c!HQ6!4n5"
DB_DATABASE = "taskflowsae_db"
DB_HOST = "mysql-taskflowsae.alwaysdata.net"


def login_user(username, password):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST, database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD
        )
        assert conn.is_connected()
        cursor = conn.cursor()

        # Récupérer le mot de passe hashé
        cursor.execute("SELECT password FROM users WHERE email=%s;", (username,))
        record = cursor.fetchone()

        if record and record[0] == password:
            return True

        return False

    except Exception:
        return False

    # finally:
    #     if conn.is_connected():
    #         cursor.close()
    #         conn.close()


login_user("toto", "toto")
