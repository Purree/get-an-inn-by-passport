from PyQt6 import QtWidgets
import sys

from Config import Config
from Interface import Ui


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    config = Config().get_config
    window = Ui()
    app.exec()
