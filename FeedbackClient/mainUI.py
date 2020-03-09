import requests
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QVBoxLayout, QMessageBox, \
    QTextEdit, QPlainTextEdit
from injector import inject

from IOClient import IOClient


class MainUIComm(QObject):
    request_close = pyqtSignal()
    login_complete = pyqtSignal()


class MainUI(QWidget):
    @inject
    def __init__(self, io_client: IOClient):
        super().__init__()

        self.connected = False
        self.io_client = io_client
        io_client.events.connect += self.ios_connect
        io_client.events.message += self.on_message

        self.c = MainUIComm()

        grid = QGridLayout()

        grid.addWidget(QLabel("URL:"), 0, 0)
        grid.addWidget(QLabel("토스URL:"), 1, 0)

        self.txt_url = QLineEdit()

        self.txt_url.setPlaceholderText("접속할 WebSocket 주소를 입력해주세요")
        self.txt_url.setText("ws://223.130.82.55:7777")

        grid.addWidget(self.txt_url, 0, 1)

        self.txt_toss = QLineEdit()

        self.txt_toss.setPlaceholderText("토스할 주소를 입력해주세요")
        self.txt_toss.setText("http://localhost:9002/feedback/jtnet/t2")

        self.txt_content = QPlainTextEdit()

        self.txt_content.setPlainText("")
        self.txt_content.setTextCursor(QTextCursor())

        grid.addWidget(self.txt_toss, 1, 1)
        grid.addWidget(self.txt_content, 2, 1)

        btn_container = QHBoxLayout()

        close_btn = QPushButton(text="닫기")
        close_btn.clicked.connect(lambda: self.c.request_close.emit())

        self.connect_btn = QPushButton(text="접속")
        self.connect_btn.clicked.connect(self.connect_work)

        btn_container.addWidget(self.connect_btn)
        btn_container.addWidget(close_btn)

        layout = QVBoxLayout()
        layout.addLayout(grid)
        layout.addLayout(btn_container)

        self.setLayout(layout)

    def ios_connect(self):
        #self._ioClient.init_member(self._authSv.get_login_id())
        self.connected = True
        self.txt_content.appendPlainText("접속되었습니다.")
        self.update_connect_btn()

    def on_message(self, message):
        self.txt_content.appendPlainText("메시지 수신 : " + str(message))

        self.toss_url(message)

    def toss_url(self, message):
        if len(self.txt_toss.text().strip()) > 0:
            self.txt_content.appendPlainText("토스 시작")
            r = requests.post(self.txt_toss.text(), data=message)
            self.txt_content.appendPlainText("토스 완료 : " + str(r.status_code))
            self.txt_content.appendPlainText("토스 응답 : " + r.text)

    def release(self):
        self.io_client.disconnect()

    def update_connect_btn(self):
        if self.connected:
            self.connect_btn.setText("접속 해제")
        else:
            self.connect_btn.setText("접속")

    # 로그인 작업을 진행한다.
    def connect_work(self):

        if not self.connected:
            if len(self.txt_url.text()) == 0:
                QMessageBox.warning(self, "알림", "주소를 입력해주세요")
                return

            self.io_client.connect(self.txt_url.text())
        else:
            self.io_client.disconnect()
            self.connected = False
            self.txt_content.appendPlainText("해제 되었습니다.")
            self.update_connect_btn()
