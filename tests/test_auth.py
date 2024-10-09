import sys
import os

# Ajouter le chemin vers le répertoire où se trouve 'auth.py'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from auth import create_user, login_user


# Test pour créer un utilisateur
create_user("john_doe", "password123", "john@example.com")

# Test pour authentifier l'utilisateur
is_logged_in = login_user("john_doe", "password123")
if is_logged_in:
    print("L'utilisateur est connecté.")
else:
    print("Échec de la connexion.")
