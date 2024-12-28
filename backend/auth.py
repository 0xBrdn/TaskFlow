"""
Module de gestion des utilisateurs et de l'authentification Google pour une application TaskFlow.

Ce module fournit des fonctions pour :
- Se connecter à une base de données MySQL.
- Créer, connecter, déconnecter, et gérer des utilisateurs (y compris via Google OAuth2).
- Envoyer des e-mails de confirmation à travers l'API Gmail.

Imports:
    mysql.connector: Utilisé pour interagir avec la base de données MySQL.
    bcrypt: Utilisé pour chiffrer et vérifier les mots de passe.
    requests: Utilisé pour faire des requêtes HTTP (Google API).
    google.oauth2.id_token: Utilisé pour vérifier les tokens OAuth2 Google.
    google.auth.transport.requests: Utilisé pour transporter les requêtes Google.
    googleapiclient.discovery.build: Utilisé pour interagir avec l'API Gmail de Google.
    email.mime.text.MIMEText: Utilisé pour formater les e-mails envoyés via Gmail.

Variables:
    SCOPES (list): Liste des autorisations nécessaires pour interagir avec l'API Gmail.
    CLIENT_ID (str): ID client Google OAuth2.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import mysql.connector
from mysql.connector import Error
import bcrypt
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os.path
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def connect_to_db():
    """
    Se connecte à la base de données MySQL.

    Returns:
        connection: L'objet de connexion à la base de données
        si la connexion est réussie, sinon None.
    """
    try:
        connection = mysql.connector.connect(
            host="mysql-taskflowsae.alwaysdata.net",
            database="taskflowsae_db",
            user="379290_user",
            password="&Y37tMHYrC9J&G7SC7R4mRS?6KBBHD8c!HQ6!4n5",
        )
        if connection.is_connected():
            return connection
    except Error:
        return None


def close_db_connection(connection):
    """
    Ferme la connexion à la base de données MySQL.

    Args:
        connection: L'objet de connexion à fermer.
    """
    if connection.is_connected():
        connection.close()


def login_with_google(id_token_str):
    cursor = None
    connection = None

    try:
        CLIENT_ID = "428963010703-4ehn75nf048kk43mmjpqksvva1d01qk8.apps.googleusercontent.com"
        print(f"Vérification du token ID : {id_token_str}")  # Log du token ID reçu

        idinfo = id_token.verify_oauth2_token(id_token_str, google_requests.Request(), CLIENT_ID)
        print(f"IDinfo reçu : {idinfo}")

        email = idinfo.get("email")
        google_name = idinfo.get("name")
        print(f"Utilisateur trouvé : {google_name}, Email : {email}")

        connection = connect_to_db()
        if connection is None:
            print("Erreur de connexion à la base de données.")
            return False

        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            stored_email = result[3]
            if stored_email == email:
                print("L'utilisateur correspond bien.")
            print(f"Utilisateur existant : {result}")  # Log si l'utilisateur existe
            return True
        else:
            print(f"Utilisateur inexistant, création de : {google_name}, {email}")
            create_user_google(google_name, email)
            return True

    except ValueError as e:
        print(f"Erreur de vérification du token : {e}")
        return False
    except Error as e:
        print(f"Erreur base de données : {e}")
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

        query = """INSERT INTO users (username, password, email, is_google_user)
                   VALUES (%s, %s, %s, %s)"""
        cursor.execute(query, (username, "", email, 1))
        connection.commit()
        send_confirmation_email(email, username)
    except Error:
        pass
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

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        query = """INSERT INTO users (username, password, email)
                   VALUES (%s, %s, %s)"""
        cursor.execute(query, (username, hashed_password, email))
        connection.commit()
        send_confirmation_email(email, username)
    except Error:
        pass
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

        query = "SELECT password FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            stored_password = result[0]

            if bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8")):
                cursor.fetchall()
                return True
            else:
                cursor.fetchall()
                return False
        else:
            return False
    except Error:
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

        query = "SELECT password FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            stored_password = result[0]

            if bcrypt.checkpw(old_password.encode("utf-8"), stored_password.encode("utf-8")):
                cursor.fetchall()
                cursor.close()

                hashed_new_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())

                cursor = connection.cursor()

                update_query = "UPDATE users SET password = %s WHERE username = %s"
                cursor.execute(update_query, (hashed_new_password, username))
                connection.commit()
                return True
            else:
                return False
        else:
            return False
    except Error:
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


def send_confirmation_email(to_email, username):
    """
    Envoie un e-mail de confirmation à l'utilisateur après la création de son compte.

    Args:
        to_email (str): L'adresse e-mail de l'utilisateur.
        username (str): Le nom d'utilisateur de l'utilisateur.

    Returns:
        None
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            file_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../api/credentials.json")
            )
            flow = InstalledAppFlow.from_client_secrets_file(file_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    message = MIMEText(
        f"Bonjour {username},\n\nVotre compte a été créé avec succès."
        f"\nMerci de vous être inscrit sur TaskFlow !"
    )
    message["to"] = to_email
    message["subject"] = "Confirmation de création de compte"

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service = build("gmail", "v1", credentials=creds)
    try:
        message = {"raw": raw_message}
        service.users().messages().send(userId="me", body=message).execute()
    except Exception:
        pass