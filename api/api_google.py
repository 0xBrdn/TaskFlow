import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from auth import login_with_google  # Remplace par le nom de ton fichier auth.py
from flask import Flask, request, jsonify, redirect, url_for
import requests

app = Flask(__name__)

CLIENT_ID = "428963010703-44ievtu901l6r9g8dhs2jjmf11mphidg.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:5000/oauth2callback"

@app.route('/oauth2callback')
def oauth2callback():
    code = request.args.get('code')  # Récupérer le code d'autorisation

    # Échanger le code d'autorisation contre un token d'accès
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }

    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        tokens = response.json()
        id_token = tokens.get('id_token')
        
        # Authentifier l'utilisateur avec Google
        if id_token:
            success = login_with_google(id_token)
            if success:
                return "Connexion réussie ! Vous pouvez fermer cette page."
            else:
                return "Échec de la connexion avec Google."
        else:
            return "Erreur lors de la récupération du token ID."
    else:
        return "Erreur lors de l'obtention du token.", 400

@app.route('/api/login/google', methods=['POST'])
def google_login():
    data = request.get_json()
    id_token = data.get('id_token')

    if not id_token:
        return jsonify({"success": False, "message": "Token ID manquant."}), 400

    success = login_with_google(id_token)
    
    if success:
        return jsonify({"success": True, "message": "Connexion réussie."}), 200
    else:
        return jsonify({"success": False, "message": "Échec de la connexion."}), 401

if __name__ == '__main__':
    app.run(port=5000)
