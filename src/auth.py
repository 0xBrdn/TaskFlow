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

        # Rechercher le mot de passe pour l'utilisateur
        query = "SELECT password FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            stored_password = result[0]

            # Vérifier si le mot de passe est correct
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                print("Connexion réussie.")
                cursor.fetchall()  # S'assurer que tous les résultats sont consommés
                return True
            else:
                print("Mot de passe incorrect.")
                cursor.fetchall()  # S'assurer que tous les résultats sont consommés
                return False
        else:
            print("Nom d'utilisateur non trouvé.")
            return False
    except Error as e:
        print(f"Erreur lors de la connexion de l'utilisateur : {e}")
        return False
    finally:
        if cursor:
            cursor.close()  # Fermer le curseur ouvert
        if connection:
            close_db_connection(connection)

def change_password(username, old_password, new_password):
    try:
        connection = connect_to_db()
        if connection is None:
            return False

        cursor = connection.cursor()

        # Rechercher le mot de passe actuel de l'utilisateur
        query = "SELECT password FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            stored_password = result[0]

            # Vérifier l'ancien mot de passe
            if bcrypt.checkpw(old_password.encode('utf-8'), stored_password.encode('utf-8')):
                # Fermer le curseur précédent avant d'en ouvrir un autre
                cursor.fetchall()  # S'assurer que tous les résultats sont consommés
                cursor.close()

                # Hacher le nouveau mot de passe
                hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

                # Ouvrir un nouveau curseur pour la mise à jour du mot de passe
                cursor = connection.cursor()

                # Mettre à jour le mot de passe
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
            cursor.close()  # Fermer le curseur ouvert
        if connection:
            close_db_connection(connection)





def logout_user():
    print("Déconnexion réussie.")