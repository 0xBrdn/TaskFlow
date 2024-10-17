import mysql.connector
from mysql.connector import Error
import bcrypt
import requests
import json

def connect_to_db():
    """
    Se connecte à la base de données MySQL.

    Returns:
        connection: L'objet de connexion à la base de données si la connexion est réussie, sinon None.
    """
    try:
        connection = mysql.connector.connect(
            host='mysql-taskflowsae.alwaysdata.net',
            database='taskflowsae_db',
            user='379290_user',
            password='&Y37tMHYrC9J&G7SC7R4mRS?6KBBHD8c!HQ6!4n5'
        )
        if connection.is_connected():
            print("Connexion à la base de données MySQL réussie")
            return connection
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL : {e}")
        return None

def close_db_connection(connection):
    """
    Ferme la connexion à la base de données MySQL.

    Args:
        connection: L'objet de connexion à fermer.
    """
    if connection.is_connected():
        connection.close()
        print("Connexion à MySQL fermée.")
def create_user(username, password, email):
    """
    Crée un nouvel utilisateur dans la base de données.

    Args:
        username (str): Le nom d'utilisateur de l'utilisateur à créer.
        password (str): Le mot de passe de l'utilisateur à créer.
        email (str): L'adresse e-mail de l'utilisateur à créer.

    Raises:
        Error: En cas d'erreur lors de l'insertion dans la base de données.
    """
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
    """
    Authentifie un utilisateur en vérifiant ses identifiants.

    Args:
        username (str): Le nom d'utilisateur de l'utilisateur à authentifier.
        password (str): Le mot de passe de l'utilisateur à authentifier.

    Returns:
        bool: True si la connexion réussit, False sinon.

    Raises:
        Error: En cas d'erreur lors de la vérification des identifiants.
    """
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
                cursor.fetchall() 
                return True
            else:
                print("Mot de passe incorrect.")
                cursor.fetchall()
                return False
        else:
            print("Nom d'utilisateur non trouvé.")
            return False
    except Error as e:
        print(f"Erreur lors de la connexion de l'utilisateur : {e}")
        return False
    finally:
        if cursor:
            cursor.close() 
        if connection:
            close_db_connection(connection)

def change_password(username, old_password, new_password):
    """
    Change le mot de passe d'un utilisateur.

    Args:
        username (str): Le nom d'utilisateur dont le mot de passe doit être changé.
        old_password (str): L'ancien mot de passe de l'utilisateur.
        new_password (str): Le nouveau mot de passe à définir.

    Returns:
        bool: True si le mot de passe est changé avec succès, False sinon.

    Raises:
        Error: En cas d'erreur lors du changement de mot de passe.
    """
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

            if bcrypt.checkpw(old_password.encode('utf-8'), stored_password.encode('utf-8')):
                cursor.fetchall()
                cursor.close()

                hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

                cursor = connection.cursor()

                update_query = "UPDATE user SET password = %s WHERE username = %s"
                cursor.execute(update_query, (hashed_new_password, username))
                connection.commit()
                print("Mot de passe changé avec succès.")
                return True
            else:
                print("L'ancien mot de passe est incorrect.")
                return False
        else:
            print("Nom d'utilisateur non trouvé.")
            return False
    except Error as e:
        print(f"Erreur lors du changement de mot de passe : {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            close_db_connection(connection)

def logout_user():
    """
    Déconnecte l'utilisateur.

    Note:
        Cette fonction peut être utilisée pour gérer les sessions côté serveur.
    """
    print("Déconnexion réussie.")