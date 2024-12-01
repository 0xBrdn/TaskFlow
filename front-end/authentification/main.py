import sys
from PyQt5 import QtWidgets
from authentification import Ui_MainWindow  # Import the UI class from login_ui.py

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.main_window = MainWindow  # Passer la référence de la fenêtre principale à l'UI
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()