from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QLabel, QVBoxLayout, QPushButton, QInputDialog, QGroupBox, QHBoxLayout
from backend.db_api import DB_API
import datetime
from typing import Optional


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)

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
        self.tree.itemSelectionChanged.connect(self.update_subtask_availability)
        self.delete_account_button.clicked.connect(self.delete_account)
        self.add_user_button.clicked.connect(self.add_selected_user)
        self.remove_user_button.clicked.connect(self.remove_selected_user_from_list)
        self.delete_project_button.clicked.connect(self.delete_project)

        self.retranslateUi(MainWindow)

    def _setup_project_tab(self):
        self.project_layout = QtWidgets.QVBoxLayout(self.project_tab)
        self.project_label = QtWidgets.QLabel("Liste des Projets")
        self.project_label.setObjectName("project_label")
        self.project_label.setStyleSheet("font-size: 16px;")
        self.project_layout.addWidget(self.project_label)

        self.project_list_widget = QtWidgets.QListWidget()
        self.project_list_widget.setStyleSheet("font-size: 14px;")
        self.project_layout.addWidget(self.project_list_widget)

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
        self.project_layout.addWidget(self.project_buttons_frame)

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
        self.add_user_button.setStyleSheet("background-color: green; color: white; border-radius: 5px;")

        self.remove_user_button = QtWidgets.QPushButton("-", self.task_tab)
        self.remove_user_button.setFixedWidth(30)
        self.remove_user_button.setStyleSheet("background-color: red; color: white; border-radius: 5px;")

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

        self.add_task_button.setObjectName("add_task_button")
        self.add_subtask_button.setObjectName("add_subtask_button")
        self.delete_task_button.setObjectName("delete_task_button")
        self.complete_task_button.setObjectName("complete_task_button")

        self.modify_task_button = QtWidgets.QPushButton("Modifier", self.task_tab)
        self.modify_task_button.setObjectName("modify_task_button")
        self.button_layout.addWidget(self.modify_task_button)
        self.modify_task_button.clicked.connect(self.modify_task)

        self.button_layout.addWidget(self.add_task_button)
        self.button_layout.addWidget(self.add_subtask_button)
        self.button_layout.addWidget(self.delete_task_button)
        self.button_layout.addWidget(self.complete_task_button)
        self.task_layout.addLayout(self.button_layout)

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
        deconnexion_button.setStyleSheet("background-color: red; color: white; font-weight: bold; font-size:14px;")
        deconnexion_button.clicked.connect(self.deconnexion)
        account_layout.addWidget(deconnexion_button)

        self.delete_account_button = QPushButton("Supprimer mon compte")
        self.delete_account_button.setStyleSheet(
            "background-color: #a40000; color: white; font-weight: bold; font-size:14px;")
        account_layout.addWidget(self.delete_account_button)

        account_layout.addStretch(1)
        layout.addWidget(account_group)

    def set_current_user(self, email):
        self.current_user = email
        self.email_label.setText(f"Email: {email}")
        # Récupération du username et du rôle depuis la DB
        try:
            # Vérifiez que la méthode get_user_info existe dans db_api.
            user_info = DB_API.get_user_info(email)
            self.username_label.setText(f"Nom d'utilisateur : {user_info.get('username', 'Inconnu')}")
            self.role_label.setText(f"Rôle : {user_info.get('role', 'Inconnu')}")
        except:
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

    def delete_account(self):
        # Demander confirmation avant de supprimer le compte
        reponse = QMessageBox.question(
            None,
            "Supprimer le compte",
            "Êtes-vous sûr de vouloir supprimer votre compte ? Cette action est irréversible.",
            QMessageBox.Yes | QMessageBox.No
        )

        if reponse == QMessageBox.Yes:
            # Récupérer l'ID de l'utilisateur à partir de l'email
            user_id = DB_API.get_userID_by_email(self.current_user)
            if isinstance(user_id, Exception) or not user_id:
                QMessageBox.critical(None, "Erreur", "Impossible de récupérer l'ID de l'utilisateur.")
                return

            # Supprimer l'utilisateur et ses dépendances
            err = DB_API.delete_user(user_id[0])  # Appelle directement la fonction existante dans db_api.py
            if err is None:  # Si aucune erreur, suppression réussie
                QMessageBox.information(None, "Succès", "Compte supprimé avec succès.")

                # Fermer toutes les fenêtres et revenir à la fenêtre d'authentification
                QtWidgets.QApplication.closeAllWindows()
                from authentification import Ui_MainWindow as AuthMainWindow
                self.auth_window = QtWidgets.QMainWindow()
                self.auth_ui = AuthMainWindow()
                self.auth_ui.setupUi(self.auth_window)
                self.auth_window.show()
            else:
                # Gérer les erreurs de suppression
                QMessageBox.warning(None, "Erreur", f"Impossible de supprimer le compte : {err}")

    def add_project(self):
        project_name, ok = QInputDialog.getText(None, "Nouveau Projet", "Nom du projet :")
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
        self.assign_user_dropdown.clear()
        self.assigned_users_list.clear()

        try:
            project_id = DB_API.get_project_id_by_project_name(project_name)
            users_in_project = DB_API.get_users_in_project_by_project_id(project_id[0])
            for user in users_in_project:
                self.assign_user_dropdown.addItem(user[1])
        except Exception as e:
            QMessageBox.warning(None, "Erreur", f"Impossible de charger les utilisateurs du projet : {str(e)}")

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

        task_title = self.task_input.text().strip()
        task_date = self.date_input.date().toString("yyyy-MM-dd")
        task_comment = self.comment_input.text().strip()
        task_priority = self.importance_input.currentIndex()

        selected_users = [self.assigned_users_list.item(i).text() for i in range(self.assigned_users_list.count())]

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
                assign=task_projectID
            )

            user_id = DB_API.get_userID_by_email(self.current_user)
            DB_API.add_task(
                project_id=project_id[0],
                task_info_id=task_info_id,
                user_id=user_id[0]
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
                formatted_date = deadline.strftime("%d/%m/%Y") if isinstance(deadline, datetime.datetime) else str(
                    deadline)
                task_item.setText(1, formatted_date)
                task_item.setText(2, task[2])
                priority = task[4]
                priority_text = "Haute" if priority == 2 else "Moyenne" if priority == 1 else "Basse"
                task_item.setText(3, priority_text)

                assigned_users = DB_API.get_users_in_tasks_group_by_group_id(task[6])
                users_text = ", ".join(
                    [user[1] for user in assigned_users]) if assigned_users else "Aucun utilisateur assigné"
                task_item.setText(4, users_text)

                color_map = {"Haute": "red", "Moyenne": "orange", "Basse": "green"}
                task_item.setForeground(3, QtGui.QColor(color_map.get(priority_text, "black")))

                task_item.setData(0, QtCore.Qt.UserRole, task[0])

                subtasks = DB_API.get_subtasks_by_task_id(task[0])
                for subtask in subtasks:
                    subtask_item = QtWidgets.QTreeWidgetItem(task_item)
                    subtask_item.setText(0, subtask[1])
                    subtask_item.setText(1, subtask[7].strftime("%d/%m/%Y"))
                    subtask_item.setText(2, subtask[2])
                    subtask_item.setText(3, "Haute" if subtask[4] == 2 else "Moyenne" if subtask[4] == 1 else "Basse")

                self.tree.setIndentation(20)

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

        # Récupérer la liste des utilisateurs sélectionnés
        selected_users = [self.assigned_users_list.item(i).text()
                          for i in range(self.assigned_users_list.count())]

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
                assign=task_projectID
            )

            DB_API.add_subtask(task_id=task_id, task_info_id=subtask_info_id)

            for user in selected_users:
                user_id = DB_API.get_user_id_by_username(user)
                if user_id:  # Vérifier que l'ID utilisateur existe
                    DB_API.add_user_to_task_group(task_projectID, user_id)

            # Créer l'élément visuel de la sous-tâche
            subtask_item = QtWidgets.QTreeWidgetItem(parent_item)
            subtask_item.setText(0, subtask_title)
            subtask_item.setText(1, subtask_date)
            subtask_item.setText(2, subtask_comment)
            subtask_item.setText(3,
                                 "Basse" if subtask_priority == 0 else "Moyenne" if subtask_priority == 1 else "Haute")
            subtask_item.setText(4, ", ".join(selected_users))  # Ajouter les utilisateurs assignés

            # Nettoyer les champs
            self.subtask_input.clear()
            self.comment_input.clear()
            self.importance_input.setCurrentIndex(0)
            self.assigned_users_list.clear()

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
        email = self.current_user
        userID = DB_API.get_userID_by_email(email)
        permission = DB_API.get_user_permission(project_id[0], userID[0])
        if permission[0] != 2:
            QMessageBox.warning(None, "Permission insuffisante",
                                "Vous n'avez pas la permission de supprimer ce projet.")
            return

        reponse = QMessageBox.question(
            None,
            "Supprimer le projet",
            f"Êtes-vous sûr de vouloir supprimer le projet '{project_name}' ? Cette action est irréversible.",
            QMessageBox.Yes | QMessageBox.No
        )

        if reponse == QMessageBox.Yes:
            DB_API.delete_user_group(project_id[0])
            err = DB_API.delete_project(project_id[0])

            if isinstance(err, Exception):
                print("Erreur lors de la suppression du projet")
                QMessageBox.critical(None, "Erreur", f"Impossible de supprimer le projet : {str(err)}")
                return

            self.project_list_widget.takeItem(self.project_list_widget.row(current_item))
            self.current_project = None
            if hasattr(self, 'current_project_label'):
                self.current_project_label.setText("Aucun projet sélectionné")
            if hasattr(self, 'tree'):
                self.tree.clear()

            QMessageBox.information(None, "Succès", "Le projet a été supprimé avec succès.")

    def modify_task(self):
        """Affiche les informations de la tâche sélectionnée dans les champs de saisie"""
        selected_items = self.tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(None, "Erreur", "Veuillez sélectionner une tâche à modifier.")
            return

        selected_item = selected_items[0]
        task_id = selected_item.data(0, QtCore.Qt.UserRole)

        try:
            task_info = DB_API.get_task_info_by_task_id(task_id)
            print(task_info)
            if not task_info:
                raise ValueError("Impossible de récupérer les informations de la tâche")

            # Les indices correspondent à la requête SQL:
            # 0: title, 1: description, 2: status, 3: priority, 4: covered, 5: assign, 6: dead_line

            # Remplir les champs avec les infos de la tâche
            self.task_input.setText(task_info[0])  # title
            self.comment_input.setText(task_info[1])  # description

            # Convertir et définir la date
            date = QtCore.QDate.fromString(task_info[6], "yyyy-MM-dd")
            self.date_input.setDate(date)

            # Définir la priorité
            self.importance_input.setCurrentIndex(task_info[3])  # priority

            # Remplir la liste des utilisateurs assignés
            self.assigned_users_list.clear()
            task_group_id = task_info[5]  # assign
            users = DB_API.get_users_in_tasks_group_by_group_id(task_group_id)
            for user in users:
                if user[1].strip():  # Supposant que user[1] est le username
                    self.assigned_users_list.addItem(user[1].strip())

            # Créer et afficher le bouton Appliquer s'il n'existe pas
            if not hasattr(self, 'apply_button'):
                self.apply_button = QtWidgets.QPushButton("Appliquer", self.task_tab)
                self.apply_button.setStyleSheet("background-color: #4CAF50; color: white;")
                self.button_layout.addWidget(self.apply_button)
                self.apply_button.clicked.connect(
                    lambda: self.apply_changes(selected_item, task_info[5]))  # Passer le task_group_id
            else:
                self.apply_button.show()

        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur lors du chargement des informations : {str(e)}")

    def apply_changes(self, item, task_group_id):
        """Applique les modifications aux champs"""
        try:
            task_id = item.data(0, QtCore.Qt.UserRole)
            task_info = DB_API.get_task_info_by_task_id(task_id)
            if not task_info:
                raise ValueError("Impossible de récupérer les informations de la tâche")

            # Récupérer les nouvelles valeurs
            new_title = self.task_input.text().strip()
            new_date = self.date_input.date().toString("yyyy-MM-dd")
            new_comment = self.comment_input.text().strip()
            new_priority = self.importance_input.currentIndex()

            # Mettre à jour la tâche dans la base de données
            DB_API.update_task_info(
                task_info_id=task_info[0],  # Supposant que c'est le task_infoID
                status=task_info[2],  # Garder le status actuel
                priority=new_priority,
                title=new_title,
                description=new_comment,
                dead_line=new_date,
                covered=task_info[4],  # Garder la valeur covered actuelle
                assign=task_group_id
            )

            # Mettre à jour les utilisateurs assignés
            DB_API.remove_all_users_from_task_group(task_group_id)
            for i in range(self.assigned_users_list.count()):
                username = self.assigned_users_list.item(i).text()
                user_id = DB_API.get_user_id_by_username(username)
                if user_id:
                    DB_API.add_user_to_task_group(task_group_id, user_id)

            # Mettre à jour l'affichage
            item.setText(0, new_title)
            item.setText(1, self.date_input.date().toString("dd/MM/yyyy"))
            item.setText(2, new_comment)
            item.setText(3, "Haute" if new_priority == 2 else "Moyenne" if new_priority == 1 else "Basse")
            item.setText(4, ", ".join([self.assigned_users_list.item(i).text()
                                       for i in range(self.assigned_users_list.count())]))

            # Nettoyer l'interface
            self.task_input.clear()
            self.comment_input.clear()
            self.importance_input.setCurrentIndex(0)
            self.assigned_users_list.clear()
            self.apply_button.hide()

            QMessageBox.information(None, "Succès", "Modifications appliquées avec succès.")

        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur lors de la modification : {str(e)}")

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
                    print(f"Erreur : utilisateur '{username}' introuvable ou erreur lors de la recherche.")
                    return False

            # Appeler la méthode de suppression
            result = DB_API.delete_user(user_id)
            if isinstance(result, Exception):
                print(f"Erreur lors de la suppression de l'utilisateur avec l'ID {user_id} : {result}")
                return False

            print(f"Utilisateur avec l'ID {user_id} supprimé avec succès.")
            return True

        except Exception as e:
            print(f"Erreur inattendue lors de la suppression de l'utilisateur : {e}")
            return False

    def send_invitation(self, user_id: int, permission: int, project_id: int):
        """
        Inviter un user dans son projet
        """
        user_group_id = DB_API.add_user_to_group(
            project_id=project_id, user_id=user_id, permission=permission, joined=False
        )
        if not user_group_id or isinstance(user_group_id, Exception):
            return None
        return user_group_id

    def get_invitation(self, user_id: int):
        """
        Cette fonction récupere les projets où l'utilisateur est invité
        """
        projects = DB_API.get_project_in_users_groups_userid(user_id=user_id)
        if not projects or isinstance(projects, Exception):
            return None
        return projects

    def set_invite(self, project_id: int, user_id: int, joined: bool):
        """
        Permet d'accepter ou refuser une invitation a un projet
        """
        err = DB_API.set_invites_status(project_id=project_id, user_id=user_id, joined=joined)
        if isinstance(err, Exception):
            return
        return


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
