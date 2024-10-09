import sys
from PyQt6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
label = QLabel('Hello, PyQt!')
label.show()
sys.exit(app.exec())
