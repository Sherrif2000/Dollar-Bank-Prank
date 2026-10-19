
import sys

from PySide6.QtWidgets import QApplication

from forgecode.main_window import MainWindow
from forgecode.theme import APP_STYLESHEET


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("ForgeCode")
    app.setOrganizationName("ForgeCode")
    app.setStyle("Fusion")
    app.setStyleSheet(APP_STYLESHEET)

    window = MainWindow()
    window.show()

    return app.exec()

