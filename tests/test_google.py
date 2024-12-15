import sys, os
import webbrowser
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from back_end.auth import *

CLIENT_ID = "428963010703-44ievtu901l6r9g8dhs2jjmf11mphidg.apps.googleusercontent.com"
REDIRECT_URI = "http://localhost:5000/oauth2callback"

AUTH_URL = (
    "https://accounts.google.com/o/oauth2/auth?response_type=code"
    "&client_id={}&redirect_uri={}&scope=email%20profile"
)


class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion")
        self.setGeometry(100, 100, 300, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Nom d'utilisateur :")
        layout.addWidget(self.label)

        self.username_input = QLineEdit(self)
        layout.addWidget(self.username_input)

        self.label_password = QLabel("Mot de passe :")
        layout.addWidget(self.label_password)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Se connecter")
        self.login_button.clicked.connect(self.login_user)
        layout.addWidget(self.login_button)

        self.google_login_button = QPushButton("Se connecter avec Google")
        self.google_login_button.clicked.connect(self.login_with_google)
        layout.addWidget(self.google_login_button)

        self.setLayout(layout)

    def login_user(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Appel de la fonction de connexion
        success = login_user(username, password)  # Appelle ta fonction de connexion ici

        if success:
            QMessageBox.information(self, "Succès", "Connexion réussie !")
        else:
            QMessageBox.warning(self, "Échec", "Nom d'utilisateur ou mot de passe incorrect.")

    def login_with_google(self):
        webbrowser.open(AUTH_URL.format(CLIENT_ID, REDIRECT_URI))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    sys.exit(app.exec())