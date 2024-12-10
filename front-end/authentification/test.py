from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QInputDialog


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Charger le fichier de style CSS
        with open('pagePrincipale.qss', 'r') as f:
            style = f.read()
            MainWindow.setStyleSheet(style)

        # Configuration de la fenêtre principale
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1769, 1098)
        MainWindow.setIconSize(QtCore.QSize(24, 25))

        # Création du widget central
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        # Création du widget avec icône et nom
        self.icon_name_widget = QtWidgets.QWidget(self.centralwidget)
        self.icon_name_widget.setMaximumSize(QtCore.QSize(70, 16777215))
        self.icon_name_widget.setObjectName("icon_name_widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.icon_name_widget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        # Configuration du logo
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.icon_name_widget)
        self.label.setMinimumSize(QtCore.QSize(50, 50))
        self.label.setMaximumSize(QtCore.QSize(50, 50))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("images/authentification/logo.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        # Configuration des boutons de navigation
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, 15, -1, -1)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")

        # Bouton Project
        self.bouton_project1 = QtWidgets.QPushButton(self.icon_name_widget)
        self.bouton_project1.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/pagePrincipale/dashboard_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap("images/pagePrincipale/dashboard.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.bouton_project1.setIcon(icon)
        self.bouton_project1.setCheckable(True)
        self.bouton_project1.setAutoExclusive(True)
        self.bouton_project1.setObjectName("bouton_project1")
        self.verticalLayout.addWidget(self.bouton_project1)

        # Bouton Profile
        self.bouton_profile1 = QtWidgets.QPushButton(self.icon_name_widget)
        self.bouton_profile1.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/pagePrincipale/profile_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap("images/pagePrincipale/profile.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.bouton_profile1.setIcon(icon1)
        self.bouton_profile1.setCheckable(True)
        self.bouton_profile1.setAutoExclusive(True)
        self.bouton_profile1.setObjectName("bouton_profile1")
        self.verticalLayout.addWidget(self.bouton_profile1)

        # Configuration des boutons de message
        self.bouton_message1 = QtWidgets.QPushButton(self.icon_name_widget)
        self.bouton_message1.setText("")

        # Configuration de l'icône du bouton message
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images/pagePrincipale/messages_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap("images/pagePrincipale/messages.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.bouton_message1.setIcon(icon2)

        # Paramètres du bouton message
        self.bouton_message1.setCheckable(True)
        self.bouton_message1.setAutoExclusive(True)
        self.bouton_message1.setObjectName("bouton_message1")
        self.verticalLayout.addWidget(self.bouton_message1)
        self.verticalLayout_3.addLayout(self.verticalLayout)

        # Ajout d'un espace extensible vertical
        spacerItem = QtWidgets.QSpacerItem(20, 418, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)

        # Configuration du bouton de sortie
        self.bouton_quitter1 = QtWidgets.QPushButton(self.icon_name_widget)
        self.bouton_quitter1.setText("")

        # Configuration de l'icône du bouton de sortie
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("images/pagePrincipale/log_out_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon3.addPixmap(QtGui.QPixmap("images/pagePrincipale/log_out.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.bouton_quitter1.setIcon(icon3)

        # Paramètres du bouton de sortie
        self.bouton_quitter1.setCheckable(True)
        self.bouton_quitter1.setAutoExclusive(True)
        self.bouton_quitter1.setObjectName("bouton_quitter1")
        self.verticalLayout_3.addWidget(self.bouton_quitter1)
        self.gridLayout_2.addWidget(self.icon_name_widget, 0, 0, 1, 1)


        # Configuration des connexions et événements
        self.bouton_project1.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.project))
        self.bouton_project2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.project))

        self.bouton_profile1.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Profile))
        self.bouton_profile2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Profile))

        self.bouton_message1.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.message))
        self.bouton_message2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.message))

    def retranslateUi(self, MainWindow):
        # Traduction des textes de l'interface
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        # Autres traductions similaires au code original