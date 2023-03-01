import sys

from PyQt6 import uic, QtCore, QtWidgets
import datetime
import requests
from requests.exceptions import HTTPError
import json


class MainWindow(QtWidgets.QMainWindow):
    ServerAddress = "http://localhost:5000"
    MessageID = 0

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # uploading ui file
        uic.loadUi('messenger.ui', self)
        # button pushing logic
        self.sendButton.clicked.connect(self.sendButton_clicked)

    def sendButton_clicked(self):
        self.SendMessage()

    def SendMessage(self):
        UserName = self.nameLine.text()
        MessageText = self.messageLine.text()
        TimeStamp = str(datetime.datetime.today())
        msg = f"{{\"UserName\": \"{UserName}\", \"MessageText\": \"{MessageText}\", \"TimeStamp\": \"{TimeStamp}\"}}"

        print("Отправлено сообщение: " + msg)
        url = self.ServerAddress + "/api/PyMessenger"
        data = json.loads(msg)
        r = requests.post(url, json=data)
        # clearing the inputs
        self.nameLine.clear()
        self.messageLine.clear()

    def GetMessage(self, id):
        id = str(id)
        url = self.ServerAddress + "/api/PyMessenger/" + id

        try:
            response = requests.get(url)
            response.raise_for_status()
        except HTTPError as http_err:
            #print(f'HTTP error occurred: {http_err}')
            return None
        except Exception as err:
            #print(f'An error occurred: {err}')
            return None
        else:
            text = response.text
            return text

    def timerEvent(self):
        msg = self.GetMessage(self.MessageID)
        while msg is not None:
            msg = json.loads(msg)
            UserName = msg["UserName"]
            MessageText = msg["MessageText"]
            TimeStamp = msg["TimeStamp"]
            msgtext = f"{TimeStamp} : <{UserName}> : {MessageText}"
            print(msgtext)
            self.messageList.insertItem(self.MessageID, msgtext)
            self.MessageID += 1
            msg = self.GetMessage(self.MessageID)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    timer = QtCore.QTimer()
    timer.timeout.connect(w.timerEvent)
    timer.start(5000)
    sys.exit(app.exec())
