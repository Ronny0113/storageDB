from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()

    window.setWindowTitle("Anal Sex")
    window.setGeometry(300, 250, 1000, 800)

    text = QtWidgets.QLabel(window)
    text.setText("Долбиться в жопу это круто!")
    text.move(100, 100)
    text.adjustSize()

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()