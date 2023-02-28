import sys

from PyQt6 import uic, QtCore, QtGui, QtWidgets
import datetime
import requests
from requests.exceptions import HTTPError
import json


class MainWindow(QtWidgets.QMainWindow):
    ServerAddress = "http://localhost:5000"
    MessageID = 0

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('messenger.ui', self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
