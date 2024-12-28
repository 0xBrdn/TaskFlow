import sys
import os
import threading
from queue import Queue
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)

from authentification import Ui_MainWindow
from api.api_google import app as flask_app

message_queue = Queue()

queue_lock = threading.Lock()

def run_flask():
    flask_app.config["message_queue"] = message_queue
    flask_app.config["queue_lock"] = queue_lock
    print("[Flask] Serveur démarré sur le port 5001.")
    flask_app.run(port=5001, use_reloader=False)

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.main_window = MainWindow
    MainWindow.show()

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    def check_queue():
        try:
            with queue_lock:
                while not message_queue.empty():
                    message = message_queue.get()
                    print(f"[PyQt] Message récupéré : {message}")

                    if not isinstance(message, dict):
                        print(f"[PyQt] Message invalide dans la file : {message}")
                        continue

                    message_type = message.get("type")
                    if message_type == "google_login_success":
                        user_data = message.get("data")
                        print(f"[PyQt] Données utilisateur reçues : {user_data}")
                        if isinstance(user_data, dict):
                            ui.connect_google_user(user_data)
                        else:
                            print(f"[PyQt] Données utilisateur invalides : {user_data}")
                    else:
                        print(f"[PyQt] Type de message inconnu : {message_type}")
        except Exception as e:
            print(f"[PyQt] Erreur lors de la lecture de la file : {e}")

    timer = QTimer()
    timer.timeout.connect(check_queue)
    timer.start(100)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()