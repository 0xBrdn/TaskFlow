from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QMessageBox,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QInputDialog,
    QGroupBox,
    QHBoxLayout,
    QListWidgetItem,
)
from backend.db_api import DB_API
import datetime
from typing import Optional


class InviteUsersDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, deny=False):
        super().__init__(parent)
        self.deny = deny
        self.setWindowTitle("Inviter des utilisateurs")
        self.setMinimumWidth(400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        if self.deny:
            error_label = QLabel(
                "Vous n'avez pas les permissions requises "
                "pour inviter des utilisateurs dans ce projet."
            )
            error_label.setStyleSheet("color: red; font-weight: bold; font-size: 14px;")
            layout.addWidget(error_label)

            close_button = QtWidgets.QPushButton("Fermer")
            close_button.clicked.connect(self.reject)
            layout.addWidget(close_button)
        else:
            # Liste des utilisateurs
            self.user_list = QtWidgets.QListWidget(self)
            self.user_list.setSelectionMode(QtWidgets.QListWidget.MultiSelection)
            layout.addWidget(QLabel("Sélectionnez les utilisateurs à inviter:"))
            layout.addWidget(self.user_list)

            # Droits d'accès
            rights_layout = QtWidgets.QHBoxLayout()
            self.rights_combo = QtWidgets.QComboBox(self)
            self.rights_combo.addItems(["lecture", "lecture + ecriture", "administration"])
            self.map_rights_combo = {"lecture": 0, "lecture + ecriture": 1, "administration": 2}
            rights_layout.addWidget(QtWidgets.QLabel("Droits d'accès:"))
            rights_layout.addWidget(self.rights_combo)
            layout.addLayout(rights_layout)

            # Boutons
            button_layout = QtWidgets.QHBoxLayout()
            self.invite_button = QtWidgets.QPushButton("Inviter")
            self.invite_button.setStyleSheet("""
                QPushButton {
                    background-color: #0066cc;
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #0080ff;
                }
            """)
            self.cancel_button = QtWidgets.QPushButton("Annuler")

            button_layout.addWidget(self.invite_button)
            button_layout.addWidget(self.cancel_button)
            layout.addLayout(button_layout)

            # Connexions
            self.invite_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)

    def load_users(self, users):
        self.user_list.clear()
        for user in users:
            item = QListWidgetItem(f"{user}")
            item.setData(QtCore.Qt.UserRole, user)
            self.user_list.addItem(item)

    def get_selected_users(self):
        selected_items = self.user_list.selectedItems()
        users = []
        rights = self.rights_combo.currentText()
        for item in selected_items:
            user = item.data(QtCore.Qt.UserRole)
            users.append((user, self.map_rights_combo.get(rights)))
        return users


class Ui_MainWindow(object):
    def __init__(self):
        self.current_user = None
        self.user_id = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("images/authentification/logo_alternatif.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        MainWindow.setWindowIcon(icon)

        # Chargement du fichier de style
        try:
            with open("style.qss", "r") as f:
                style = f.read()
                MainWindow.setStyleSheet(style)
        except FileNotFoundError:
            pass

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout.setObjectName("layout")

        # Onglets : Projets, Tâches, Compte
        self.tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.project_tab = QtWidgets.QWidget()
        self.task_tab = QtWidgets.QWidget()
        self.account_tab = QtWidgets.QWidget()
        self.tabs.addTab(self.project_tab, "Projets")
        self.tabs.addTab(self.task_tab, "Tâches")
        self.tabs.addTab(self.account_tab, "Compte")
        self.layout.addWidget(self.tabs)

        # Setup des onglets
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
        self.invite_users_button.clicked.connect(self.show_invite_dialog)
        self.tree.itemSelectionChanged.connect(self.update_subtask_availability)
        self.delete_account_button.clicked.connect(self.delete_account)
        self.add_user_button.clicked.connect(self.add_selected_user)
        self.remove_user_button.clicked.connect(self.remove_selected_user_from_list)
        self.delete_project_button.clicked.connect(self.delete_project)
        self.accept_project_button.clicked.connect(self.accept_project)
        self.refuse_project_button.clicked.connect(self.refuse_project)

        self.retranslateUi(MainWindow)

    def _setup_project_tab(self):
        # Layout principal horizontal pour diviser l'écran en deux
        self.main_project_layout = QtWidgets.QHBoxLayout(self.project_tab)

        # Partie gauche - Projets actifs
        self.left_widget = QtWidgets.QWidget()
        self.left_layout = QtWidgets.QVBoxLayout(self.left_widget)

        self.project_label = QtWidgets.QLabel("Projets Actifs")
        self.project_label.setObjectName("project_label")
        self.project_label.setStyleSheet("font-size: 16px;")
        self.left_layout.addWidget(self.project_label)

        self.project_list_widget = QtWidgets.QListWidget()
        self.project_list_widget.setStyleSheet("font-size: 14px;")
        self.left_layout.addWidget(self.project_list_widget)

        self.project_buttons_frame = QtWidgets.QFrame()
        self.project_buttons_frame.setObjectName("project_buttons_frame")
        self.project_buttons_layout = QtWidgets.QHBoxLayout(self.project_buttons_frame)

        self.add_project_button = QtWidgets.QPushButton("Ajouter un Projet")
        self.add_project_button.setObjectName("add_project_button")

        self.delete_project_button = QtWidgets.QPushButton("Supprimer le Projet")
        self.delete_project_button.setObjectName("delete_project_button")
        self.delete_project_button.setStyleSheet("""
            QPushButton#delete_project_button {
                background-color: #a40000;
                color: white;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#delete_project_button:hover {
                background-color: #cc0000;
            }
        """)

        self.project_buttons_layout.addWidget(self.add_project_button)
        self.project_buttons_layout.addWidget(self.delete_project_button)
        self.left_layout.addWidget(self.project_buttons_frame)

        # Partie droite - Projets en attente
        self.right_widget = QtWidgets.QWidget()
        self.right_layout = QtWidgets.QVBoxLayout(self.right_widget)

        self.pending_label = QtWidgets.QLabel("Projets en Attente")
        self.pending_label.setObjectName("pending_label")
        self.pending_label.setStyleSheet("font-size: 16px;")
        self.right_layout.addWidget(self.pending_label)

        self.pending_project = QtWidgets.QListWidget()
        self.pending_project.setStyleSheet("font-size: 14px;")
        self.right_layout.addWidget(self.pending_project)

        # Frame pour les boutons de projets en attente
        self.pending_buttons_frame = QtWidgets.QFrame()
        self.pending_buttons_frame.setObjectName("pending_buttons_frame")
        self.pending_buttons_layout = QtWidgets.QHBoxLayout(self.pending_buttons_frame)

        # Bouton Accepter (bleu)
        self.accept_project_button = QtWidgets.QPushButton("Accepter Projet")
        self.accept_project_button.setObjectName("accept_project_button")
        self.accept_project_button.setStyleSheet("""
            QPushButton#accept_project_button {
                background-color: #0066cc;
                color: white;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#accept_project_button:hover {
                background-color: #0080ff;
            }
        """)

        # Bouton Refuser (rouge)
        self.refuse_project_button = QtWidgets.QPushButton("Refuser Projet")
        self.refuse_project_button.setObjectName("refuse_project_button")
        self.refuse_project_button.setStyleSheet("""
            QPushButton#refuse_project_button {
                background-color: #a40000;
                color: white;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#refuse_project_button:hover {
                background-color: #cc0000;
            }
        """)

        self.pending_buttons_layout.addWidget(self.accept_project_button)
        self.pending_buttons_layout.addWidget(self.refuse_project_button)
        self.right_layout.addWidget(self.pending_buttons_frame)

        # Ajout des widgets gauche et droit au layout principal
        self.main_project_layout.addWidget(self.left_widget)
        self.main_project_layout.addWidget(self.right_widget)

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
        self.tree.setHeaderLabels(
            ["Tâche", "Date", "Commentaire", "Importance", "Utilisateurs assignés"]
        )
        self.tree.setStyleSheet("font-size: 14px;")
        self.task_layout.addWidget(self.tree)

        for i in range(4):
            self.tree.header().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

        self.form_layout = QtWidgets.QFormLayout()

        self.task_input = QtWidgets.QLineEdit(self.task_tab)
        self.task_input.setObjectName("task_input")

        self.subtask_input = QtWidgets.QLineEdit(self.task_tab)
        self.subtask_input.setObjectName("subtask_input")
        self.subtask_input.setPlaceholderText("veuillez sélectionner une tâche")
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

        assign_group = QGroupBox("Assigner des utilisateurs")
        assign_group.setStyleSheet("""
         QGroupBox {
             border: 2px solid #8f8f91;
             border-radius: 10px;
             margin-top: 1em;
             background-color: #e0f0ff;
         }
         QGroupBox:title {
             subcontrol-origin: margin;
             subcontrol-position: top center;
             padding: 0 3px;
             background-color: transparent;
         }
         """)
        assign_layout = QHBoxLayout(assign_group)

        self.assign_user_dropdown = QtWidgets.QComboBox(self.task_tab)
        self.assign_user_dropdown.setObjectName("assign_user_dropdown")
        self.assign_user_dropdown.setFixedWidth(150)

        self.add_user_button = QtWidgets.QPushButton("+", self.task_tab)
        self.add_user_button.setFixedWidth(30)
        self.add_user_button.setStyleSheet(
            "background-color: green; color: white; border-radius: 5px;"
        )

        self.remove_user_button = QtWidgets.QPushButton("-", self.task_tab)
        self.remove_user_button.setFixedWidth(30)
        self.remove_user_button.setStyleSheet(
            "background-color: red; color: white; border-radius: 5px;"
        )

        self.assigned_users_list = QtWidgets.QListWidget(self.task_tab)
        self.assigned_users_list.setFixedHeight(60)
        self.assigned_users_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        assign_layout.addWidget(self.assign_user_dropdown)
        assign_layout.addWidget(self.add_user_button)
        assign_layout.addWidget(self.remove_user_button)
        assign_layout.addWidget(self.assigned_users_list)

        self.form_layout.addRow("Assigner un ou plusieurs utilisateurs :", assign_group)
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
        self.invite_users_button = QtWidgets.QPushButton("Inviter des utilisateurs", self.task_tab)

        self.add_task_button.setObjectName("add_task_button")
        self.add_subtask_button.setObjectName("add_subtask_button")
        self.delete_task_button.setObjectName("delete_task_button")
        self.complete_task_button.setObjectName("complete_task_button")
        self.invite_users_button.setObjectName("invite_user")

        self.modify_task_button = QtWidgets.QPushButton("Modifier", self.task_tab)
        self.modify_task_button.setObjectName("modify_task_button")
        self.button_layout.addWidget(self.modify_task_button)
        self.modify_task_button.clicked.connect(self.modify_task)

        self.button_layout.addWidget(self.add_task_button)
        self.button_layout.addWidget(self.add_subtask_button)
        self.button_layout.addWidget(self.delete_task_button)
        self.button_layout.addWidget(self.complete_task_button)
        self.button_layout.addWidget(self.invite_users_button)
        self.task_layout.addLayout(self.button_layout)

        self.uncomplete_task_button = QtWidgets.QPushButton("Marquer comme non terminé", self.task_tab)
        self.uncomplete_task_button.setObjectName("uncomplete_task_button")
        self.button_layout.addWidget(self.uncomplete_task_button)

        # Connectez le bouton à la nouvelle fonction
        self.uncomplete_task_button.clicked.connect(self.mark_uncompleted)

    def _setup_account_tab(self):
        layout = QVBoxLayout(self.account_tab)

        account_group = QGroupBox("Informations du Compte")
        account_group.setStyleSheet("font-size: 16px;")
        account_layout = QVBoxLayout(account_group)

        logo_label = QLabel()
        try:
            pixmap = QtGui.QPixmap("images/logo_alternatif.png")
            pixmap = pixmap.scaledToWidth(150, QtCore.Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
            logo_label.setAlignment(QtCore.Qt.AlignCenter)
        except Exception as e:
            print(f"Impossible de charger le logo : {e}")
        account_layout.addWidget(logo_label)

        self.email_label = QLabel("Email: ")
        self.email_label.setObjectName("email_label")
        self.email_label.setStyleSheet("font-size: 14px;")
        account_layout.addWidget(self.email_label)

        self.username_label = QLabel("Nom d'utilisateur : Inconnu")
        self.username_label.setStyleSheet("font-size: 14px;")
        account_layout.addWidget(self.username_label)

        self.role_label = QLabel("Rôle : Inconnu")
        self.role_label.setStyleSheet("font-size: 14px;")
        account_layout.addWidget(self.role_label)

        deconnexion_button = QPushButton("Se déconnecter")
        deconnexion_button.setObjectName("deconnexion_button")
        deconnexion_button.setStyleSheet(
            "background-color: red; color: white; font-weight: bold; font-size:14px;"
        )
        deconnexion_button.clicked.connect(self.deconnexion)
        account_layout.addWidget(deconnexion_button)

        self.delete_account_button = QPushButton("Supprimer mon compte")
        self.delete_account_button.setStyleSheet(
            "background-color: #a40000; color: white; font-weight: bold; font-size:14px;"
        )
        account_layout.addWidget(self.delete_account_button)

        account_layout.addStretch(1)
        layout.addWidget(account_group)

    def set_current_user(self, email):
        self.current_user = email
        self.user_id = DB_API.get_userID_by_email(email)[0]
        self.email_label.setText(f"Email: {email}")
        # Récupération du username et du rôle depuis la DB
        try:
            # Vérifiez que la méthode get_user_info existe dans db_api.
            user_info = DB_API.get_user_info(email)
            self.username_label.setText(
                f"Nom d'utilisateur : {user_info.get('username', 'Inconnu')}"
            )
            self.role_label.setText(f"Rôle : {user_info.get('role', 'Inconnu')}")
        except Exception:
            self.username_label.setText("Nom d'utilisateur : Inconnu")
            self.role_label.setText("Rôle : Inconnu")

        self.load_projects()

    def deconnexion(self):
        from authentification import Ui_MainWindow as AuthMainWindow

        QMessageBox.information(None, "Déconnexion", "Vous êtes maintenant déconnecté.")
        QtWidgets.QApplication.closeAllWindows()

        self.auth_window = QtWidgets.QMainWindow()
        self.auth_ui = AuthMainWindow()
        self.auth_ui.setupUi(self.auth_window)
        self.auth_window.show()

        self.user_id = None
        self.current_user = None

    def delete_account(self):
        # Demander confirmation avant de supprimer le compte
        reponse = QMessageBox.question(
            None,
            "Supprimer le compte",
            "Êtes-vous sûr de vouloir supprimer votre compte ? Cette action est irréversible.",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reponse == QMessageBox.Yes:
            # Récupérer l'ID de l'utilisateur à partir de l'email
            user_id = DB_API.get_userID_by_email(self.current_user)
            if isinstance(user_id, Exception) or not user_id:
                QMessageBox.critical(
                    None, "Erreur", "Impossible de récupérer l'ID de l'utilisateur."
                )
                return

            # Supprimer l'utilisateur et ses dépendances
            err = DB_API.delete_user(
                user_id[0]
            )  # Appelle directement la fonction existante dans db_api.py
            if err is None:  # Si aucune erreur, suppression réussie
                QMessageBox.information(None, "Succès", "Compte supprimé avec succès.")

                # Fermer toutes les fenêtres et revenir à la fenêtre d'authentification
                QtWidgets.QApplication.closeAllWindows()
                from authentification import Ui_MainWindow as AuthMainWindow

                self.auth_window = QtWidgets.QMainWindow()
                self.auth_ui = AuthMainWindow()
                self.auth_ui.setupUi(self.auth_window)
                self.auth_window.show()
                self.user_id = None
                self.current_user = None
            else:
                # Gérer les erreurs de suppression
                QMessageBox.warning(None, "Erreur", f"Impossible de supprimer le compte : {err}")

    def add_project(self):
        project_name, ok = QInputDialog.getText(None, "Nouveau Projet", "Nom du projet :")
        if not ok or not project_name.strip():
            return
        existant = DB_API.check_projects(project_name)
        if existant:
            return
        project_id = DB_API.add_project(project_name)
        permission = 2
        joined = 2
        DB_API.add_user_to_group(project_id, self.user_id, permission, joined)
        self.load_projects()

    def load_projects(self):
        self.project_list_widget.clear()
        self.pending_project.clear()
        try:
            projects = DB_API.get_projects_by_user_id(self.user_id)
            if projects:
                for project in projects:
                    project_id, project_name, joined = project
                    if joined == 2:
                        self.project_list_widget.addItem(f"{project_name}")
            pending_project = self.get_invitation(user_id=self.user_id, only_pending=True)
            if pending_project:
                for p_project in pending_project:
                    project_id, project_name, permission, joined = p_project
                    self.pending_project.addItem(f"{project_name}")

        except Exception as e:
            QMessageBox.warning(None, "Erreur", f"Impossible de charger les projets : {e!s}")

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
        self.assign_user_dropdown.clear()
        self.assigned_users_list.clear()

        try:
            project_id = DB_API.get_project_id_by_project_name(project_name)
            users_in_project = DB_API.get_users_in_project_by_project_id(project_id[0])
            for user in users_in_project:
                self.assign_user_dropdown.addItem(user[1])
        except Exception as e:
            QMessageBox.warning(
                None, "Erreur", f"Impossible de charger les utilisateurs du projet : {e!s}"
            )

    def add_selected_user(self):
        selected_user = self.assign_user_dropdown.currentText().strip()
        if selected_user and not self.is_user_already_assigned(selected_user):
            self.assigned_users_list.addItem(selected_user)

    def remove_selected_user_from_list(self):
        items = self.assigned_users_list.selectedItems()
        if items:
            for item in items:
                self.assigned_users_list.takeItem(self.assigned_users_list.row(item))

    def is_user_already_assigned(self, username: str) -> bool:
        for i in range(self.assigned_users_list.count()):
            if self.assigned_users_list.item(i).text() == username:
                return True
        return False

    def add_task(self):
        if not self.current_project:
            QMessageBox.warning(None, "Erreur", "Veuillez sélectionner un projet.")
            return

        project_id = DB_API.get_project_id_by_project_name(self.current_project)
        userID = DB_API.get_userID_by_email(self.current_user)
        permission = DB_API.get_user_permission(project_id[0], userID[0])
        if permission[0] < 1:
            QMessageBox.warning(
                None,
                "Permission insuffisante",
                "Vous n'avez pas la permission pour ajouter cette tâche.",
            )
            return

        task_title = self.task_input.text().strip()
        task_date = self.date_input.date().toString("yyyy-MM-dd")
        task_comment = self.comment_input.text().strip()
        task_priority = self.importance_input.currentIndex()

        selected_users = [
            self.assigned_users_list.item(i).text()
            for i in range(self.assigned_users_list.count())
        ]

        if not task_title:
            QMessageBox.warning(None, "Erreur", "Veuillez entrer une tâche.")
            return

        if not selected_users:
            QMessageBox.warning(None, "Erreur", "Veuillez assigner au moins un utilisateur.")
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
                assign=task_projectID,
            )

            DB_API.add_task(
                project_id=project_id[0], task_info_id=task_info_id, user_id=self.user_id
            )

            for user in selected_users:
                uid = DB_API.get_user_id_by_username(user)
                DB_API.add_user_to_task_group(task_projectID, uid)

            QMessageBox.information(None, "Succès", "Tâche ajoutée avec succès.")
            self.load_tasks_for_project(self.current_project)

            self.task_input.clear()
            self.comment_input.clear()
            self.importance_input.setCurrentIndex(0)
            self.assigned_users_list.clear()

        except Exception as e:
            QMessageBox.critical(
                None, "Erreur", f"Une erreur s'est produite lors de l'ajout de la tâche : {e!s}"
            )

    def load_tasks_for_project(self, project_name):
        self.tree.clear()
        try:
            project_id = DB_API.get_project_id_by_project_name(project_name)
            tasks = DB_API.get_tasks_by_project_id(project_id[0])
            for task in tasks:
                task_item = QtWidgets.QTreeWidgetItem(self.tree)
                task_item.setText(0, task[1])  # Titre de la tâche
                deadline = task[7]
                formatted_date = (
                    deadline.strftime("%d/%m/%Y")
                    if isinstance(deadline, datetime.datetime)
                    else str(deadline)
                )
                task_item.setText(1, formatted_date)  # Date limite
                task_item.setText(2, task[2])  # Description
                priority = task[4]
                priority_text = (
                    "Haute" if priority == 2 else "Moyenne" if priority == 1 else "Basse"
                )
                task_item.setText(3, priority_text)  # Priorité

                assigned_users = DB_API.get_users_in_tasks_group_by_group_id(task[6])
                users_text = (
                    ", ".join([user[1] for user in assigned_users])
                    if assigned_users
                    else "Aucun utilisateur assigné"
                )
                task_item.setText(4, users_text)  # Utilisateurs assignés

                # Stocker l'ID réel de la tâche pour un usage futur
                task_item.setData(0, QtCore.Qt.UserRole, task[0])

                # Vérifier le statut en direct et appliquer la couleur en fonction
                if task[3] == 1:  # Statut = 1 signifie "terminé"
                    self.set_task_background(task_item, "green")
                else:  # Statut différent de 1 signifie "non terminé"
                    self.set_task_background(task_item, "white")

                # Charger les sous-tâches
                subtasks = DB_API.get_subtasks_by_task_id(task[0])
                for subtask in subtasks:
                    subtask_item = QtWidgets.QTreeWidgetItem(task_item)
                    subtask_item.setText(0, subtask[1])  # Titre de la sous-tâche
                    subtask_item.setText(1, subtask[7].strftime("%d/%m/%Y"))  # Date limite
                    subtask_item.setText(2, subtask[2])  # Description
                    subtask_item.setText(
                        3,
                        "Haute" if subtask[4] == 2 else "Moyenne" if subtask[4] == 1 else "Basse",
                    )
                    subtask_item.setData(0, QtCore.Qt.UserRole, subtask[0])  # ID de la sous-tâche

                    # Vérifier le statut en direct et appliquer la couleur verte si terminé
                    if subtask[3] == 1:  # Statut = 1 signifie "terminé"
                        self.set_task_background(subtask_item, "green")
                    else:  # Statut différent de 1 signifie "non terminé"
                        self.set_task_background(subtask_item, "white")

            self.tree.setIndentation(20)

            # Mettre à jour les tâches périodiquement en cas de changement de statut
            self.refresh_task_status(project_id[0])

        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Impossible de charger les tâches : {e!s}")

    def set_task_background(self, item, color):
        """
        Applique un fond coloré à un item.
        """
        brush = QtGui.QBrush(QtGui.QColor(color))
        for i in range(item.columnCount()):
            item.setBackground(i, brush)

    def refresh_task_status(self, project_id):
        """
        Rafraîchit périodiquement le statut des tâches et met à jour la couleur.
        """
        tasks = DB_API.get_tasks_by_project_id(project_id)
        for i in range(self.tree.topLevelItemCount()):
            task_item = self.tree.topLevelItem(i)
            task_id = task_item.data(0, QtCore.Qt.UserRole)
            for task in tasks:
                if task[0] == task_id:
                    # Vérifier et appliquer la couleur en fonction du statut
                    if task[3] == 1:  # Statut = 1 signifie "terminé"
                        self.set_task_background(task_item, "green")
                    else:
                        self.set_task_background(task_item, "white")  # Couleur par défaut
                    break

        # Planifier un nouveau rafraîchissement après 2 secondes
        QtCore.QTimer.singleShot(2000, lambda: self.refresh_task_status(project_id))

    def add_subtask(self):
        selected_items = self.tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(None, "Erreur", "Veuillez sélectionner une tâche parente.")
            return

        project_id = DB_API.get_project_id_by_project_name(self.current_project)
        permission = DB_API.get_user_permission(project_id[0], self.user_id)
        if permission[0] < 1:
            QMessageBox.warning(
                None,
                "Permission insuffisante",
                "Vous n'avez pas la permission pour ajouter cette tâche.",
            )
            return

        parent_item = selected_items[0]
        subtask_title = self.subtask_input.text().strip()
        subtask_date = self.date_input.date().toString("yyyy-MM-dd")
        subtask_comment = self.comment_input.text().strip()
        subtask_priority = self.importance_input.currentIndex()

        # Récupérer la liste des utilisateurs sélectionnés
        selected_users = [
            self.assigned_users_list.item(i).text()
            for i in range(self.assigned_users_list.count())
        ]

        if not subtask_title:
            QMessageBox.warning(None, "Erreur", "Veuillez entrer une sous-tâche.")
            return

        if not selected_users:
            QMessageBox.warning(None, "Erreur", "Veuillez assigner au moins un utilisateur.")
            return

        try:
            task_id = parent_item.data(0, QtCore.Qt.UserRole)
            if not task_id:
                raise ValueError("ID de la tâche parente introuvable.")

            task_projectID = DB_API.add_task_group()

            subtask_info_id = DB_API.add_task_info(
                status=0,
                priority=subtask_priority,
                title=subtask_title,
                description=subtask_comment,
                dead_line=subtask_date,
                covered=0,
                assign=task_projectID,
            )

            DB_API.add_subtask(task_id=task_id, task_info_id=subtask_info_id)

            for user in selected_users:
                user_id = DB_API.get_user_id_by_username(user)
                if user_id:
                    DB_API.add_user_to_task_group(task_projectID, user_id)

            subtask_item = QtWidgets.QTreeWidgetItem(parent_item)
            subtask_item.setText(0, subtask_title)
            subtask_item.setText(1, subtask_date)
            subtask_item.setText(2, subtask_comment)
            subtask_item.setText(
                3,
                "Basse"
                if subtask_priority == 0
                else "Moyenne"
                if subtask_priority == 1
                else "Haute",
            )
            subtask_item.setText(4, ", ".join(selected_users))

            self.subtask_input.clear()
            self.comment_input.clear()
            self.importance_input.setCurrentIndex(0)
            self.assigned_users_list.clear()

            QMessageBox.information(None, "Succès", "Sous-tâche ajoutée avec succès.")

        except Exception as e:
            QMessageBox.critical(
                None,
                "Erreur",
                f"Une erreur s'est produite lors de l'ajout de la sous-tâche : {e!s}",
            )

    def delete_task(self):
        selected_items = self.tree.selectedItems()
        project_id = DB_API.get_project_id_by_project_name(self.current_project)
        userID = DB_API.get_userID_by_email(self.current_user)
        permission = DB_API.get_user_permission(project_id[0], userID[0])
        if permission[0] < 1:
            QMessageBox.warning(
                None,
                "Permission insuffisante",
                "Vous n'avez pas la permission pour supprimer cette tâche.",
            )
            return
        if not selected_items:
            QMessageBox.warning(None, "Erreur", "Veuillez sélectionner une tâche à supprimer.")
            return
        for item in selected_items:
            task_id = item.data(0, QtCore.Qt.UserRole)
            DB_API.delete_task(task_id)
            if item.parent():
                parent = item.parent()
                parent.removeChild(item)
            else:
                index = self.tree.indexOfTopLevelItem(item)
                self.tree.takeTopLevelItem(index)

    def delete_project(self):
        current_item = self.project_list_widget.currentItem()
        if not current_item:
            QMessageBox.warning(None, "Erreur", "Veuillez sélectionner un projet à supprimer.")
            return

        project_name = current_item.text()

        project_id = DB_API.get_project_id_by_project_name(project_name)
        permission = DB_API.get_user_permission(project_id[0], self.user_id)
        if permission[0] != 2:
            QMessageBox.warning(
                None,
                "Permission insuffisante",
                "Vous n'avez pas la permission de supprimer ce projet.",
            )
            return

        reponse = QMessageBox.question(
            None,
            "Supprimer le projet",
            f"Êtes-vous sûr de vouloir supprimer le projet "
            f"'{project_name}' ? Cette action est irréversible.",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reponse == QMessageBox.Yes:
            DB_API.delete_user_group(project_id[0])
            """
            DB_API.delete_tasks_groups(project_id[0])
            DB_API.delete_tasks_infos(project_id[0])
            DB_API.delete_tasks(project_id[0])
            Faire en sorte que les tâches se suppriment avec le projet
            """
            err = DB_API.delete_project(project_id[0])
            if isinstance(err, Exception):
                print("Erreur lors de la suppression du projet")
                QMessageBox.critical(
                    None, "Erreur", f"Impossible de supprimer le projet : {err!s}"
                )
                return

            self.project_list_widget.takeItem(self.project_list_widget.row(current_item))
            self.current_project = None
            if hasattr(self, "current_project_label"):
                self.current_project_label.setText("Aucun projet sélectionné")
            if hasattr(self, "tree"):
                self.tree.clear()

            QMessageBox.information(None, "Succès", "Le projet a été supprimé avec succès.")

    def modify_task(self):
        selected_items = self.tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(None, "Erreur", "Veuillez sélectionner une tâche à modifier.")
            return

        project_id = DB_API.get_project_id_by_project_name(self.current_project)
        userID = DB_API.get_userID_by_email(self.current_user)
        permission = DB_API.get_user_permission(project_id[0], userID[0])

        if permission[0] < 1:
            QMessageBox.warning(
                None,
                "Permission insuffisante",
                "Vous n'avez pas la permission pour modifier cette tâche.",
            )
            return

        selected_item = selected_items[0]
        parent_item = selected_item.parent()
        is_subtask = bool(parent_item)
        task_id = selected_item.data(0, QtCore.Qt.UserRole)

        if is_subtask:
            task_info = DB_API.get_subtask_info_by_subtask_id(task_id)
            task_info = task_info[0]
            task_infoID = DB_API.get_task_infoID_by_title(task_info[0])
        else:
            task_info = DB_API.get_task_info_by_task_id(task_id)
            task_info = task_info[0]
            task_infoID = DB_API.get_task_infoID_by_title(task_info[0])

        task_group_id = task_info[5]

        assigned_users = DB_API.get_users_in_tasks_group_by_group_id(task_group_id)
        all_users = DB_API.get_users_in_project_by_project_id(project_id[0])

        dialog = TaskEditDialog(
            parent=self.task_tab,
            task_info=task_info,
            assigned_users=assigned_users,
            all_users=all_users
        )

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            form_data = dialog.get_form_data()
            DB_API.update_task_title(form_data['title'], task_infoID[0])
            DB_API.update_task_description(form_data['comment'], task_infoID[0])
            DB_API.update_task_priority(form_data['priority'], task_infoID[0])
            DB_API.update_task_date(form_data['date'], task_infoID[0])
            DB_API.delete_users_from_users_tasks_groups(task_group_id)
            added_users = set()
            for username in form_data['assigned_users']:
                if username not in added_users:
                    user_id = DB_API.get_user_id_by_username(username)
                    if user_id:
                        DB_API.add_user_to_task_group(task_group_id, user_id)
                        added_users.add(username)

            selected_item.setText(0, form_data['title'])
            selected_item.setText(1, QtCore.QDate.fromString(form_data['date'], "yyyy-MM-dd").toString("dd/MM/yyyy"))
            selected_item.setText(2, form_data['comment'])
            selected_item.setText(
                3, "Haute" if form_data['priority'] == 2 else "Moyenne" if form_data['priority'] == 1 else "Basse"
            )
            selected_item.setText(4, ", ".join(form_data['assigned_users']))

            QMessageBox.information(None, "Succès", "Modifications appliquées avec succès.")

    def mark_completed(self):
        selected_items = self.tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(
                None, "Erreur", "Veuillez sélectionner une tâche à marquer comme terminée."
            )
            return

        project_id = DB_API.get_project_id_by_project_name(self.current_project)
        userID = DB_API.get_userID_by_email(self.current_user)
        permission = DB_API.get_user_permission(project_id[0], userID[0])

        if permission[0] < 1:
            QMessageBox.warning(
                None,
                "Permission insuffisante",
                "Vous n'avez pas la permission pour modifier cette tâche.",
            )
            return

        selected_item = selected_items[0]
        parent_item = selected_item.parent()
        is_subtask = bool(parent_item)
        task_id = selected_item.data(0, QtCore.Qt.UserRole)

        if is_subtask:
            task_info = DB_API.get_subtask_info_by_subtask_id(task_id)
            task_info = task_info[0]
            task_info_id = DB_API.get_task_infoID_by_title(task_info[0])
        else:
            task_info = DB_API.get_task_info_by_task_id(task_id)
            task_info = task_info[0]
            task_info_id = DB_API.get_task_infoID_by_title(task_info[0])

        if not task_id:
            QMessageBox.warning(
                None, "Erreur", "L'élément sélectionné ne contient pas un ID de tâche valide."
            )
            return

        if not task_info_id:
            QMessageBox.critical(
                None,
                "Erreur",
                "Impossible de récupérer les informations de la tâche sélectionnée.",
            )
            return

        success = DB_API.update_task_status(int(task_info_id[0]), 1)

        if success:
            QMessageBox.information(None, "Succès", "La tâche a été marquée comme terminée.")
        else:
            QMessageBox.critical(
                None,
                "Erreur",
                "Une erreur s'est produite lors de la mise à jour du statut de la tâche.",
            )
            return

    def mark_uncompleted(self):
        selected_items = self.tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(
                None, "Erreur", "Veuillez sélectionner une tâche à marquer comme non terminée."
            )
            return

        project_id = DB_API.get_project_id_by_project_name(self.current_project)
        userID = DB_API.get_userID_by_email(self.current_user)
        permission = DB_API.get_user_permission(project_id[0], userID[0])

        if permission[0] < 1:
            QMessageBox.warning(
                None,
                "Permission insuffisante",
                "Vous n'avez pas la permission pour modifier cette tâche.",
            )
            return

        selected_item = selected_items[0]
        parent_item = selected_item.parent()
        is_subtask = bool(parent_item)
        task_id = selected_item.data(0, QtCore.Qt.UserRole)

        if is_subtask:
            task_info = DB_API.get_subtask_info_by_subtask_id(task_id)
            task_info = task_info[0]
            task_info_id = DB_API.get_task_infoID_by_title(task_info[0])
        else:
            task_info = DB_API.get_task_info_by_task_id(task_id)
            task_info = task_info[0]
            task_info_id = DB_API.get_task_infoID_by_title(task_info[0])

        if not task_id:
            QMessageBox.warning(
                None, "Erreur", "L'élément sélectionné ne contient pas un ID de tâche valide."
            )
            return

        if not task_info_id:
            QMessageBox.critical(
                None,
                "Erreur",
                "Impossible de récupérer les informations de la tâche sélectionnée.",
            )
            return

        success = DB_API.update_task_status(int(task_info_id[0]), 0)

        if success:
            QMessageBox.information(None, "Succès", "La tâche a été marquée comme non terminée.")

            self.set_task_background(selected_items[0], "white")

            self.load_tasks_for_project(self.current_project)
        else:
            QMessageBox.critical(
                None,
                "Erreur",
                "Une erreur s'est produite lors de la mise à jour du statut de la tâche.",
            )
            return

    def update_subtask_availability(self):
        selected_items = self.tree.selectedItems()
        if selected_items:
            self.add_subtask_button.setEnabled(True)
            self.subtask_input.setEnabled(True)
        else:
            self.add_subtask_button.setEnabled(False)
            self.subtask_input.setEnabled(False)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("TaskFlow")

    def accept_project(self):
        selected_item = self.pending_project.currentItem()
        if selected_item:
            project = selected_item.text()
            self.project_list_widget.addItem(project)
            self.pending_project.takeItem(self.pending_project.row(selected_item))
            project_id = DB_API.get_project_id_by_project_name(project)[0]
            self.set_invite(project_id=project_id, user_id=self.user_id, joined=True)

    def refuse_project(self):
        selected_item = self.pending_project.currentItem()
        if selected_item:
            project = selected_item.text()
            self.pending_project.takeItem(self.pending_project.row(selected_item))
            project_id = DB_API.get_project_id_by_project_name(project)[0]
            self.set_invite(project_id=project_id, user_id=self.user_id, joined=False)

    def delete_user(self, username: str, user_id: Optional[int] = None) -> bool:
        """
        Supprime un utilisateur de la base de données en utilisant son username ou son user_id.

        :param username: Le nom d'utilisateur (utilisé si user_id n'est pas fourni).
        :param user_id: L'ID de l'utilisateur (prioritaire sur username si fourni).
        :return: True si la suppression a réussi, False sinon.
        """
        try:
            # Si l'user_id n'est pas fourni, récupérez-le avec le username
            if not user_id:
                user_id = DB_API.get_user_id_by_username(username)
                if user_id is None or isinstance(user_id, Exception):
                    print(
                        f"Erreur : utilisateur '{username}' introuvable "
                        f"ou erreur lors de la recherche."
                    )
                    return False

            # Appeler la méthode de suppression
            result = DB_API.delete_user(user_id)
            if isinstance(result, Exception):
                print(
                    f"Erreur lors de la suppression de l'utilisateur avec "
                    f"l'ID {user_id} : {result}"
                )
                return False

            print(f"Utilisateur avec l'ID {user_id} supprimé avec succès.")
            return True

        except Exception as e:
            print(f"Erreur inattendue lors de la suppression de l'utilisateur : {e}")
            return False

    def send_invitation(self, project_id: int, user_id: int, permission: int):
        """
        Inviter un user dans son projet
        """
        user_group_id = DB_API.add_user_to_group(
            project_id=project_id, user_id=user_id, permission=permission, joined=False
        )
        if not user_group_id or isinstance(user_group_id, Exception):
            return None
        return user_group_id

    def get_invitation(self, user_id: int, only_pending=False):
        """
        Cette fonction récupere les projets où l'utilisateur est invité

        Si only_pending = True, cela récupere seulement les invitations en attente,
        où il faut que l'utilisateur réponde, sinon la fonction revoie tous les
        projets dont l'utilisateur a accepté l'invitation

        :param user_id: ID de l'utilisateur
        :param only_pending: Récupère seulement les projets en attente
        """
        joined = 2
        if only_pending:
            joined = 0
        projects = DB_API.get_project_in_users_groups_userid(user_id=user_id)
        if not projects or isinstance(projects, Exception):
            return None
        return [item for item in projects if item[3] == joined]

    def set_invite(self, project_id: int, user_id: int, joined: bool):
        """
        Permet d'accepter ou refuser une invitation a un projet
        """
        if joined:
            _joined = 2
        else:
            _joined = 1
        err = DB_API.set_invites_status(project_id=project_id, user_id=user_id, joined=_joined)
        if isinstance(err, Exception):
            return
        return

    def get_user_to_invite(self, _list_users: list, _list_users_in_projects: list):
        list_users = [user[1] for user in _list_users]
        list_users_in_projects = [user[1] for user in _list_users_in_projects]
        return [user for user in list_users if user not in list_users_in_projects]

    def show_invite_dialog(self):
        project_id = DB_API.get_project_id_by_project_name(self.current_project)[0]
        _list_users = DB_API.get_all_users()
        _list_users_in_projects = DB_API.get_users_in_project_by_project_id(project_id)
        perms = next(user[2] for user in _list_users_in_projects if user[0] == self.user_id)
        if perms == 2:
            users = self.get_user_to_invite(_list_users, _list_users_in_projects)
            dialog = InviteUsersDialog(self.task_tab)
            dialog.load_users(users)

            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                selected_users = dialog.get_selected_users()
                for user, rights in selected_users:
                    user_id = next(u[0] for u in _list_users if u[1] == user)
                    print(user, rights, user_id, _list_users, project_id)
                    self.send_invitation(project_id, user_id, rights)
        else:
            dialog = InviteUsersDialog(self.task_tab, deny=True)
            dialog.exec_()


class TaskEditDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, task_info=None, assigned_users=None, all_users=None):
        super().__init__(parent)
        self.setWindowTitle("Modifier la tâche")
        self.setModal(True)
        self.resize(400, 500)

        layout = QtWidgets.QVBoxLayout(self)
        form_layout = QtWidgets.QFormLayout()

        self.title_input = QtWidgets.QLineEdit(self)
        self.title_input.setText(task_info[0] if task_info else "")

        self.date_input = QtWidgets.QDateEdit(self)
        self.date_input.setCalendarPopup(True)
        if task_info:
            date = QtCore.QDate(task_info[6].year, task_info[6].month, task_info[6].day)
            self.date_input.setDate(date)

        self.comment_input = QtWidgets.QLineEdit(self)
        self.comment_input.setText(task_info[1] if task_info else "")

        self.importance_input = QtWidgets.QComboBox(self)
        self.importance_input.addItems(["Faible", "Moyenne", "Haute"])
        if task_info:
            self.importance_input.setCurrentIndex(task_info[3])

        # Section des utilisateurs assignés
        assign_group = QtWidgets.QGroupBox("Assigner des utilisateurs")
        assign_layout = QtWidgets.QVBoxLayout()

        # Liste des utilisateurs disponibles et assignés
        user_selection_layout = QtWidgets.QHBoxLayout()

        self.assign_user_dropdown = QtWidgets.QComboBox(self)
        if all_users:
            self.assign_user_dropdown.addItems([user[1] for user in all_users])

        self.add_user_button = QtWidgets.QPushButton("+")
        self.add_user_button.setFixedWidth(30)
        self.add_user_button.setStyleSheet("background-color: green; color: white;")

        user_selection_layout.addWidget(self.assign_user_dropdown)
        user_selection_layout.addWidget(self.add_user_button)

        self.assigned_users_list = QtWidgets.QListWidget(self)
        self.assigned_users_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        if assigned_users:
            for user in assigned_users:
                if user[1].strip():
                    self.assigned_users_list.addItem(user[1].strip())

        self.remove_user_button = QtWidgets.QPushButton("-")
        self.remove_user_button.setFixedWidth(30)
        self.remove_user_button.setStyleSheet("background-color: red; color: white;")

        assign_layout.addLayout(user_selection_layout)
        assign_layout.addWidget(self.assigned_users_list)
        assign_layout.addWidget(self.remove_user_button)
        assign_group.setLayout(assign_layout)

        # Ajout des champs au formulaire
        form_layout.addRow("Titre :", self.title_input)
        form_layout.addRow("Date :", self.date_input)
        form_layout.addRow("Commentaire :", self.comment_input)
        form_layout.addRow("Importance :", self.importance_input)

        layout.addLayout(form_layout)
        layout.addWidget(assign_group)

        # Boutons de confirmation
        button_box = QtWidgets.QHBoxLayout()
        self.cancel_button = QtWidgets.QPushButton("Annuler")
        self.apply_button = QtWidgets.QPushButton("Appliquer")
        self.apply_button.setStyleSheet("background-color: #4CAF50; color: white;")

        button_box.addWidget(self.cancel_button)
        button_box.addWidget(self.apply_button)
        layout.addLayout(button_box)

        # Connexions des signaux
        self.cancel_button.clicked.connect(self.reject)
        self.apply_button.clicked.connect(self.accept)
        self.add_user_button.clicked.connect(self.add_selected_user)
        self.remove_user_button.clicked.connect(self.remove_selected_user)

    def add_selected_user(self):
        selected_user = self.assign_user_dropdown.currentText()
        if selected_user and not self.is_user_already_assigned(selected_user):
            self.assigned_users_list.addItem(selected_user)

    def remove_selected_user(self):
        current_item = self.assigned_users_list.currentItem()
        if current_item:
            self.assigned_users_list.takeItem(self.assigned_users_list.row(current_item))

    def is_user_already_assigned(self, username):
        for i in range(self.assigned_users_list.count()):
            if self.assigned_users_list.item(i).text() == username:
                return True
        return False

    def get_form_data(self):
        return {
            "title": self.title_input.text().strip(),
            "date": self.date_input.date().toString("yyyy-MM-dd"),
            "comment": self.comment_input.text().strip(),
            "priority": self.importance_input.currentIndex(),
            "assigned_users": [
                self.assigned_users_list.item(i).text()
                for i in range(self.assigned_users_list.count())
            ],
        }


if __name__ == "__main__":
    # u = Ui_MainWindow()
    # print(u.get_invitation(11, only_pending=True))
    # u.send_invitation(6, 25, 1)
    # u.send_invitation(9, 25, 1)
    # u.send_invitation(10, 25,1)
    # u.send_invitation(11, 25,1)
    # u.send_invitation(12, 25,1)
    # u.send_invitation(14, 25,1)
    # print(u.get_invitation(11, only_pending=True))
    # # u.send_invitation(11, 2, 12)
    # print(u.get_invitation(11, only_pending=True))

    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
