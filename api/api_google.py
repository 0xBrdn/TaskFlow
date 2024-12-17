"""
Module d'authentification Google OAuth2 pour une application Flask.

Ce module permet de gérer l'authentification via Google OAuth2 à travers deux routes principales :
- `/oauth2callback` : Route de redirection après la connexion Google OAuth2.
- `/api/login/google` : API permettant la connexion via Google en envoyant un token ID.

Imports:
    sys (module): Utilisé pour manipuler le chemin d'accès aux modules Python.
    os (module): Utilisé pour gérer les chemins d'accès aux fichiers et dossiers.
    auth.login_with_google (fonction): Fonction externe pour gérer l'authentification avec Google.
    flask.Flask (classe): Classe de l'application Flask.
    flask.request (objet): Objet pour récupérer les requêtes HTTP entrantes.
    flask.jsonify (fonction): Fonction pour retourner une réponse JSON.
    flask.redirect (fonction): Fonction pour rediriger les utilisateurs vers une autre URL.
    flask.url_for (fonction): Génère les URLs pour les routes définies.
    requests (module): Utilisé pour faire des requêtes HTTP externes (ici vers l'API Google).

Variables:
    CLIENT_ID (str): ID client Google OAuth2.
    CLIENT_SECRET (str): Clé secrète client Google OAuth2.
    REDIRECT_URI (str): URI de redirection après authentification via Google OAuth2.

Routes:
    /oauth2callback (fonction):
        Gère le retour après authentification Google OAuth2 et traite le code d'autorisation.
        
        Returns:
            str: Message de succès ou d'échec de l'authentification.
            tuple: En cas d'erreur, retourne un message et un code HTTP 400.

    /api/login/google (fonction):
        API pour la connexion via Google en utilisant un token ID.
        
        Returns:
            json: Réponse JSON avec un message de succès ou d'échec et un code HTTP.
"""

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from back_end.auth import login_with_google
from flask import Flask, request, jsonify, redirect, url_for
import requests

app = Flask(__name__)

CLIENT_ID = "428963010703-44ievtu901l6r9g8dhs2jjmf11mphidg.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:5000/oauth2callback"

@app.route('/oauth2callback')
def oauth2callback():
    """
    Route de redirection après l'authentification Google OAuth2.

    Cette route est appelée lorsque Google redirige l'utilisateur après une tentative de connexion.
    Elle traite le code d'autorisation reçu et échange celui-ci contre un token d'accès auprès de l'API Google.

    Returns:
        str: Message de confirmation de la connexion réussie ou d'erreur en cas d'échec.
        tuple: En cas de problème lors de l'obtention du token, retourne un message d'erreur et un code HTTP 400.
    """
    code = request.args.get('code')

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

        if id_token:
            success = login_with_google(id_token)
            if success:
                return "L'utilisateur exite déjà ! Vous pouvez fermer cette page et vous connecter en rentrtant uniquement l'adresse mail de votre compte Google."
            else:
                return "Échec de la connexion avec Google."
        else:
            return "Erreur lors de la récupération du token ID."
    else:
        return "Erreur lors de l'obtention du token.", 400

@app.route('/api/login/google', methods=['POST'])
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