import sys
import os
import subprocess
import threading
from PyQt5 import QtWidgets, QtGui, QtCore

MAIN_SCRIPT = "main.py"      # Script à lancer
RUBIS_IMAGE = "rubis.png"    # Image du rubis

class SylasUI(QtWidgets.QWidget):
    output_signal = QtCore.pyqtSignal(str)  # Signal pour l'affichage thread-safe

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SYLAS - Interface")
        self.setGeometry(200, 150, 900, 600)
        self.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")

        # Layout principal
        main_layout = QtWidgets.QHBoxLayout(self)

        # Zone de texte (affichage)
        self.output_area = QtWidgets.QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setFont(QtGui.QFont("Consolas", 10))
        self.output_area.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                border: none;
                color: #e0e0e0;
                padding: 8px;
            }
        """)

        # Colonne gauche : Affichage + Entrée
        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(self.output_area)

        # Champ de saisie utilisateur
        input_layout = QtWidgets.QHBoxLayout()
        self.input_field = QtWidgets.QLineEdit()
        self.input_field.setFont(QtGui.QFont("Consolas", 10))
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #3c3c3c;
                border: 1px solid #555;
                color: #ffffff;
                padding: 6px;
            }
        """)
        self.input_field.returnPressed.connect(self.send_input)

        # Bouton envoyer
        self.send_button = QtWidgets.QPushButton("Envoyer")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #8b0000;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #a00000;
            }
        """)
        self.send_button.clicked.connect(self.send_input)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        left_layout.addLayout(input_layout)

        # Rubis à droite
        rubis_label = QtWidgets.QLabel()
        if os.path.exists(RUBIS_IMAGE):
            pixmap = QtGui.QPixmap(RUBIS_IMAGE)
            rubis_label.setPixmap(pixmap.scaled(250, 250, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        else:
            rubis_label.setText("[Rubis manquant]")
            rubis_label.setAlignment(QtCore.Qt.AlignCenter)
            rubis_label.setStyleSheet("color: #ff4444; font-size: 14px;")

        # Ajout dans layout principal
        main_layout.addLayout(left_layout, 3)
        main_layout.addWidget(rubis_label, 1)

        # Signal pour thread -> UI
        self.output_signal.connect(self.append_output)

        # Lancement de main.py
        self.process = subprocess.Popen(
            [sys.executable, MAIN_SCRIPT],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True,
            encoding="utf-8",
            errors="replace"
        )

        # Thread lecture
        threading.Thread(target=self.read_output, daemon=True).start()

    def read_output(self):
        """Lit la sortie de main.py en continu"""
        for line in self.process.stdout:
            self.output_signal.emit(line)

    def append_output(self, text):
        """Ajoute du texte à l'affichage"""
        self.output_area.moveCursor(QtGui.QTextCursor.End)
        self.output_area.insertPlainText(text)
        self.output_area.moveCursor(QtGui.QTextCursor.End)

    def send_input(self):
        """Envoie le texte à main.py"""
        text = self.input_field.text()
        if text.strip():
            try:
                self.process.stdin.write(text + "\n")
                self.process.stdin.flush()
            except Exception as e:
                self.output_signal.emit(f"\n[ERREUR envoi] {e}\n")
        self.input_field.clear()

def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = SylasUI()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
