import sys
import os
from flask import Flask, request, jsonify, current_app
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from backend.auth import login_with_google

app = Flask(__name__)

CLIENT_ID = "428963010703-4ehn75nf048kk43mmjpqksvva1d01qk8.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:5001/oauth2callback"

@app.route("/oauth2callback")
def oauth2callback():
    code = request.args.get("code")
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
        # Envoyer la requête pour obtenir les tokens
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            tokens = response.json()
            id_token_str = tokens.get("id_token")

            if not id_token_str:
                return jsonify({"success": False, "message": "Token ID manquant."}), 400

            # Vérifier et décoder le ID Token
            try:
                idinfo = id_token.verify_oauth2_token(
                    id_token_str, google_requests.Request(), CLIENT_ID
                )
            except ValueError as e:
                return jsonify({"success": False, "message": f"Erreur de validation du token : {e}"}), 400

            user_data = {
                "email": idinfo.get("email"),
                "name": idinfo.get("name"),
            }

            print(f"[Flask] Utilisateur connecté : {user_data}")

            success = login_with_google(id_token_str)
            if success:
                queue_lock = current_app.config.get("queue_lock")
                if queue_lock:
                    with queue_lock:
                        message = {
                            "type": "google_login_success",
                            "data": user_data,
                        }
                        print(f"[Flask] Ajout du message à la file : {message}")
                        current_app.config["message_queue"].put(message)
                else:
                    print("[Flask] Erreur : verrou introuvable dans la configuration Flask.")

                return jsonify({"success": True, "message": "Connexion réussie."})
            else:
                return jsonify({"success": False, "message": "Échec de la connexion à la base de données."}), 400
        else:
            return jsonify({"success": False, "message": "Erreur lors de l'obtention du token."}), 400
    except Exception as e:
        return jsonify({"success": False, "message": f"Erreur serveur : {e}"}), 500

@app.route("/api/login/google", methods=["POST"])
def google_login():
    data = request.get_json()
    id_token_str = data.get("id_token")

    if not id_token_str:
        return jsonify({"success": False, "message": "Token ID manquant."}), 400

    success = login_with_google(id_token_str)

    if success:
        return jsonify({"success": True, "message": "Connexion réussie."}), 200
    else:
        return jsonify({"success": False, "message": "Échec de la connexion."}), 401

if __name__ == "__main__":
    app.run(port=5001)