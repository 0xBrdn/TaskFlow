import os
from PyQt5 import QtCore, QtGui, QtWidgets
from back_end.db_api import DB_API
from pagePrincipale import Ui_MainWindow as MainWindowUI
import webbrowser

CLIENT_ID = "428963010703-44ievtu901l6r9g8dhs2jjmf11mphidg.apps.googleusercontent.com"
REDIRECT_URI = "http://localhost:5000/oauth2callback"

AUTH_URL = (
    "https://accounts.google.com/o/oauth2/auth?response_type=code"
    "&client_id={}&redirect_uri={}&scope=email%20profile"
)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        """
            Initialise et configure l'interface utilisateur pour la fenêtre de connexion/inscription.

            Cette méthode met en place tous les éléments graphiques de la fenêtre d'authentification,
            incluant les champs de saisie email et mot de passe, les boutons, et la gestion des états
            de formulaire (connexion/inscription).

            Principales fonctionnalités:
            - Configuration des widgets PyQt5
            - Création des frames, labels, champs de saisie et boutons
            - Mise en place des connexions pour la gestion des événements
            - Chargement de la feuille de style
            - Initialisation de l'état du formulaire

            :param MainWindow: La fenêtre principale de l'application à configurer
            :type MainWindow: QtWidgets.QMainWindow

            Exemple d'utilisation:
            main_window = QtWidgets.QMainWindow()
            ui = Ui_MainWindow()
            ui.setupUi(main_window)
            main_window.show()
            """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1035, 774)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/authentification/logo_alternatif.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        # Charger le fichier QSS
        with open("authentification.qss", "r") as file:
            stylesheet = file.read()
            MainWindow.setStyleSheet(stylesheet)

        # Instanciation de la page dans sa globalité
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # Frame de la mire d'authentification
        self.frameMire = QtWidgets.QFrame(self.centralwidget)
        self.frameMire.setMinimumSize(QtCore.QSize(350, 500))
        self.frameMire.setMaximumSize(QtCore.QSize(350, 500))
        self.frameMire.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameMire.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameMire.setObjectName("frameMire")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frameMire)
        self.verticalLayout.setObjectName("verticalLayout")

        # Frame du titre
        self.frameTitre = QtWidgets.QFrame(self.frameMire)
        self.frameTitre.setMinimumSize(QtCore.QSize(100, 60))
        self.frameTitre.setMaximumSize(QtCore.QSize(300, 60))
        self.frameTitre.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameTitre.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameTitre.setObjectName("frameTitre")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frameTitre)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        # Label du titre
        self.label = QtWidgets.QLabel(self.frameTitre)
        self.label.setMinimumSize(QtCore.QSize(100, 60))
        self.label.setMaximumSize(QtCore.QSize(1500, 60))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("titre")
        self.verticalLayout_5.addWidget(self.label)
        self.verticalLayout.addWidget(self.frameTitre, 0, QtCore.Qt.AlignHCenter)

        # Frame pour le champs Email
        self.frameLogin = QtWidgets.QFrame(self.frameMire)
        self.frameLogin.setMinimumSize(QtCore.QSize(350, 100))
        self.frameLogin.setMaximumSize(QtCore.QSize(350, 100))
        self.frameLogin.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameLogin.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameLogin.setObjectName("frameLogin")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frameLogin)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # Titre et champ de l'Email
        self.titreMail = QtWidgets.QLabel(self.frameLogin)
        self.titreMail.setMinimumSize(QtCore.QSize(60, 30))
        self.titreMail.setMaximumSize(QtCore.QSize(60, 30))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.titreMail.setFont(font)
        self.verticalLayout_2.addWidget(self.titreMail)

        self.inputMail = QtWidgets.QLineEdit(self.frameLogin)
        self.inputMail.setMinimumSize(QtCore.QSize(300, 30))
        self.inputMail.setMaximumSize(QtCore.QSize(300, 30))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        self.inputMail.setFont(font)
        self.inputMail.setObjectName("inputMail")
        self.verticalLayout_2.addWidget(self.inputMail)

        self.verticalLayout.addWidget(self.frameLogin, 0, QtCore.Qt.AlignHCenter)

        # Frame pour le champ mot de passe
        self.framePassword = QtWidgets.QFrame(self.frameMire)
        self.framePassword.setMinimumSize(QtCore.QSize(350, 100))
        self.framePassword.setMaximumSize(QtCore.QSize(350, 100))
        self.framePassword.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.framePassword.setFrameShadow(QtWidgets.QFrame.Raised)
        self.framePassword.setObjectName("framePassword")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.framePassword)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        # # Titre et champ du mot de passe
        self.titrePassword = QtWidgets.QLabel(self.framePassword)
        self.titrePassword.setMaximumSize(QtCore.QSize(120, 30))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.titrePassword.setFont(font)
        self.verticalLayout_3.addWidget(self.titrePassword)

        self.inputPassword = QtWidgets.QLineEdit(self.framePassword)
        self.inputPassword.setMinimumSize(QtCore.QSize(300, 30))
        self.inputPassword.setMaximumSize(QtCore.QSize(300, 30))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        self.inputPassword.setFont(font)
        self.inputPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.inputPassword.setObjectName("inputPassword")
        self.verticalLayout_3.addWidget(self.inputPassword)

        self.verticalLayout.addWidget(self.framePassword, 0, QtCore.Qt.AlignHCenter)

        self.google_login_button = QtWidgets.QPushButton(self.frameMire)
        self.google_login_button.setMinimumSize(QtCore.QSize(60, 60))
        self.google_login_button.setMaximumSize(QtCore.QSize(60, 60))

        google_icon = QtGui.QIcon("images/authentification/logo_google.png")
        self.google_login_button.setIcon(google_icon)
        self.google_login_button.setIconSize(QtCore.QSize(50, 50))

        self.google_login_button.clicked.connect(self.login_with_google)

        self.verticalLayout.addWidget(self.google_login_button, 0, QtCore.Qt.AlignHCenter)

        # Frame pour les message d'erreur
        self.frameErreur = QtWidgets.QFrame(self.frameMire)
        self.frameErreur.setMinimumSize(QtCore.QSize(350, 50))
        self.frameErreur.setMaximumSize(QtCore.QSize(350, 50))
        self.frameErreur.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameErreur.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameErreur.setObjectName("frameErreur")

        self.verticalLayoutErreur = QtWidgets.QVBoxLayout(self.frameErreur)
        self.verticalLayoutErreur.setObjectName("verticalLayoutErreur")

        # Label pour les erreurs
        self.labelErreur = QtWidgets.QLabel(self.frameErreur)
        self.labelErreur.setObjectName("labelErreur")
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        self.labelErreur.setFont(font)
        self.labelErreur.setStyleSheet("color: red;")
        self.labelErreur.setAlignment(QtCore.Qt.AlignCenter)
        self.labelErreur.setWordWrap(True)
        self.verticalLayoutErreur.addWidget(self.labelErreur)

        # Organise le frame des erreurs pour qu'ils se place entre le champ mot de passe et le bouton Valider.
        self.verticalLayout.insertWidget(3, self.frameErreur, 0, QtCore.Qt.AlignHCenter)

        # Frame pour le bouton Valider.
        self.frameBouton = QtWidgets.QFrame(self.frameMire)
        self.frameBouton.setMinimumSize(QtCore.QSize(150, 100))
        self.frameBouton.setMaximumSize(QtCore.QSize(150, 100))
        self.frameBouton.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameBouton.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameBouton.setObjectName("frameBouton")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frameBouton)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        # Bouton Valider
        self.boutonValider = QtWidgets.QPushButton(self.frameBouton)
        self.boutonValider.setMaximumSize(QtCore.QSize(150, 50))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.boutonValider.setFont(font)
        self.boutonValider.setObjectName("boutonValider")
        self.verticalLayout_4.addWidget(self.boutonValider)
        self.boutonValider.clicked.connect(self.handle_login)

        self.verticalLayout.addWidget(self.frameBouton, 0, QtCore.Qt.AlignHCenter)

        # "Créer un compte" label (lien)
        self.frameCreerCompte = QtWidgets.QFrame(self.frameMire)
        self.frameCreerCompte.setMinimumSize(QtCore.QSize(100, 50))
        self.frameCreerCompte.setMaximumSize(QtCore.QSize(100, 50))
        self.frameCreerCompte.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameCreerCompte.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameCreerCompte.setObjectName("frameCreerCompte")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frameCreerCompte)
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        self.boutonCreerCompte = QtWidgets.QLabel("<a href='#'>Créer un compte</a>", self.frameCreerCompte)
        self.boutonCreerCompte.setMinimumSize(QtCore.QSize(25, 25))
        self.boutonCreerCompte.setMaximumSize(QtCore.QSize(80, 25))
        self.boutonCreerCompte.setObjectName("boutonCreerCompte")
        self.boutonCreerCompte.setAlignment(QtCore.Qt.AlignCenter)
        self.boutonCreerCompte.linkActivated.connect(self.show_signup_form)  # Connecte le lien à la fonction qui permett le changement de forme
        self.verticalLayout_6.addWidget(self.boutonCreerCompte)
        self.verticalLayout.addWidget(self.frameCreerCompte, 0, QtCore.Qt.AlignHCenter)

        self.gridLayout.addWidget(self.frameMire, 2, 0, 1, 1)

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(300, 140))
        self.frame.setMaximumSize(QtCore.QSize(300, 160))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout.addWidget(self.frame_2, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        # Variable qui vérifie la forme actuelle
        self.is_login_form = True

        # Stocke la reference MainWindow
        self.main_window = MainWindow

        # Initialise l'était du formulaire et les connections.
        self.update_form_state()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def show_signup_form(self):
        """
        Permute entre les formulaires de connexion et d'inscription.
        Cette méthode met à jour l'état de l'interface utilisateur en basculant
        entre les deux formulaires disponibles: connexion et inscription.

        Fonctionnalités principales:
        - Basculer entre l'état de connexion et d'inscription.
        - Mettre à jour l'affichage des champs, titres, et boutons associés.

        Exemple d'utilisation:
        self.show_signup_form()
        """
        self.is_login_form = not self.is_login_form
        self.update_form_state()

    def update_form_state(self):
        """
        Met à jour l'état et l'apparence des formulaires selon le contexte.

        Cette méthode est appelée pour ajuster dynamiquement les éléments de l'interface,
        en fonction de l'état actuel du formulaire (connexion ou inscription). Elle adapte
        notamment les labels, les placeholders, les textes des boutons, et les connexions
        des événements.

        Fonctionnalités principales:
        - Mise à jour des textes affichés (titres, boutons, placeholders).
        - Déconnexion des anciens événements et création de nouveaux.
        - Gestion des connexions pour valider l'action courante (connexion/inscription).

        Exemple d'utilisation:
            self.is_login_form = False
            self.update_form_state()
        """

        _translate = QtCore.QCoreApplication.translate

        # Déconnecte les connections existantes
        try:
            self.boutonValider.clicked.disconnect()
            self.inputMail.returnPressed.disconnect()
            self.inputPassword.returnPressed.disconnect()
        except:
            pass

        if self.is_login_form:
            # Formulaire d'authentification
            self.main_window.setWindowTitle(_translate("MainWindow", "TaskFlow - Login"))
            self.label.setText(_translate("MainWindow", "S'identifier"))
            self.boutonValider.setText(_translate("MainWindow", "Valider"))
            self.boutonCreerCompte.setText("<a href='#'>Créer un compte</a>")
            self.inputPassword.setPlaceholderText("")
            self.inputMail.setPlaceholderText("")

            # Met en place les connection du formulaire d'authentification.
            self.boutonValider.clicked.connect(self.handle_login)
            self.inputMail.returnPressed.connect(self.handle_login)
            self.inputPassword.returnPressed.connect(self.handle_login)
        else:
            # Formulaire de création de compte
            self.main_window.setWindowTitle(_translate("MainWindow", "TaskFlow - Inscription"))
            self.label.setText(_translate("MainWindow", "Créer un compte"))
            self.boutonValider.setText(_translate("MainWindow", "S'inscrire"))
            self.boutonCreerCompte.setText("<a href='#'>Retour</a>")
            self.inputPassword.setPlaceholderText("Minimum 8 caractères")
            self.inputMail.setPlaceholderText("exemple@email.com")

            # Met en place les connection du formulaire d'authentification.
            self.boutonValider.clicked.connect(self.handle_signup)
            self.inputMail.returnPressed.connect(self.handle_signup)
            self.inputPassword.returnPressed.connect(self.handle_signup)

    def handle_login(self):
        """
        Gère la soumission du formulaire de connexion.

        Cette méthode valide les champs de saisie, récupère les informations d'authentification
        depuis la base de données, et affiche un message de succès ou d'erreur en conséquence.
        En cas de succès, elle redirige vers la fenêtre principale.

        Fonctionnalités principales:
        - Validation des champs email et mot de passe.
        - Comparaison des données avec celles stockées en base de données.
        - Affichage des messages d'erreur ou de succès.
        - Navigation vers la fenêtre principale en cas de connexion réussie.

        Exemple d'utilisation:
        self.handle_login()
        """

        # Nettoie les potentiels messages d'erreur existants
        self.clear_error_message()

        email = self.inputMail.text()
        password = self.inputPassword.text()
        print("Authentification...")

        hashpass = DB_API.get_email_hashpass(email)
        if isinstance(hashpass, Exception) or not hashpass:
            self.show_error_message("Échec de connexion", "Email ou mot de passe incorrect")
            print("echec")
            return False

        elif hashpass[0] == password:
            self.show_success_message("Connexion réussie", "Bienvenue!")
            print("succes")

            self.open_main_window()
            return True

        else:
            self.show_error_message("Échec de connexion", "Email ou mot de passe incorrect")
            print("echec")
            return False

    def login_with_google(self):
        webbrowser.open(AUTH_URL.format(CLIENT_ID, REDIRECT_URI))

    def handle_signup(self):
        """
        Gère la soumission du formulaire d'inscription.

        Cette méthode valide les champs de saisie (email et mot de passe), vérifie la disponibilité
        de l'email, et crée un nouvel utilisateur si toutes les conditions sont remplies.
        Elle retourne ensuite à l'écran de connexion.

        Fonctionnalités principales:
        - Validation du format de l'email.
        - Vérification que l'email n'existe pas déjà en base de données.
        - Création d'un nouvel utilisateur dans la base de données.
        - Affichage des messages d'erreur ou de succès.

        Exemple d'utilisation:
            self.handle_signup()
        """
        self.clear_error_message()

        email = self.inputMail.text()
        password = self.inputPassword.text()

        # Vérification des éléments remplis
        if not self.validate_email(email):
            self.show_error_message("Erreur d'inscription", "Veuillez entrer une adresse email valide")
            return False

        if len(password) < 8:
            self.show_error_message("Erreur d'inscription", "Le mot de passe doit contenir au moins 8 caractères")
            return False

        # Vérifie si l'adresse mail est existante
        existing_user = DB_API.get_email_hashpass(email)
        if existing_user and not isinstance(existing_user, Exception):
            self.show_error_message("Erreur d'inscription", "Cette adresse email est déjà utilisée")
            return False

        # Créé le nouvel utilisateur
        try:
            success = DB_API.add_user(email, password)
            if success:
                self.show_success_message("Inscription réussie", "Votre compte a été créé avec succès!")
                # Switch back to login form
                self.is_login_form = True
                self.update_form_state()
                return True
            else:
                self.show_error_message("Erreur d'inscription", "Erreur lors de la création du compte")
                return False
        except Exception as e:
            self.show_error_message("Erreur d'inscription", f"Une erreur est survenue: {str(e)}")
            return False

    def validate_email(self, email):
        """
        Valide le format de l'email saisi par l'utilisateur.

        Cette méthode utilise une expression régulière pour vérifier si l'email
        respecte le format standard.

        :param email: Adresse email à valider
        :type email: str
        :return: `True` si le format est valide, sinon `False`
        :rtype: bool

        Exemple d'utilisation:
        if not self.validate_email(email):
            print("Email invalide")
        """

        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def show_error_message(self, title, message):
        """
        Affiche un message d'erreur dans le label prévu à cet effet.

        Cette méthode met à jour le contenu du label `labelErreur` avec un message d'erreur.
        Le message est automatiquement effacé après un délai de 3 secondes.

        :param title: Titre du message d'erreur (non affiché ici, prévu pour une extension future)
        :type title: str
        :param message: Contenu du message d'erreur
        :type message: str

        Exemple d'utilisation:
        self.show_error_message("Erreur", "Email ou mot de passe incorrect")
        """

        self.labelErreur.setText(message)
        # Délais de supression de message. Ici 3 secondes.
        QtCore.QTimer.singleShot(3000, self.clear_error_message)

    def clear_error_message(self):
        """
        Efface le message d'erreur affiché dans `labelErreur`.

        Cette méthode remet le contenu du label à une chaîne vide.

        Exemple d'utilisation:
        self.clear_error_message()
        """

        self.labelErreur.clear()

    def show_success_message(self, title, message):
        """
        Affiche un message de succès dans le label prévu à cet effet.

        Cette méthode modifie temporairement le style du label `labelErreur` pour afficher
        un message de succès en blanc, puis le réinitialise après un délai de 3 secondes.

        :param title: Titre du message de succès (non affiché ici, prévu pour une extension future)
        :type title: str
        :param message: Contenu du message de succès
        :type message: str

        Exemple d'utilisation:
        self.show_success_message("Succès", "Votre compte a été créé avec succès")
        """

        self.labelErreur.setStyleSheet("color: white;")
        self.labelErreur.setText(message)
        # Nettoie les messages de succès au bout de 3 secondes
        QtCore.QTimer.singleShot(3000, self.clear_error_message)
        # Réinitialise la couleur du label.
        QtCore.QTimer.singleShot(3000, lambda: self.labelErreur.setStyleSheet("color: red;"))

    def open_main_window(self):
        """
        Redirige vers la fenêtre principale après une connexion réussie.

        Cette méthode ferme la fenêtre d'authentification et instancie la fenêtre principale
        de l'application.

        Fonctionnalités principales:
        - Fermeture de la fenêtre actuelle.
        - Création et affichage de la fenêtre principale.

        Exemple d'utilisation:
        self.open_main_window()
        """

        # Fermer la fenêtre de connexion actuelle
        self.main_window.close()

        # Créer et afficher la fenêtre principale
        self.main_window_instance = QtWidgets.QMainWindow()
        self.main_window_ui = MainWindowUI()
        self.main_window_ui.setupUi(self.main_window_instance)

        # Passer l'email de l'utilisateur connecté
        self.main_window_ui.set_current_user(self.inputMail.text())

        # Stocker une référence à la fenêtre principale
        self.main_window_ui.main_window = self.main_window_instance
        self.main_window_instance.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("TaskFlow - Login", "TaskFlow - Login"))
        self.label.setText(_translate("MainWindow", "S'identifier"))
        self.titreMail.setText(_translate("MainWindow", "E-Mail"))
        self.titrePassword.setText(_translate("MainWindow", "Mot de passe"))
        self.boutonValider.setText(_translate("MainWindow", "Valider"))