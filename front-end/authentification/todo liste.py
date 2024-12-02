from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Configuration de la fenêtre principale
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Disposition verticale principale
        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout.setObjectName("layout")

        # Titre
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setText("Ma Todo Liste")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        self.layout.addWidget(self.title_label)

        # Tableau pour afficher les tâches
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Tâche", "Date", "Commentaire"])
        self.table.setStyleSheet("background-color: #ecf0f1; font-size: 14px;")
        self.layout.addWidget(self.table)

        # Zone d'entrée pour ajouter une nouvelle tâche
        self.form_layout = QtWidgets.QFormLayout()
        self.task_input = QtWidgets.QLineEdit(self.centralwidget)
        self.date_input = QtWidgets.QDateEdit(self.centralwidget)
        self.date_input.setCalendarPopup(True)
        self.comment_input = QtWidgets.QLineEdit(self.centralwidget)

        self.form_layout.addRow("Tâche :", self.task_input)
        self.form_layout.addRow("Date :", self.date_input)
        self.form_layout.addRow("Commentaire :", self.comment_input)
        self.layout.addLayout(self.form_layout)

        # Boutons pour les actions
        self.button_layout = QtWidgets.QHBoxLayout()
        self.add_button = QtWidgets.QPushButton("Ajouter", self.centralwidget)
        self.delete_button = QtWidgets.QPushButton("Supprimer", self.centralwidget)
        self.complete_button = QtWidgets.QPushButton("Marquer comme terminé", self.centralwidget)

        # Style des boutons
        self.add_button.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 10px;")
        self.delete_button.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold; padding: 10px;")
        self.complete_button.setStyleSheet("background-color: #f39c12; color: white; font-weight: bold; padding: 10px;")

        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.complete_button)
        self.layout.addLayout(self.button_layout)

        # Connexion des boutons aux actions
        self.add_button.clicked.connect(self.add_task)
        self.delete_button.clicked.connect(self.delete_task)
        self.complete_button.clicked.connect(self.mark_completed)

        # Finalisation
        MainWindow.setCentralWidget(self.centralwidget)

    def add_task(self):
        """Ajoute une nouvelle tâche à la liste."""
        task = self.task_input.text().strip()
        date = self.date_input.date().toString("dd/MM/yyyy")
        comment = self.comment_input.text().strip()

        if not task:
            QMessageBox.warning(None, "Erreur", "Veuillez entrer une tâche.")
            return

        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(task))
        self.table.setItem(row, 1, QTableWidgetItem(date))
        self.table.setItem(row, 2, QTableWidgetItem(comment))

        # Réinitialisation des champs
        self.task_input.clear()
        self.comment_input.clear()

    def delete_task(self):
        """Supprime la tâche sélectionnée."""
        rows = sorted(set(index.row() for index in self.table.selectedIndexes()), reverse=True)
        if not rows:
            QMessageBox.warning(None, "Erreur", "Veuillez sélectionner une tâche à supprimer.")
            return
        for row in rows:
            self.table.removeRow(row)

    def mark_completed(self):
        """Marque la tâche sélectionnée comme terminée."""
        rows = sorted(set(index.row() for index in self.table.selectedIndexes()), reverse=True)
        if not rows:
            QMessageBox.warning(None, "Erreur", "Veuillez sélectionner une tâche à marquer comme terminée.")
            return
        for row in rows:
            item = self.table.item(row, 0)
            font = item.font()
            font.setStrikeOut(True)  # Appliquer la barre sur le texte
            font.setBold(False)  # Optionnel : Rendre la police plus fine une fois terminée
            item.setFont(font)
            item.setForeground(
                QtGui.QColor(128, 128, 128))  # Changer la couleur du texte pour indiquer qu'elle est terminée
            item.setText(item.text() + " (Completed)")  # Ajouter "(Completed)" pour indiquer l'état en anglais

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Todo List")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
