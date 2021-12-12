from PyQt6 import QtWidgets
import sys

from Config import Config
from Interface import Ui

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    config = Config().get_config
    window = Ui()
    app.exec()
