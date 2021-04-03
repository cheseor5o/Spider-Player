from view import windowOS

import sys
from PyQt5.QtWidgets import *

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        mainWindow = windowOS.Main_Window()
        mainWindow.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
