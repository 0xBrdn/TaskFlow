import mysql.connector
from mysql.connector import Error
import bcrypt

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',   
            database='TaskFlow',  
            user='root',      
            password='(x5GuPz#3V9]e6'  
        )
        if connection.is_connected():
            print("Connexion à la base de données MySQL réussie")
            return connection
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL : {e}")
        return None

def close_db_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Connexion à MySQL fermée.")

def create_user(username, password, email):
    try:
        connection = connect_to_db()
        if connection is None:
            return

        cursor = connection.cursor()

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        query = """INSERT INTO user (username, password, email) 
                   VALUES (%s, %s, %s)"""
        cursor.execute(query, (username, hashed_password, email))
        connection.commit()
        print("Utilisateur créé avec succès.")
    except Error as e:
        print(f"Erreur lors de la création de l'utilisateur : {e}")
    finally:
        if connection:
            close_db_connection(connection)

def login_user(username, password):
    try:
        connection = connect_to_db()
        if connection is None:
            return False

        cursor = connection.cursor()

        query = "SELECT password FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            stored_password = result[0]

            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                print("Connexion réussie.")
                return True
            else:
                print("Mot de passe incorrect.")
                return False
        else:
            print("Nom d'utilisateur non trouvé.")
            return False
    except Error as e:
        print(f"Erreur lors de la connexion de l'utilisateur : {e}")
        return False
    finally:
        if connection:
            close_db_connection(connection)

def logout_user():
    print("Déconnexion réussie.")
