import sys
from mainWin import MyMainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywin = MyMainWindow()
    mywin.show()
    # mywin.showMaximized()
    sys.exit(app.exec_())
