import sys
import webbrowser
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox

CLIENT_ID = "428963010703-44ievtu901l6r9g8dhs2jjmf11mphidg.apps.googleusercontent.com"
REDIRECT_URI = "http://localhost:5000/oauth2callback"  # URI de redirection

# URL pour obtenir le code d'autorisation
AUTH_URL = (
    "https://accounts.google.com/o/oauth2/auth?response_type=code"
    "&client_id={}&redirect_uri={}&scope=email%20profile"
)

class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion Google")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Cliquez pour vous connecter avec Google")
        layout.addWidget(self.label)

        self.google_login_button = QPushButton("Se connecter avec Google")
        self.google_login_button.clicked.connect(self.login_with_google)
        layout.addWidget(self.google_login_button)

        self.setLayout(layout)

    def login_with_google(self):
        # Ouvrir le navigateur pour l'authentification
        webbrowser.open(AUTH_URL.format(CLIENT_ID, REDIRECT_URI))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    sys.exit(app.exec())
