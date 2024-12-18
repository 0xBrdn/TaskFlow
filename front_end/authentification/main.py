import sys
import os
import threading
from PyQt5 import QtWidgets

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)

from authentification import Ui_MainWindow

from api.api_google import app as flask_app

def run_flask():
    """
    Fonction pour démarrer le serveur Flask dans un thread séparé.
    """
    flask_app.run(port=5000, use_reloader=False)

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.main_window = MainWindow
    MainWindow.show()
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()