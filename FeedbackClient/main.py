import sys
from PyQt5.QtCore import QCoreApplication, QDate, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMainWindow, QDesktopWidget, QAction, qApp, \
    QDialog
from PyQt5.uic.properties import QtGui
from injector import Injector

from mainUI import MainUI


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self._injector = Injector()

        self.init_ui()
        self.init_main()

    def init_ui(self):
        exit_action = QAction("종료", self)
        exit_action.setStatusTip("프로그램을 종료합니다.")

        exit_action.triggered.connect(qApp.quit)

        self.statusBar()

        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        file_menu = menu_bar.addMenu("파일")

        file_menu.addAction(exit_action)

        self.setWindowTitle("Test Client")

    def init_main(self):
        self.mainUI = self._injector.get(MainUI)
        self.mainUI.c.request_close.connect(self.close)
        # self.mainUI.c.login_complete.connect(self.login_complete)
        self.setCentralWidget(self.mainUI)
        self.setGeometry(900, 900, 600, 600)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        self.move(qr.topLeft())

    def closeEvent(self, event):
        self.mainUI.release()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()

    try:
        app.exec_()
    except:
        print("exiting")
