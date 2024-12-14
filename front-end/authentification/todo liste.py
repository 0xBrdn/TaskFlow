from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setStyleSheet("background-color: white;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout.setObjectName("layout")

        # Onglets pour séparer les projets et les tâches
        self.tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.project_tab = QtWidgets.QWidget()
        self.task_tab = QtWidgets.QWidget()
        self.tabs.addTab(self.project_tab, "Projets")
        self.tabs.addTab(self.task_tab, "Tâches")
        self.layout.addWidget(self.tabs)

        # Interface de gestion des projets
        self.project_layout = QtWidgets.QVBoxLayout(self.project_tab)
        self.project_label = QtWidgets.QLabel("Liste des Projets")
        self.project_label.setStyleSheet("font-size: 20px; color: black;")
        self.project_layout.addWidget(self.project_label)

        self.project_list_widget = QtWidgets.QListWidget()
        self.project_list_widget.setStyleSheet("font-size: 14px; background-color: white; color: black;")
        self.project_layout.addWidget(self.project_list_widget)

        self.add_project_button = QtWidgets.QPushButton("Ajouter un Projet")
        self.add_project_button.setStyleSheet(
            "background-color: #2ecc71; color: white; font-size: 16px; font-weight: bold; padding: 10px; border-radius: 8px;"
        )
        self.project_layout.addWidget(self.add_project_button)

        # Interface de gestion des tâches
        self.task_layout = QtWidgets.QVBoxLayout(self.task_tab)

        self.title_label = QtWidgets.QLabel(self.task_tab)
        self.title_label.setText("Gestionnaire de Tâches")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: black;")
        self.task_layout.addWidget(self.title_label)

        # Affichage du nom du projet sélectionné
        self.current_project_label = QtWidgets.QLabel(self.task_tab)
        self.current_project_label.setAlignment(QtCore.Qt.AlignCenter)
        self.current_project_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50;")
        self.task_layout.addWidget(self.current_project_label)

        # Tableau pour afficher les tâches
        self.table = QtWidgets.QTableWidget(self.task_tab)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Tâche", "Sous-tâche", "Date", "Commentaire", "Importance"])
        self.table.setStyleSheet("background-color: white; font-size: 14px;")
        self.task_layout.addWidget(self.table)

        # Ajuster la largeur des colonnes
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Zone d'entrée pour ajouter une tâche
        self.form_layout = QtWidgets.QFormLayout()
        self.task_input = QtWidgets.QLineEdit(self.task_tab)
        self.task_input.setStyleSheet("font-size: 16px; padding: 8px;")

        self.subtask_input = QtWidgets.QLineEdit(self.task_tab)
        self.subtask_input.setStyleSheet("font-size: 16px; padding: 8px;")

        self.date_input = QtWidgets.QDateEdit(self.task_tab)
        self.date_input.setCalendarPopup(True)
        self.date_input.setStyleSheet("font-size: 16px; padding: 8px;")

        self.comment_input = QtWidgets.QLineEdit(self.task_tab)
        self.comment_input.setStyleSheet("font-size: 16px; padding: 8px;")

        self.importance_input = QtWidgets.QComboBox(self.task_tab)
        self.importance_input.addItems(["Faible", "Moyenne", "Haute"])
        self.importance_input.setStyleSheet("font-size: 16px; padding: 8px;")

        self.form_layout.addRow("Tâche :", self.task_input)
        self.form_layout.addRow("Sous-tâche :", self.subtask_input)
        self.form_layout.addRow("Date :", self.date_input)
        self.form_layout.addRow("Commentaire :", self.comment_input)
        self.form_layout.addRow("Importance :", self.importance_input)
        self.task_layout.addLayout(self.form_layout)

        # Boutons pour les actions
        self.button_layout = QtWidgets.QHBoxLayout()
        self.add_task_button = QtWidgets.QPushButton("Ajouter une Tâche", self.task_tab)
        self.delete_task_button = QtWidgets.QPushButton("Supprimer", self.task_tab)
        self.complete_task_button = QtWidgets.QPushButton("Marquer comme terminé", self.task_tab)

        button_style = (
            "background-color: #3498db; color: white; font-size: 14px; font-weight: bold; padding: 8px 16px; border-radius: 8px;"
        )
        self.add_task_button.setStyleSheet(button_style)
        self.delete_task_button.setStyleSheet(
            "background-color: #e74c3c; color: white; font-size: 14px; font-weight: bold; padding: 8px 16px; border-radius: 8px;"
        )
        self.complete_task_button.setStyleSheet(
            "background-color: #f39c12; color: white; font-size: 14px; font-weight: bold; padding: 8px 16px; border-radius: 8px;"
        )

        self.button_layout.addWidget(self.add_task_button)
        self.button_layout.addWidget(self.delete_task_button)
        self.button_layout.addWidget(self.complete_task_button)
        self.task_layout.addLayout(self.button_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        # Connexions
        self.add_project_button.clicked.connect(self.add_project)
        self.project_list_widget.currentRowChanged.connect(self.project_clicked)
        self.add_task_button.clicked.connect(self.add_task)
        self.delete_task_button.clicked.connect(self.delete_task)
        self.complete_task_button.clicked.connect(self.mark_completed)

        # Données internes
        self.projects = {}

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
