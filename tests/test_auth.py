import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from auth import create_user, login_user, change_password, login_with_google

create_user("john_doe", "password123", "john@example.com")

if change_password("john_doe", "password123", "newpassword789"):
    print("Mot de passe changé avec succès.")
else:
    print("Échec du changement de mot de passe.")

if login_user("john_doe", "newpassword789"):
    print("L'utilisateur est connecté avec le nouveau mot de passe.")
else:
    print("Échec de la connexion avec le nouveau mot de passe.")

# Exemple de jeton reçu de Google (à remplacer par le jeton réel)
google_token = "TOKEN_ID_FROM_GOOGLE"

if login_with_google(google_token):
    print("Utilisateur authentifié avec succès via Google.")
else:
    print("Échec de l'authentification Google.")

