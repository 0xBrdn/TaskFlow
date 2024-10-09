import mysql.connector
from mysql.connector import Error
import bcrypt

# Fonction pour se connecter à la base de données
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',   # Remplace par l'hôte de ta base de données (ex: 'localhost')
            database='TaskFlow',  # Remplace par le nom de ta base de données
            user='root',      # Remplace par ton nom d'utilisateur MySQL
            password='(x5GuPz#3V9]e6'  # Remplace par ton mot de passe MySQL
        )
        if connection.is_connected():
            print("Connexion à la base de données MySQL réussie")
            return connection
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL : {e}")
        return None

# Fonction pour fermer la connexion à la base de données
def close_db_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Connexion à MySQL fermée.")

# Fonction pour créer un utilisateur avec hachage du mot de passe
def create_user(username, password, email):
    try:
        connection = connect_to_db()
        if connection is None:
            return

        cursor = connection.cursor()

        # Hachage du mot de passe avec bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insérer un nouvel utilisateur dans la table "user"
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

# Fonction pour se connecter (authentifier) un utilisateur
def login_user(username, password):
    try:
        connection = connect_to_db()
        if connection is None:
            return False

        cursor = connection.cursor()

        # Rechercher l'utilisateur par le nom d'utilisateur
        query = "SELECT password FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            stored_password = result[0]  # Le mot de passe haché dans la DB

            # Vérifier si le mot de passe correspond
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

# Fonction pour déconnecter un utilisateur (côté serveur, dans le contexte de session par exemple)
def logout_user():
    # Ici, tu pourrais gérer des tokens ou des sessions côté serveur.
    print("Déconnexion réussie.")
