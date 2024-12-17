from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QLabel, QVBoxLayout, QPushButton, QInputDialog
from back_end.db_api import DB_API
import datetime
from typing import Optional


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
        self.tree.setColumnCount(5)
        self.tree.setHeaderLabels(["Tâche", "Date", "Commentaire", "Importance", "Utilisateurs assignés"])
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

        self.assign_input = QtWidgets.QListWidget(self.task_tab)
        self.assign_input.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.assign_input.setObjectName("assign_input")
        self.form_layout.addRow("Assigner un ou plusieurs utilisateurs :", self.assign_input)

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
        self.load_projects()

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

        try:
            project_id = DB_API.add_project(project_name)
            permission = 2
            joined = 1
            userID = DB_API.get_userID_by_email(self.current_user)
            DB_API.add_user_to_group(project_id, userID[0], permission, joined)

            self.load_projects()
        except Exception as e:
            QMessageBox.warning(None, "Erreur", f"Impossible d'ajouter le projet : {str(e)}")

    def load_projects(self):
        self.project_list_widget.clear()
        try:
            userID = DB_API.get_userID_by_email(self.current_user)

            projects = DB_API.get_projects_by_user_id(userID[0])

            for project in projects:
                self.project_list_widget.addItem(f"{project[1]}")

        except Exception as e:
            QMessageBox.warning(None, "Erreur", f"Impossible de charger les projets : {str(e)}")

    def project_clicked(self):
        project_index = self.project_list_widget.currentRow()
        if project_index >= 0:
            project_name_with_details = self.project_list_widget.item(project_index).text()
            project_name = project_name_with_details.split(" (")[0]
            self.current_project = project_name
            self.current_project_label.setText(f"Projet sélectionné : {project_name}")
            self.tabs.setCurrentWidget(self.task_tab)
            self.load_tasks_for_project(project_name)
            self.load_users_for_project(project_name)

    def load_users_for_project(self, project_name):
        self.assign_input.clear()

        try:
            project_id = DB_API.get_project_id_by_project_name(project_name)
            users_in_project = DB_API.get_users_in_project_by_project_id(project_id[0])

            for user in users_in_project:
                self.assign_input.addItem(user[1])  # Ajoute les utilisateurs à la liste
        except Exception as e:
            QMessageBox.warning(None, "Erreur", f"Impossible de charger les utilisateurs du projet : {str(e)}")

    def add_task(self):
        if not self.current_project:
            QMessageBox.warning(None, "Erreur", "Veuillez sélectionner un projet.")
            return

        task_title = self.task_input.text().strip()
        task_date = self.date_input.date().toString("yyyy-MM-dd")
        task_comment = self.comment_input.text().strip()
        task_priority = self.importance_input.currentIndex()

        selected_users = [item.text() for item in self.assign_input.selectedItems()]

        if not task_title:
            QMessageBox.warning(None, "Erreur", "Veuillez entrer une tâche.")
            return

        try:
            task_projectID = DB_API.add_task_group()
            project_id = DB_API.get_project_id_by_project_name(self.current_project)

            task_info_id = DB_API.add_task_info(
                status=0,
                priority=task_priority,
                title=task_title,
                description=task_comment,
                dead_line=task_date,
                covered=0,
                assign=task_projectID if selected_users else None
            )

            user_id = DB_API.get_userID_by_email(self.current_user)
            DB_API.add_task(
                project_id=project_id[0],
                task_info_id=task_info_id,
                user_id=user_id[0]
            )

            for user in selected_users:
                user_id = DB_API.get_userID_by_username(user)
                DB_API.add_user_to_task_group(task_projectID, user_id)

            QMessageBox.information(None, "Succès", "Tâche ajoutée avec succès.")
            self.load_tasks_for_project(self.current_project)

            self.task_input.clear()
            self.comment_input.clear()
            self.importance_input.setCurrentIndex(0)
            self.assign_input.clearSelection()

        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Une erreur s'est produite lors de l'ajout de la tâche : {str(e)}")

    def load_tasks_for_project(self, project_name):
        self.tree.clear()

        try:
            project_id = DB_API.get_project_id_by_project_name(project_name)
            tasks = DB_API.get_tasks_by_project_id(project_id[0])
            for task in tasks:
                task_item = QtWidgets.QTreeWidgetItem(self.tree)
                task_item.setText(0, task[1])
                deadline = task[7]
                if isinstance(deadline, datetime.datetime):
                    formatted_date = deadline.strftime("%d/%m/%Y")
                else:
                    formatted_date = str(deadline)
                task_item.setText(1, formatted_date)
                task_item.setText(2, task[2])
                priority = task[4]
                if priority == 3:
                    priority = "Haute"
                elif priority == 2:
                    priority = "Moyenne"
                elif priority == 1:
                    priority = "Basse"
                task_item.setText(3, priority)

                assigned_users = DB_API.get_users_in_tasks_group_by_group_id(task[6])
                if assigned_users:
                    users_text = ", ".join([user[1] for user in assigned_users])
                    task_item.setText(4, users_text)
                else:
                    task_item.setText(4, "Aucun utilisateur assigné")

                if priority == "Haute":
                    task_item.setForeground(3, QtGui.QColor("red"))
                elif priority == "Moyenne":
                    task_item.setForeground(3, QtGui.QColor("orange"))
                else:
                    task_item.setForeground(3, QtGui.QColor("green"))

                task_item.setData(0, QtCore.Qt.UserRole, task[0])
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Impossible de charger les tâches : {str(e)}")

    def add_subtask(self):
        selected_items = self.tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(None, "Erreur", "Veuillez sélectionner une tâche parente.")
            return

        parent_item = selected_items[0]
        subtask_title = self.subtask_input.text().strip()
        subtask_date = self.date_input.date().toString("yyyy-MM-dd")
        subtask_comment = self.comment_input.text().strip()
        subtask_priority = self.importance_input.currentIndex()

        if not subtask_title:
            QMessageBox.warning(None, "Erreur", "Veuillez entrer une sous-tâche.")
            return

        try:
            task_id = parent_item.data(0,QtCore.Qt.UserRole)

            if not task_id:
                raise ValueError("ID de la tâche parente introuvable.")

            subtask_info_id = DB_API.add_task_info(
                status=0,
                priority=subtask_priority,
                title=subtask_title,
                description=subtask_comment,
                dead_line=subtask_date,
                covered=0,
                assign=None
            )

            DB_API.add_subtask(
                task_id=task_id,
                task_info_id=subtask_info_id
            )

            subtask_item = QtWidgets.QTreeWidgetItem(parent_item)
            subtask_item.setText(0, subtask_title)
            subtask_item.setText(1, subtask_date)
            subtask_item.setText(2, subtask_comment)
            subtask_item.setText(3,
                                 "Basse" if subtask_priority == 1 else "Moyenne" if subtask_priority == 2 else "Haute")

            self.subtask_input.clear()
            self.comment_input.clear()
            self.importance_input.setCurrentIndex(0)

            QMessageBox.information(None, "Succès", "Sous-tâche ajoutée avec succès.")

        except Exception as e:
            QMessageBox.critical(None, "Erreur",
                                 f"Une erreur s'est produite lors de l'ajout de la sous-tâche : {str(e)}")

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

    def delete_user(username: str, user_id: Optional[int] = None) -> bool:
        """
        Permet de delete un utilisateur de la db et toutes ses dépendances.

        Cette fonction renvoie un boolean. En cas d'échec,
        elle renverra False et en cas de succes, elle renverra True.

        :param username: Username de l'utilisateur
        :param user_id: ID de l'utilisateur (optionnel)

        Exemple:
        >>> err = delete_user("toto")
        >>> if err:
        >>>     print("supprimé avec succes")
        >>> err = delete_user(user_id=4)
        >>> if err:
        >>>     print("supprimé avec succes")
        """
        if not user_id:
            user_id = DB_API.get_userID_by_username(username)
            if isinstance(user_id, Exception):
                return False
        err = DB_API.delete_user(user_id)
        if isinstance(err, Exception):
            return False
        return True
        # Faire un bouton dans la page compte pour pouvoir supprimer son compte, vérification avec mot de passe


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
