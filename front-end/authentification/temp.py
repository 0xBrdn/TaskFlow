from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QFont


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)

        # Définir le widget central avec le nom d'objet pour le style QSS
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Charger la feuille de style QSS
        with open('styles.qss', 'r') as f:
            MainWindow.setStyleSheet(f.read())

        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout.setObjectName("layout")

        # Onglets pour séparer les projets, les tâches et le compte
        self.tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.tabs.setObjectName("tabs")

        self.project_tab = QtWidgets.QWidget()
        self.project_tab.setObjectName("project_tab")

        self.task_tab = QtWidgets.QWidget()
        self.task_tab.setObjectName("task_tab")

        self.account_tab = QtWidgets.QWidget()
        self.account_tab.setObjectName("account_tab")

        self.tabs.addTab(self.project_tab, "Projets")
        self.tabs.addTab(self.task_tab, "Tâches")
        self.tabs.addTab(self.account_tab, "Compte")
        self.layout.addWidget(self.tabs)

        # Configurations des onglets existants (projets et tâches)
        self._setup_project_tab()
        self._setup_task_tab()
        self._setup_account_tab()

        MainWindow.setCentralWidget(self.centralwidget)

        # Connexions
        self.add_project_button.clicked.connect(self.add_project)
        self.project_list_widget.currentRowChanged.connect(self.project_clicked)
        self.add_task_button.clicked.connect(self.add_task)
        self.delete_task_button.clicked.connect(self.delete_task)
        self.complete_task_button.clicked.connect(self.mark_completed)

        # Données internes
        self.projects = {}
        self.current_user = None

    def _setup_project_tab(self):
        self.project_layout = QtWidgets.QVBoxLayout(self.project_tab)
        self.project_label = QtWidgets.QLabel("Liste des Projets")
        self.project_label.setObjectName("project_label")
        self.project_label.setStyleSheet("font-size: 20px; color: white;")
        self.project_layout.addWidget(self.project_label)

        self.project_list_widget = QtWidgets.QListWidget()
        self.project_list_widget.setObjectName("project_list_widget")
        self.project_list_widget.setStyleSheet(
            "font-size: 14px; background-color: rgba(92, 92, 92, 190); color: white;")
        self.project_layout.addWidget(self.project_list_widget)

        self.add_project_button = QtWidgets.QPushButton("Ajouter un Projet")
        self.add_project_button.setObjectName("add_project_button")
        self.project_layout.addWidget(self.add_project_button)

    def _setup_task_tab(self):
        self.task_layout = QtWidgets.QVBoxLayout(self.task_tab)

        self.title_label = QtWidgets.QLabel(self.task_tab)
        self.title_label.setText("Gestionnaire de Tâches")
        self.title_label.setObjectName("task_title_label")
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        self.task_layout.addWidget(self.title_label)

        self.current_project_label = QtWidgets.QLabel(self.task_tab)
        self.current_project_label.setObjectName("current_project_label")
        self.current_project_label.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")
        self.task_layout.addWidget(self.current_project_label)

        self.table = QtWidgets.QTableWidget(self.task_tab)
        self.table.setObjectName("tasks_table")
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Tâche", "Sous-tâche", "Date", "Commentaire", "Importance"])
        self.table.setStyleSheet("background-color: rgba(92, 92, 92, 190); color: white;")
        self.task_layout.addWidget(self.table)

        # Reste du code de _setup_task_tab inchangé...
        # (Gardez l'implémentation précédente pour les inputs, boutons, etc.)

    def _setup_account_tab(self):
        layout = QVBoxLayout(self.account_tab)
        self.account_tab.setObjectName("account_tab")

        titre_label = QLabel("Informations du Compte")
        titre_label.setObjectName("account_title_label")
        titre_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; margin-bottom: 20px;")
        titre_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(titre_label)

        self.email_label = QLabel("Email: ")
        self.email_label.setObjectName("email_label")
        self.email_label.setStyleSheet("font-size: 16px; color: white; margin-bottom: 10px;")
        layout.addWidget(self.email_label)

        deconnexion_button = QPushButton("Se déconnecter")
        deconnexion_button.setObjectName("deconnexion_button")
        layout.addWidget(deconnexion_button)

        layout.addStretch(1)

    # Le reste des méthodes reste identique à votre implémentation précédente

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Gestionnaire de Projets et Tâches")

# Les autres méthodes restent identiques