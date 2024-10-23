from PyQt5 import QtCore, QtGui, QtWidgets
import bcrypt
from backend.db_api import DB_API

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1035, 774)

        # Charger le fichier QSS
        self.load_stylesheet(MainWindow)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.frameMire = QtWidgets.QFrame(self.centralwidget)
        self.frameMire.setMinimumSize(QtCore.QSize(350, 30))
        self.frameMire.setMaximumSize(QtCore.QSize(350, 500))
        self.frameMire.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameMire.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameMire.setObjectName("frameMire")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frameMire)
        self.verticalLayout.setObjectName("verticalLayout")

        self.frameTitre = QtWidgets.QFrame(self.frameMire)
        self.frameTitre.setMinimumSize(QtCore.QSize(100, 60))
        self.frameTitre.setMaximumSize(QtCore.QSize(300, 60))
        self.frameTitre.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameTitre.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameTitre.setObjectName("frameTitre")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frameTitre)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

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

        self.frameLogin = QtWidgets.QFrame(self.frameMire)
        self.frameLogin.setMinimumSize(QtCore.QSize(350, 100))
        self.frameLogin.setMaximumSize(QtCore.QSize(350, 100))
        self.frameLogin.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameLogin.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameLogin.setObjectName("frameLogin")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frameLogin)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

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

        self.framePassword = QtWidgets.QFrame(self.frameMire)
        self.framePassword.setMinimumSize(QtCore.QSize(350, 100))
        self.framePassword.setMaximumSize(QtCore.QSize(350, 100))
        self.framePassword.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.framePassword.setFrameShadow(QtWidgets.QFrame.Raised)
        self.framePassword.setObjectName("framePassword")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.framePassword)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

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

        self.frameBouton = QtWidgets.QFrame(self.frameMire)
        self.frameBouton.setMinimumSize(QtCore.QSize(150, 100))
        self.frameBouton.setMaximumSize(QtCore.QSize(150, 100))
        self.frameBouton.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameBouton.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameBouton.setObjectName("frameBouton")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frameBouton)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

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
        self.gridLayout.addWidget(self.frameMire, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.inputMail.returnPressed.connect(self.bouton_animation)
        self.inputPassword.returnPressed.connect(self.bouton_animation)


    def bouton_animation(self):
        self.boutonValider.setFocus()
        self.handle_login()
        QtCore.QTimer.singleShot(100, self.boutonValider.clearFocus)

    def handle_login(self):
        email = self.inputMail.text()
        password = self.inputPassword.text()

        hashpass = DB_API.get_email_hashpass(email)
        if isinstance(hashpass, Exception) or not hashpass:
            print("Identifiant incorrect ou compte non local", hashpass)
            return False

        elif hashpass[0] == password:
            print("YAY")
            return True
        else:
            print("Identifiant ou mot de passe incorrect")
            return False

    def load_stylesheet(self, MainWindow):
        with open("style.qss", "r") as file:
            stylesheet = file.read()
            MainWindow.setStyleSheet(stylesheet)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "S'identifier"))
        self.titreMail.setText(_translate("MainWindow", "E-Mail"))
        self.titrePassword.setText(_translate("MainWindow", "Mot de passe"))
        self.boutonValider.setText(_translate("MainWindow", "Valider"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
