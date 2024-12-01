from PyQt5 import QtCore, QtGui, QtWidgets
from backend.db_api import DB_API
from front_end2 import Ui_MainWindow as MainWindowUI


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1035, 774)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./images/logo_alternatif.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        # Charger le fichier QSS
        self.load_stylesheet(MainWindow)

        # Setup existing design
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # Existing frames and widgets
        self.frameMire = QtWidgets.QFrame(self.centralwidget)
        self.frameMire.setMinimumSize(QtCore.QSize(350, 500))
        self.frameMire.setMaximumSize(QtCore.QSize(350, 500))
        self.frameMire.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameMire.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameMire.setObjectName("frameMire")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frameMire)
        self.verticalLayout.setObjectName("verticalLayout")

        # Frame title
        self.frameTitre = QtWidgets.QFrame(self.frameMire)
        self.frameTitre.setMinimumSize(QtCore.QSize(100, 60))
        self.frameTitre.setMaximumSize(QtCore.QSize(300, 60))
        self.frameTitre.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameTitre.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameTitre.setObjectName("frameTitre")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frameTitre)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        # Title label
        self.label = QtWidgets.QLabel(self.frameTitre)
        self.label.setMinimumSize(QtCore.QSize(100, 60))
        self.label.setMaximumSize(QtCore.QSize(1500, 60))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.verticalLayout.addWidget(self.frameTitre, 0, QtCore.Qt.AlignHCenter)

        # Frame for email input
        self.frameLogin = QtWidgets.QFrame(self.frameMire)
        self.frameLogin.setMinimumSize(QtCore.QSize(350, 100))
        self.frameLogin.setMaximumSize(QtCore.QSize(350, 100))
        self.frameLogin.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameLogin.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameLogin.setObjectName("frameLogin")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frameLogin)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # Email title and input
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

        # Frame for password input
        self.framePassword = QtWidgets.QFrame(self.frameMire)
        self.framePassword.setMinimumSize(QtCore.QSize(350, 100))
        self.framePassword.setMaximumSize(QtCore.QSize(350, 100))
        self.framePassword.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.framePassword.setFrameShadow(QtWidgets.QFrame.Raised)
        self.framePassword.setObjectName("framePassword")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.framePassword)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        # Password title and input
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

        # Frame for the submit button
        self.frameBouton = QtWidgets.QFrame(self.frameMire)
        self.frameBouton.setMinimumSize(QtCore.QSize(150, 100))
        self.frameBouton.setMaximumSize(QtCore.QSize(150, 100))
        self.frameBouton.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameBouton.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameBouton.setObjectName("frameBouton")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frameBouton)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        # Submit button
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

        # "Créer un compte" label (link)
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
        self.boutonCreerCompte.linkActivated.connect(self.show_signup_form)  # Connect the label to open signup form
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

        # Add a state variable to track current form
        self.is_login_form = True

        # Store MainWindow reference
        self.main_window = MainWindow

        # Initialize the form state and connections
        self.update_form_state()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # def bouton_animation(self):
    #     self.boutonValider.setFocus()
    #     self.handle_login()
    #     QtCore.QTimer.singleShot(100, self.boutonValider.clearFocus)

    def show_signup_form(self):
        """Toggle between login and signup forms"""
        self.is_login_form = not self.is_login_form
        self.update_form_state()

    def update_form_state(self):
        """Update form labels and button connections based on current state"""
        _translate = QtCore.QCoreApplication.translate

        # Disconnect any existing connections
        try:
            self.boutonValider.clicked.disconnect()
            self.inputMail.returnPressed.disconnect()
            self.inputPassword.returnPressed.disconnect()
        except:
            pass  # No connections to disconnect

        if self.is_login_form:
            # Login form state
            self.main_window.setWindowTitle(_translate("MainWindow", "TaskFlow - Login"))
            self.label.setText(_translate("MainWindow", "S'identifier"))
            self.boutonValider.setText(_translate("MainWindow", "Valider"))
            self.boutonCreerCompte.setText("<a href='#'>Créer un compte</a>")
            self.inputPassword.setPlaceholderText("")
            self.inputMail.setPlaceholderText("")

            # Set login form connections
            self.boutonValider.clicked.connect(self.handle_login)
            self.inputMail.returnPressed.connect(self.handle_login)
            self.inputPassword.returnPressed.connect(self.handle_login)
        else:
            # Signup form state
            self.main_window.setWindowTitle(_translate("MainWindow", "TaskFlow - Inscription"))
            self.label.setText(_translate("MainWindow", "Créer un compte"))
            self.boutonValider.setText(_translate("MainWindow", "S'inscrire"))
            self.boutonCreerCompte.setText("<a href='#'>Retour</a>")
            self.inputPassword.setPlaceholderText("Minimum 8 caractères")
            self.inputMail.setPlaceholderText("exemple@email.com")

            # Set signup form connections
            self.boutonValider.clicked.connect(self.handle_signup)
            self.inputMail.returnPressed.connect(self.handle_signup)
            self.inputPassword.returnPressed.connect(self.handle_signup)

    def handle_login(self):
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

    def handle_signup(self):
        """Handle signup form submission"""
        email = self.inputMail.text()
        password = self.inputPassword.text()

        # Basic validation
        if not self.validate_email(email):
            self.show_error_message("Erreur d'inscription", "Veuillez entrer une adresse email valide")
            return False

        if len(password) < 8:
            self.show_error_message("Erreur d'inscription", "Le mot de passe doit contenir au moins 8 caractères")
            return False

        # Check if email already exists
        existing_user = DB_API.get_email_hashpass(email)
        if existing_user and not isinstance(existing_user, Exception):
            self.show_error_message("Erreur d'inscription", "Cette adresse email est déjà utilisée")
            return False

        # Create new user
        try:
            # Assuming DB_API has a create_user method - you'll need to implement this
            success = DB_API.create_user(email, password)
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
        """Basic email validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def show_error_message(self, title, message):
        """Show error message dialog"""
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    def show_success_message(self, title, message):
        """Show success message dialog"""
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    def load_stylesheet(self, MainWindow):
        with open("style.qss", "r") as file:
            stylesheet = file.read()
            MainWindow.setStyleSheet(stylesheet)

    def open_main_window(self):
        # Fermer la fenêtre de connexion actuelle
        self.main_window.close()

        # Créer et afficher la fenêtre principale
        self.main_window_instance = QtWidgets.QMainWindow()
        self.main_window_ui = MainWindowUI()
        self.main_window_ui.setupUi(self.main_window_instance)
        self.main_window_instance.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("TaskFlow - Login", "TaskFlow - Login"))
        self.label.setText(_translate("MainWindow", "S'identifier"))
        self.titreMail.setText(_translate("MainWindow", "E-Mail"))
        self.titrePassword.setText(_translate("MainWindow", "Mot de passe"))
        self.boutonValider.setText(_translate("MainWindow", "Valider"))