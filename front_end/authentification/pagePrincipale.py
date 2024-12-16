from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QLabel, QVBoxLayout, QPushButton, QInputDialog


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)

        # Chargement du fichier de style
        try:
            with open('style.qss', 'r') as f:
                style = f.read()
                MainWindow.setStyleSheet(style)
        except FileNotFoundError:
            print("style.qss introuvable. Utilisation du style par défaut.")

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
        self.add_subtask_button.clicked.connect(self.add_subtask)
        self.delete_task_button.clicked.connect(self.delete_task)
        self.complete_task_button.clicked.connect(self.mark_completed)
        self.tree.itemSelectionChanged.connect(self.update_subtask_availability)

        # Données internes
        self.projects = {}
        self.users = ["zack", "maxime", "swann"]
        self.current_user = None
        self.current_project = None

    def _setup_project_tab(self):
        self.project_layout = QtWidgets.QVBoxLayout(self.project_tab)
        self.project_label = QtWidgets.QLabel("Liste des Projets")
        self.project_label.setObjectName("project_label")
        self.project_label.setStyleSheet("font-size: 16px;")
        self.project_layout.addWidget(self.project_label)

        self.project_list_widget = QtWidgets.QListWidget()
        self.project_list_widget.setStyleSheet("font-size: 14px;")
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
        self.title_label.setStyleSheet("font-size: 18px;")
        self.task_layout.addWidget(self.title_label)

        self.current_project_label = QtWidgets.QLabel(self.task_tab)
        self.current_project_label.setAlignment(QtCore.Qt.AlignCenter)
        self.current_project_label.setObjectName("current_project_label")
        self.current_project_label.setStyleSheet("font-size: 16px;")
        self.task_layout.addWidget(self.current_project_label)

        self.tree = QtWidgets.QTreeWidget(self.task_tab)
        self.tree.setColumnCount(4)
        self.tree.setHeaderLabels(["Tâche", "Date", "Commentaire", "Importance"])
        self.tree.setStyleSheet("font-size: 14px;")
        self.task_layout.addWidget(self.tree)

        for i in range(4):
            self.tree.header().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

        self.form_layout = QtWidgets.QFormLayout()

        self.task_input = QtWidgets.QLineEdit(self.task_tab)
        self.task_input.setObjectName("task_input")

        self.subtask_input = QtWidgets.QLineEdit(self.task_tab)
        self.subtask_input.setObjectName("subtask_input")
        self.subtask_input.setPlaceholderText("veuillez séléctionner une taches")
        self.subtask_input.setEnabled(False)

        self.date_input = QtWidgets.QDateEdit(self.task_tab)
        self.date_input.setCalendarPopup(True)
        self.date_input.setObjectName("date_input")
        self.date_input.setDate(QtCore.QDate(2025, 1, 1))

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
        self.add_subtask_button = QtWidgets.QPushButton("Ajouter Sous-Tâche", self.task_tab)
        self.add_subtask_button.setEnabled(False)
        self.delete_task_button = QtWidgets.QPushButton("Supprimer", self.task_tab)
        self.complete_task_button = QtWidgets.QPushButton("Marquer comme terminé", self.task_tab)

        self.add_task_button.setObjectName("add_task_button")
        self.add_subtask_button.setObjectName("add_subtask_button")
        self.delete_task_button.setObjectName("delete_task_button")
        self.complete_task_button.setObjectName("complete_task_button")

        self.button_layout.addWidget(self.add_task_button)
        self.button_layout.addWidget(self.add_subtask_button)
        self.button_layout.addWidget(self.delete_task_button)
        self.button_layout.addWidget(self.complete_task_button)
        self.task_layout.addLayout(self.button_layout)

    def _setup_account_tab(self):
        layout = QVBoxLayout(self.account_tab)
        titre_label = QLabel("Informations du Compte")
        titre_label.setObjectName("titre_label")
        titre_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(titre_label)

        self.email_label = QLabel("Email: ")
        self.email_label.setObjectName("email_label")
        layout.addWidget(self.email_label)

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

        QMessageBox.information(None, "Déconnexion", "Vous êtes maintenant déconnecté.")

        QtWidgets.QApplication.closeAllWindows()

        self.auth_window = QtWidgets.QMainWindow()
        self.auth_ui = AuthMainWindow()
        self.auth_ui.setupUi(self.auth_window)
        self.auth_window.show()

    def add_project(self):
        project_name, ok = QtWidgets.QInputDialog.getText(None, "Nouveau Projet", "Nom du projet :")
        if not ok or not project_name.strip():
            return

        user, ok_user = QtWidgets.QInputDialog.getItem(
            None, "Utilisateur", "Sélectionnez un utilisateur :", self.users, 0, False
        )
        if not ok_user:
            return

        creation_date = QtCore.QDate.currentDate().toString("dd/MM/yyyy")

        if project_name in self.projects:
            QMessageBox.warning(None, "Erreur", "Ce projet existe déjà.")
        else:
            self.projects[project_name] = {
                "tasks": [],
                "created_by": user,
                "created_on": creation_date
            }
            self.project_list_widget.addItem(f"{project_name} (par {user}, {creation_date})")

    def project_clicked(self):
        project_index = self.project_list_widget.currentRow()
        if project_index >= 0:
            project_name_with_details = self.project_list_widget.item(project_index).text()
            project_name = project_name_with_details.split(" (")[0]
            self.current_project = project_name
            self.current_project_label.setText(f"Projet sélectionné : {project_name}")
            self.tabs.setCurrentWidget(self.task_tab)
            self.load_tasks_for_project(project_name)

    def add_task(self):
        if not self.current_project:
            QMessageBox.warning(None, "Erreur", "Veuillez sélectionner un projet.")
            return

        task = self.task_input.text().strip()
        date = self.date_input.date().toString("dd/MM/yyyy")
        comment = self.comment_input.text().strip()
        importance = self.importance_input.currentText()

        if not task:
            QMessageBox.warning(None, "Erreur", "Veuillez entrer une tâche.")
            return

        task_item = QtWidgets.QTreeWidgetItem(self.tree)
        task_item.setText(0, task)
        task_item.setText(1, date)
        task_item.setText(2, comment)
        task_item.setText(3, importance)

        if importance == "Haute":
            task_item.setForeground(3, QtGui.QColor("red"))
        elif importance == "Moyenne":
            task_item.setForeground(3, QtGui.QColor("orange"))
        else:
            task_item.setForeground(3, QtGui.QColor("green"))

        self.projects[self.current_project]["tasks"].append({
            "task": task,
            "date": date,
            "comment": comment,
            "importance": importance
        })

        self.task_input.clear()
        self.comment_input.clear()
        self.importance_input.setCurrentIndex(0)

    def load_tasks_for_project(self, project_name):
        self.tree.clear()
        if project_name in self.projects:
            for task in self.projects[project_name]["tasks"]:
                task_item = QtWidgets.QTreeWidgetItem(self.tree)
                task_item.setText(0, task["task"])
                task_item.setText(1, task["date"])
                task_item.setText(2, task["comment"])
                task_item.setText(3, task["importance"])

                if task["importance"] == "Haute":
                    task_item.setForeground(3, QtGui.QColor("red"))
                elif task["importance"] == "Moyenne":
                    task_item.setForeground(3, QtGui.QColor("orange"))
                else:
                    task_item.setForeground(3, QtGui.QColor("green"))

    def add_subtask(self):
        selected_items = self.tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(None, "Erreur", "Veuillez sélectionner une tâche parente.")
            return

        parent_item = selected_items[0]
        subtask = self.subtask_input.text().strip()

        if not subtask:
            QMessageBox.warning(None, "Erreur", "Veuillez entrer une sous-tâche.")
            return

        subtask_item = QtWidgets.QTreeWidgetItem(parent_item)
        subtask_item.setText(0, subtask)
        subtask_item.setText(1, self.date_input.date().toString("dd/MM/yyyy"))
        subtask_item.setText(2, self.comment_input.text().strip())
        subtask_item.setText(3, self.importance_input.currentText())

        self.subtask_input.clear()
        self.comment_input.clear()
        self.importance_input.setCurrentIndex(0)

    def delete_task(self):
        selected_items = self.tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(None, "Erreur", "Veuillez sélectionner une tâche à supprimer.")
            return

        for item in selected_items:
            if item.parent():
                parent = item.parent()
                parent.removeChild(item)
            else:
                index = self.tree.indexOfTopLevelItem(item)
                self.tree.takeTopLevelItem(index)

                self.projects[self.current_project]["tasks"] = [
                    t for t in self.projects[self.current_project]["tasks"] if t["task"] != item.text(0)
                ]

    def mark_completed(self):
        selected_items = self.tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(None, "Erreur", "Veuillez sélectionner une tâche à marquer comme terminée.")
            return

        for item in selected_items:
            for col in range(4):
                item.setBackground(col, QtGui.QColor("lightgreen"))
                font = item.font(col)
                font.setStrikeOut(True)
                item.setFont(col, font)

    def update_subtask_availability(self):
        selected_items = self.tree.selectedItems()
        if selected_items:
            self.add_subtask_button.setEnabled(True)
            self.subtask_input.setEnabled(True)
        else:
            self.add_subtask_button.setEnabled(False)
            self.subtask_input.setEnabled(False)

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