import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from auth import create_user, login_user, change_password

# Test de la création d'un utilisateur
create_user("john_doe", "password123", "john@example.com")

# Test pour le changement de mot de passe
if change_password("john_doe", "password123", "newpassword789"):
    print("Mot de passe changé avec succès.")
else:
    print("Échec du changement de mot de passe.")

# Test de la connexion post-changement
if login_user("john_doe", "newpassword789"):
    print("L'utilisateur est connecté avec le nouveau mot de passe.")
else:
    print("Échec de la connexion avec le nouveau mot de passe.")

create_user("test", "test", "taskflowreminder1@gmail.com")

