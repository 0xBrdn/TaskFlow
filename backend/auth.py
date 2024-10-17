import mysql.connector
from mysql.connector import Error
import bcrypt
import requests
import json
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

def connect_to_db():
    """
    Se connecte à la base de données MySQL.

    Returns:
        connection: L'objet de connexion à la base de données si la connexion est réussie, sinon None.
    """
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
    """
    Ferme la connexion à la base de données MySQL.

    Args:
        connection: L'objet de connexion à fermer.
    """
    if connection.is_connected():
        connection.close()
        print("Connexion à MySQL fermée.")

def login_with_google(id_token_str):
    """
    Authentifie un utilisateur avec un compte Google en validant le jeton.
    Args:
        id_token_str (str): Le jeton ID reçu de l'authentification Google.
    Returns:
        bool: True si l'authentification réussit, False sinon.
    """
    cursor = None
    connection = None

    try:
        # Remplace par ton vrai ID client Google
        CLIENT_ID = '428963010703-44ievtu901l6r9g8dhs2jjmf11mphidg.apps.googleusercontent.com'

        # Vérifier le jeton ID avec Google
        idinfo = id_token.verify_oauth2_token(id_token_str, google_requests.Request(), CLIENT_ID)

        # Récupérer l'adresse e-mail et le nom de l'utilisateur à partir du jeton
        email = idinfo.get('email')
        google_name = idinfo.get('name')

        # Vérifier si l'utilisateur existe déjà dans la base de données
        connection = connect_to_db()
        if connection is None:
            return False

        cursor = connection.cursor()

        query = "SELECT * FROM user WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            print("Utilisateur Google existant trouvé, connexion réussie.")
            return True
        else:
            # Si l'utilisateur n'existe pas, le créer comme un utilisateur Google
            create_user_google(google_name, email)
            print("Utilisateur Google créé avec succès.")
            return True

    except ValueError as e:
        print(f"Erreur lors de la vérification du jeton : {e}")
        return False
    except Error as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            close_db_connection(connection)

def create_user_google(username, email):
    """
    Crée un utilisateur Google dans la base de données.

    Args:
        username (str): Le nom d'utilisateur de Google.
        email (str): L'adresse e-mail de l'utilisateur Google.

    Returns:
        None
    """
    try:
        connection = connect_to_db()
        if connection is None:
            return

        cursor = connection.cursor()

        # Créer un utilisateur avec is_google_user=1
        query = """INSERT INTO user (username, password, email, is_google_user) 
                   VALUES (%s, %s, %s, %s)"""
        # Pas besoin de mot de passe car l'authentification se fait via Google
        cursor.execute(query, (username, None, email, 1))
        connection.commit()
        print("Utilisateur Google créé avec succès.")
    except Error as e:
        print(f"Erreur lors de la création de l'utilisateur Google : {e}")
    finally:
        if connection:
            close_db_connection(connection)



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