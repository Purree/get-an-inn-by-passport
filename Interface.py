from datetime import datetime
import traceback
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QFileDialog
from Config import Config
from Controller import Controller


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()

        uic.loadUi('window.ui', self)

        self.config = Config()
        self.config_cookies = self.config.get_config['COOKIES']
        self.config_timeouts = self.config.get_config['TIMEOUTS']
        self.config_paths = self.config.get_config['PATHS']
        self.config_proxy = self.config.get_config['PROXIES']
        self.load_data_from_config()

        self.StartButton.clicked.connect(self.start_button_pressed)
        self.stopButton.clicked.connect(self.stop_button_pressed)
        self.proxyFilePicker.clicked.connect(self.change_proxy_path)
        self.fileInputPicker.clicked.connect(self.change_input_path)
        self.fileOutputPicker.clicked.connect(self.change_output_path)
        self.activateTextOutput.clicked.connect(self.activate_text_output)
        self.deleteProxy.clicked.connect(self.delete_proxy)

        self.function_started = False

        self.Controller = Controller(self)

        self.show()

    def start_button_pressed(self):
        proxy = self.proxyInput.text()
        timeout = self.timeoutInput.value()
        interval = self.intervalInput.value()
        input_path = self.config_paths['innerpath']
        output_path = self.config_paths['outerpath']

        if input_path == '' or output_path == '':
            self.throw_error('Ошибка в заполненных данных')
            return False

        self.config.set_proxies(proxy)
        self.config.set_timeouts(timeout, interval)
        self.update_enabled_status(True)

        try:
            self.Controller.start()
        except Exception as error:
            self.Controller.write_data_to_file(
                '.\\crashlog.txt', 'a', f'\n_________________{datetime.now()}______________________\n '
                                        f'{str(traceback.format_exc())}')
            self.throw_error(f'{error}')
            self.append_text_output('Возникла ошибка, записана в лог\n')
            self.append_text_output(f'{error}')
            self.update_enabled_status(False)

    def delete_proxy(self):
        self.config.set_paths(proxy_path='')
        self.proxyText.setText(self.config_paths['proxypath'])

    def stop_button_pressed(self):
        self.append_text_output('Скрипт выключен\n_________________\n')
        self.update_enabled_status(False)

    def activate_text_output(self):
        self.textOutput.setEnabled(True)

    def update_enabled_status(self, status):
        scroll_bar = self.textOutput.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

        self.function_started = status

        self.stopButton.setEnabled(self.function_started)
        self.textOutput.setEnabled(self.function_started)
        self.proxyFilePicker.setEnabled(not self.function_started)
        self.intervalInput.setEnabled(not self.function_started)
        self.timeoutInput.setEnabled(not self.function_started)
        self.fileOutputPicker.setEnabled(not self.function_started)
        self.deleteProxy.setEnabled(not self.function_started)
        self.fileInputPicker.setEnabled(not self.function_started)
        self.StartButton.setEnabled(not self.function_started)

    def change_input_path(self):
        picked_data = QFileDialog.getOpenFileName(
            self, 'Выбери входной файл', self.config_paths['innerpath'], '*.txt'
        )

        if picked_data[0]:
            validated_data = picked_data[0].replace('/', '\\')
            print(f'{validated_data}')
            self.config.set_paths(inner_path=validated_data)
            self.inputPath.setText(self.shorten_string(self.config_paths['innerpath']))

    def change_output_path(self):
        picked_data = QFileDialog.getExistingDirectory(self, "Выберите папку",
                                                       self.config_paths['outerpath'][0:-14])

        if picked_data:
            validated_data = picked_data.replace('/', '\\')
            self.config.set_paths(outer_path=validated_data)
            self.outputPath.setText(self.shorten_string(self.config_paths['outerpath'][0:-14]))

    def change_proxy_path(self):
        picked_data = QFileDialog.getOpenFileName(self, "Выберите папку", self.config_paths['proxypath'], '*.txt')

        if picked_data[0]:
            validated_data = picked_data[0].replace('/', '\\')
            self.config.set_paths(proxy_path=validated_data)
            self.proxyText.setText(self.config_paths['proxypath'])

    def update_current_line(self, line):
        self.textProgress.setText(
            f'{line}/{self.textProgress.text().split("/")[1]}'
        )

    def update_line_count(self, line):
        self.textProgress.setText(
            f'{self.textProgress.text().split("/")[0]}/{line}'
        )

    def update_current_proxy(self, proxy):
        self.currentProxy.setText(f'Прокси: {proxy}')

    def quit_thread(self):
        self.Controller.Logic.quit()

    def load_data_from_config(self):
        self.proxyInput.setText(self.config.get_config['PROXIES']['https'])

        self.timeoutInput.setValue(float(self.config_timeouts['timeout']))
        self.intervalInput.setValue(float(self.config_timeouts['interval']))

        self.inputPath.setText(self.shorten_string(self.config_paths['innerpath']))
        self.outputPath.setText(self.shorten_string(self.config_paths['outerpath'][0:-14]))
        self.proxyText.setText(self.config_paths['proxypath'])

    def throw_error(self, error_text):
        self.errorText.setText(error_text)

    def shorten_string(self, string):
        return string[0:3] + '...' + string[-18:] if len(string) > 24 else string

    def append_text_output(self, text):
        scroll_bar = self.textOutput.verticalScrollBar()
        scroll_bar_position = 0
        if scroll_bar.value() >= scroll_bar.maximum() - 4:
            scroll_bar_position = -1
        else:
            scroll_bar_position = scroll_bar.value()

        self.textOutput.setText(self.textOutput.toPlainText() + text + '\n')
        scroll_bar.setValue(scroll_bar_position if scroll_bar_position != -1 else scroll_bar.maximum())
