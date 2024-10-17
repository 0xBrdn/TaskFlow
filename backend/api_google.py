from flask import Flask, request, jsonify
from auth import login_with_google  # Remplace par le nom de ton fichier auth.py

app = Flask(__name__)

@app.route('/api/login/google', methods=['POST'])
def google_login():
    data = request.get_json()
    id_token = data.get('id_token')

    if not id_token:
        return jsonify({"success": False, "message": "Token ID manquant."}), 400

    # Imprime le token pour vérifier
    print("Received ID Token:", id_token)

    success = login_with_google(id_token)
    
    if success:
        return jsonify({"success": True, "message": "Connexion réussie."}), 200
    else:
        return jsonify({"success": False, "message": "Échec de la connexion."}), 401


if __name__ == '__main__':
    app.run(port=5000)  
