from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QLabel, QVBoxLayout, QPushButton


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)

        # Chargement du fichier de style
        with open('style.qss', 'r') as f:
            style = f.read()
            MainWindow.setStyleSheet(style)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout.setObjectName("layout")

        # Onglets pour séparer les projets, les tâches et le compte
        self.tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.project_tab = QtWidgets.QWidget()
        self.task_tab = QtWidgets.QWidget()
        self.account_tab = QtWidgets.QWidget()
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
        self.project_layout.addWidget(self.project_label)

        self.project_list_widget = QtWidgets.QListWidget()
        self.project_layout.addWidget(self.project_list_widget)

        self.add_project_button = QtWidgets.QPushButton("Ajouter un Projet")
        self.add_project_button.setObjectName("add_project_button")
        self.project_layout.addWidget(self.add_project_button)

    def _setup_task_tab(self):
        self.task_layout = QtWidgets.QVBoxLayout(self.task_tab)

        self.title_label = QtWidgets.QLabel(self.task_tab)
        self.title_label.setText("Gestionnaire de Tâches")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.task_layout.addWidget(self.title_label)

        self.current_project_label = QtWidgets.QLabel(self.task_tab)
        self.current_project_label.setAlignment(QtCore.Qt.AlignCenter)
        self.current_project_label.setObjectName("current_project_label")
        self.task_layout.addWidget(self.current_project_label)

        self.table = QtWidgets.QTableWidget(self.task_tab)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Tâche", "Sous-tâche", "Date", "Commentaire", "Importance"])
        self.task_layout.addWidget(self.table)

        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.form_layout = QtWidgets.QFormLayout()
        self.task_input = QtWidgets.QLineEdit(self.task_tab)
        self.task_input.setObjectName("task_input")

        self.subtask_input = QtWidgets.QLineEdit(self.task_tab)
        self.subtask_input.setObjectName("subtask_input")

        self.date_input = QtWidgets.QDateEdit(self.task_tab)
        self.date_input.setCalendarPopup(True)
        self.date_input.setObjectName("date_input")

        self.comment_input = QtWidgets.QLineEdit(self.task_tab)
        self.comment_input.setObjectName("comment_input")

        self.importance_input = QtWidgets.QComboBox(self.task_tab)
        self.importance_input.addItems(["Faible", "Moyenne", "Haute"])
        self.importance_input.setObjectName("importance_input")

        self.form_layout.addRow("Tâche :", self.task_input)
        self.form_layout.addRow("Sous-tâche :", self.subtask_input)
        self.form_layout.addRow("Date :", self.date_input)
        self.form_layout.addRow("Commentaire :", self.comment_input)
        self.form_layout.addRow("Importance :", self.importance_input)
        self.task_layout.addLayout(self.form_layout)

        self.button_layout = QtWidgets.QHBoxLayout()
        self.add_task_button = QtWidgets.QPushButton("Ajouter une Tâche", self.task_tab)
        self.delete_task_button = QtWidgets.QPushButton("Supprimer", self.task_tab)
        self.complete_task_button = QtWidgets.QPushButton("Marquer comme terminé", self.task_tab)

        self.add_task_button.setObjectName("add_task_button")
        self.delete_task_button.setObjectName("delete_task_button")
        self.complete_task_button.setObjectName("complete_task_button")

        self.button_layout.addWidget(self.add_task_button)
        self.button_layout.addWidget(self.delete_task_button)
        self.button_layout.addWidget(self.complete_task_button)
        self.task_layout.addLayout(self.button_layout)

    def _setup_account_tab(self):
        layout = QVBoxLayout(self.account_tab)

        # Titre
        titre_label = QLabel("Informations du Compte")
        titre_label.setObjectName("titre_label")
        titre_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(titre_label)

        # Email de l'utilisateur
        self.email_label = QLabel("Email: ")
        self.email_label.setObjectName("email_label")
        layout.addWidget(self.email_label)

        # Bouton de déconnexion
        deconnexion_button = QPushButton("Se déconnecter")
        deconnexion_button.setObjectName("deconnexion_button")
        deconnexion_button.clicked.connect(self.deconnexion)
        layout.addWidget(deconnexion_button)

        layout.addStretch(1)

    def set_current_user(self, email):
        self.current_user = email
        self.email_label.setText(f"Email: {email}")

    def deconnexion(self):
        from authentification import Ui_MainWindow as AuthMainWindow

        # Fermer la fenêtre actuelle
        self.main_window.close()

        # Ouvrir la fenêtre d'authentification
        self.main_window_auth = QtWidgets.QMainWindow()
        self.main_window_ui = AuthMainWindow()
        self.main_window_ui.setupUi(self.main_window_auth)
        self.main_window_ui.main_window = self.main_window_auth
        self.main_window_auth.show()

    # Les autres méthodes restent identiques à l'implémentation précédente
    def add_project(self):
        project_name, ok = QtWidgets.QInputDialog.getText(None, "Nouveau Projet", "Nom du projet :")
        if ok and project_name.strip():
            if project_name in self.projects:
                QMessageBox.warning(None, "Erreur", "Ce projet existe déjà.")
            else:
                self.projects[project_name] = []
                self.project_list_widget.addItem(project_name)
                QMessageBox.information(None, "Succès", f"Projet '{project_name}' ajouté.")

    def project_clicked(self):
        project_index = self.project_list_widget.currentRow()
        if project_index >= 0:
            project_name = self.project_list_widget.item(project_index).text()
            self.current_project_label.setText(f"Projet sélectionné : {project_name}")
            self.load_tasks()
            self.tabs.setCurrentWidget(self.task_tab)

    def load_tasks(self):
        project_index = self.project_list_widget.currentRow()
        if project_index >= 0:
            project_name = self.project_list_widget.item(project_index).text()
            self.table.setRowCount(0)
            for task, subtask, date, comment, importance, completed in self.projects[project_name]:
                row = self.table.rowCount()
                self.table.insertRow(row)
                task_item = QTableWidgetItem(task)
                subtask_item = QTableWidgetItem(subtask)
                date_item = QTableWidgetItem(date)
                comment_item = QTableWidgetItem(comment)
                importance_item = QTableWidgetItem(importance)

                if completed:
                    for item in [task_item, subtask_item, date_item, comment_item, importance_item]:
                        item.setBackground(QtGui.QColor("lightgreen"))
                        font = item.font()
                        font.setStrikeOut(True)
                        item.setFont(font)

                if importance == "Haute":
                    importance_item.setForeground(QtGui.QColor("red"))
                    font = importance_item.font()
                    font.setBold(True)
                    importance_item.setFont(font)
                elif importance == "Moyenne":
                    importance_item.setForeground(QtGui.QColor("orange"))
                else:
                    importance_item.setForeground(QtGui.QColor("green"))

                self.table.setItem(row, 0, task_item)
                self.table.setItem(row, 1, subtask_item)
                self.table.setItem(row, 2, date_item)
                self.table.setItem(row, 3, comment_item)
                self.table.setItem(row, 4, importance_item)

    def add_task(self):
        project_index = self.project_list_widget.currentRow()
        if project_index < 0:
            QMessageBox.warning(None, "Erreur", "Veuillez sélectionner un projet.")
            return

        project_name = self.project_list_widget.item(project_index).text()
        task = self.task_input.text().strip()
        subtask = self.subtask_input.text().strip()
        date = self.date_input.date().toString("dd/MM/yyyy")
        comment = self.comment_input.text().strip()
        importance = self.importance_input.currentText()

        if not task:
            QMessageBox.warning(None, "Erreur", "Veuillez entrer une tâche.")
            return

        self.projects[project_name].append((task, subtask, date, comment, importance, False))
        self.load_tasks()

        self.task_input.clear()
        self.subtask_input.clear()
        self.comment_input.clear()
        self.importance_input.setCurrentIndex(0)

    def delete_task(self):
        project_index = self.project_list_widget.currentRow()
        if project_index < 0:
            QMessageBox.warning(None, "Erreur", "Veuillez sélectionner un projet.")
            return

        project_name = self.project_list_widget.item(project_index).text()
        rows = sorted(set(index.row() for index in self.table.selectedIndexes()), reverse=True)
        if not rows:
            QMessageBox.warning(None, "Erreur", "Veuillez sélectionner une tâche à supprimer.")
            return

        for row in rows:
            del self.projects[project_name][row]
        self.load_tasks()

    def mark_completed(self):
        project_index = self.project_list_widget.currentRow()
        if project_index < 0:
            QMessageBox.warning(None, "Erreur", "Veuillez sélectionner un projet.")
            return

        project_name = self.project_list_widget.item(project_index).text()
        rows = sorted(set(index.row() for index in self.table.selectedIndexes()), reverse=True)
        if not rows:
            QMessageBox.warning(None, "Erreur", "Veuillez sélectionner une tâche à marquer comme terminée.")
            return

        for row in rows:
            task_data = self.projects[project_name][row]
            self.projects[project_name][row] = (*task_data[:-1], True)  # Marque comme terminé
        self.load_tasks()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Gestionnaire de Projets et Tâches")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())