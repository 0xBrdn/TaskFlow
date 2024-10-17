import os.path
import base64
import json
import requests
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Si vous modifiez ces portées, supprimez le fichier token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def send_confirmation_email(to_email, username):
    """
    Envoie un e-mail de confirmation à l'utilisateur après la création de son compte.

    Args:
        to_email (str): L'adresse e-mail de l'utilisateur.
        username (str): Le nom d'utilisateur de l'utilisateur.

    Returns:
        None
    """
    # Authentification à l'API Gmail
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Créer le message
    message = MIMEText(f"Bonjour {username},\n\nVotre compte a été créé avec succès.\nMerci de vous être inscrit !")
    message['to'] = to_email
    message['subject'] = "Confirmation de création de compte"

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Envoi de l'e-mail
    service = build('gmail', 'v1', credentials=creds)
    try:
        message = {'raw': raw_message}
        service.users().messages().send(userId='me', body=message).execute()
        print("E-mail de confirmation envoyé avec succès.")
    except Exception as e:
        print(f"Une erreur est survenue lors de l'envoi de l'e-mail : {e}")

