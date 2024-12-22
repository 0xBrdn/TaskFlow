import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from backend.auth import login_with_google
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CLIENT_ID = "428963010703-44ievtu901l6r9g8dhs2jjmf11mphidg.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:5000/oauth2callback"


@app.route("/oauth2callback")
def oauth2callback():
    code = request.args.get("code")
    print(f"Code reçu : {code}")  # Vérifiez le code reçu ici

    if not code:
        return jsonify({"success": False, "message": "Code manquant."}), 400

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    try:
        response = requests.post(token_url, data=data)
        print(f"Réponse de Google : {response.status_code}, {response.text}")  # Log de la réponse de Google

        if response.status_code == 200:
            tokens = response.json()
            id_token = tokens.get("id_token")
            print(f"ID Token reçu : {id_token}")  # Vérifiez si le ID token est bien reçu

            if id_token:
                success = login_with_google(id_token)
                if success:
                    return jsonify({"success": True, "id_token": id_token, "message": "Connexion réussie."})
                else:
                    print("Échec de l'authentification dans login_with_google.")  # Log si la connexion échoue
                    return jsonify({"success": False, "message": "Échec de la connexion avec Google."}), 400
            else:
                print("ID token manquant dans la réponse.")  # Log si l'ID token est manquant
                return jsonify({"success": False, "message": "Erreur lors de la récupération du token ID."}), 400
        else:
            print(f"Erreur lors de l'obtention du token : {response.status_code}")  # Log de l'erreur de Google
            return jsonify({"success": False, "message": "Erreur lors de l'obtention du token."}), 400
    except Exception as e:
        print(f"Erreur lors de l'appel API : {e}")  # Log de l'exception
        return jsonify({"success": False, "message": "Erreur lors de la récupération du token."}), 500

@app.route("/api/login/google", methods=["POST"])
def google_login():
    """
    API de connexion via Google OAuth2.

    Cette API permet à un client d'envoyer un token ID pour authentifier un utilisateur via Google.

    Request Body:
        - id_token (str): Token ID Google à utiliser pour l'authentification.

    Returns:
        json: Un objet JSON indiquant le succès ou l'échec de la connexion.
        HTTP Code:
            - 200 en cas de succès.
            - 400 si le token ID est manquant.
            - 401 en cas d'échec de la connexion avec le token.
    """
    data = request.get_json()
    id_token = data.get("id_token")

    if not id_token:
        return jsonify({"success": False, "message": "Token ID manquant."}), 400

    success = login_with_google(id_token)

    if success:
        return jsonify({"success": True, "message": "Connexion réussie."}), 200
    else:
        return jsonify({"success": False, "message": "Échec de la connexion."}), 401


if __name__ == "__main__":
    app.run(port=5000)
