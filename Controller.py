import os.path
import traceback
from datetime import datetime

from PyQt6.QtCore import QThread
import PyQt6.QtCore as QtCore


from inn_requests import send_request, get_random_proxy_from_file


class Controller:
    def __init__(self, interface_instance):
        """
        Class that manipulate thread with logic.

        :param interface_instance: Object Required Instance of Interface class
        """
        self.Ui = interface_instance

        self.config_cookies = self.Ui.config_cookies
        self.config_timeouts = self.Ui.config_timeouts
        self.config_paths = self.Ui.config_paths
        self.config_proxy = self.Ui.config_proxy

        self.Logic = Logic(self.Ui, self.config_cookies, self.config_timeouts,
                           self.config_paths, self.config_proxy, self.parse_document, self.write_data_to_file)

        self.Logic.append_text_output.connect(self.Ui.append_text_output)
        self.Logic.update_enabled_status.connect(self.Ui.update_enabled_status)
        self.Logic.update_lines_count.connect(self.Ui.update_line_count)
        self.Logic.update_line_index.connect(self.Ui.update_current_line)
        self.Logic.update_proxy.connect(self.Ui.update_current_proxy)
        self.Logic.throw_error.connect(self.Ui.throw_error)

    def parse_document(self, path):
        """
        Transform every line in document what looks like surname|name|patronymic(Optional)|year-month-day|passport to
        object with all this data and push it to array

        :param path: String Path to document with data
        :return: Array Ready to request data
        """
        data_from_document = open(path, 'r', encoding='utf-8').readlines()
        reformatted_data = []
        for line in data_from_document:
            line = line.replace("\n", "").split('|')
            if len(line) < 4 or len(line) > 5:
                continue

            if '-' in line[2]:
                fam, nam, bdate, docno = line
            else:
                fam, nam, otch, bdate, docno = line

            bdate = ".".join(list(reversed(bdate.split('-'))))
            docno = f'{docno[0:2]} {docno[2:4]} {docno[4::]}'
            reformatted_data.append([line, {
                'c': 'find',
                'fam': fam,
                'nam': nam,
                'opt_otch': 1,
                'doctype': 21,
                'docno': docno,
                'bdate': bdate
            }])

        return reformatted_data

    def write_data_to_file(self, path, method, text):
        with open(path, method, encoding='utf-8') as output:
            output.write(text)

    def start(self):
        self.Logic.start()


class Logic(QtCore.QThread):
    append_text_output = QtCore.pyqtSignal(object)
    update_enabled_status = QtCore.pyqtSignal(object)
    update_lines_count = QtCore.pyqtSignal(object)
    update_line_index = QtCore.pyqtSignal(object)
    update_proxy = QtCore.pyqtSignal(object)
    throw_error = QtCore.pyqtSignal(object)

    def __init__(self, interface_instance, cookies, timeouts, paths, proxy, parse_document, write_data_to_file):
        """
        Logic that in a separate thread

        :param interface_instance:
        :param cookies:
        :param timeouts:
        :param paths:
        :param proxy:
        :param parse_document:
        :param write_data_to_file:
        """
        QThread.__init__(self)
        self.NonThreadUi = interface_instance

        self.config_cookies = cookies
        self.config_timeouts = timeouts
        self.config_paths = paths
        self.config_proxy = proxy
        self.parse_document = parse_document
        self.write_data_to_file = write_data_to_file

    def __del__(self):
        self.wait()

    def run(self):
        data_for_requests = self.parse_document(self.config_paths['innerPath'])

        # # If file already exist append divider
        # if os.path.isfile(self.config_paths['outerPath']):
        #     self.write_data_to_file(self.config_paths['outerPath'], 'a',
        #                             f'\n_________________{datetime.now()}______________________\n')

        self.update_lines_count.emit(f'{len(data_for_requests)}')

        for index, (data_array, data_object) in enumerate(data_for_requests):
            if not self.NonThreadUi.function_started:
                break
            self.update_line_index.emit(f'{index+1}')

            proxy = get_random_proxy_from_file(self.config_paths['proxypath'])

            if proxy == '':
                self.throw_error.emit('Вы не используете прокси')
            else:
                self.throw_error.emit('')

            self.update_proxy.emit(proxy)

            try:
                received_data = send_request(
                    data_object,
                    self.config_cookies,
                    float(self.config_timeouts["timeout"]),
                    float(self.config_timeouts["interval"]),
                    proxy=proxy,
                    print_function=self.append_text_output.emit
                )

            except Exception as error:
                self.write_data_to_file(
                    '.\\crashlog.txt', 'a', f'\n_________________{datetime.now()}______________________\n '
                                            f'{str(traceback.format_exc())}')
                if str(error) == 'Missing dependencies for SOCKS support.':
                    self.append_text_output.emit('Отсутствует поддержка SOCKS прокси. Ошибка была записана в crashlog')
                    self.update_enabled_status.emit(False)
                    break

                self.append_text_output.emit(
                    'Ошибка со стороны сервера, возможно, нерабочий прокси. Ошибка была записана в crashlog')
                self.update_enabled_status.emit(False)
                break

            self.write_data_to_file(self.config_paths['outerPath'], 'a', f'{"|".join(data_array)}|{received_data}\n')

        self.update_enabled_status.emit(False)
        self.NonThreadUi.quit_thread()
