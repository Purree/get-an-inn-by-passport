from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QFileDialog
from Config import Config


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()

        uic.loadUi('window.ui', self)

        self.config = Config()
        self.load_data_from_config()
        self.StartButton.clicked.connect(self.start_button_pressed)
        self.stopButton.clicked.connect(self.stop_button_pressed)
        self.fileInputPicker.clicked.connect(self.change_input_path)
        self.fileOutputPicker.clicked.connect(self.change_output_path)

        self.show()

    def start_button_pressed(self):
        proxy = self.proxyInput.text()
        timeout = self.timeoutInput.value()
        interval = self.intervalInput.value()
        input_path = self.config.get_config['PATHS']['innerpath']
        output_path = self.config.get_config['PATHS']['outerpath']

        if input_path == '' or output_path == '':
            self.throw_error('Ошибка в заполненных данных')
            return False

        self.config.set_proxies(proxy)
        self.config.set_timeouts(timeout, interval)
        self.update_enabled_status(True)

    def stop_button_pressed(self):
        self.append_text_output('Скрипт выключен\n_________________\n')
        self.update_enabled_status(False)

    def update_enabled_status(self, status):
        self.stopButton.setEnabled(status)
        self.textOutput.setEnabled(status)
        self.StartButton.setEnabled(not status)

    def change_input_path(self):
        picked_data = QFileDialog.getOpenFileName(
            self, 'Выбери входной файл', self.config.get_config['PATHS']['innerpath'], '*.txt'
        )

        if picked_data[0]:
            validated_data = picked_data[0].replace('/', '\\')
            self.config.set_paths(validated_data)
            self.inputPath.setText(self.shorten_string(self.config.get_config['PATHS']['innerpath']))

    def change_output_path(self):
        picked_data = QFileDialog.getExistingDirectory(self, "Выберите папку",
                                                       self.config.get_config['PATHS']['outerpath'])

        if picked_data:
            validated_data = picked_data.replace('/', '\\')
            self.config.set_paths(outer_path=validated_data)
            self.outputPath.setText(self.shorten_string(self.config.get_config['PATHS']['outerpath'][0:-14]))

    def load_data_from_config(self):
        self.proxyInput.setText(self.config.get_config['PROXIES']['https'])

        self.timeoutInput.setValue(float(self.config.get_config['TIMEOUTS']['timeout']))
        self.intervalInput.setValue(float(self.config.get_config['TIMEOUTS']['interval']))

        self.inputPath.setText(self.shorten_string(self.config.get_config['PATHS']['innerpath']))
        self.outputPath.setText(self.shorten_string(self.config.get_config['PATHS']['outerpath'][0:-14]))

    def throw_error(self, error_text):
        self.errorText.setText(error_text)

    def shorten_string(self, string):
        return string[0:3] + '...' + string[-18:] if len(string) > 24 else string

    def append_text_output(self, text):
        self.textOutput.setText(self.textOutput.toPlainText() + text + '\n')
