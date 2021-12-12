import os.path
from datetime import datetime
from PyQt6 import QtWidgets, uic
import sys
from PyQt6.QtWidgets import QFileDialog

from Config import Config
from Interface import Ui
from inn_requests import send_request


def parse_document(path):
    data_from_document = open(path, 'r', encoding='utf-8').readlines()
    reformatted_data = []
    for line in data_from_document:
        line = line.replace("\n", "").split('|')
        if len(line) < 4:
            continue

        if '-' in line[2]:
            fam, nam, bdate, docno = line
        else:
            fam, nam, otch, bdate, docno = line

        bdate = ".".join(list(reversed(bdate.split('-'))))
        docno = docno[0:2] + ' ' + docno[2:4] + ' ' + docno[4::]
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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    config = Config().get_config
    window = Ui()
    app.exec()

    # config_cookies = config['COOKIES']
    # config_timeouts = config['TIMEOUTS']
    # config_paths = config['PATHS']
    # config_proxy = config['PROXIES']
    #
    # data_for_requests = parse_document(config_paths['innerPath'])
    #
    # if os.path.isfile(config_paths['outerPath']):
    #     with open(config_paths['outerPath'], 'a', encoding='utf-8') as completed_data:
    #         completed_data.write(f'\n_________________{datetime.now()}______________________\n')
    #
    # for data in data_for_requests:
    #     print(data)
    #
    #     try:
    #         received_data = send_request(
    #             data[1],
    #             config_cookies,
    #             float(config_timeouts["timeout"]),
    #             float(config_timeouts["interval"]),
    #             proxies=dict(config["PROXIES"])
    #         )
    #
    #     except Exception as error:
    #         if error == 'Missing dependencies for SOCKS support.':
    #             exit('Отсутствует поддержка SOCKS прокси')
    #
    #         with open('.\\crashlog.txt', 'a', encoding='utf-8') as crash_log:
    #             crash_log.write(f'\n_________________{datetime.now()}______________________\n')
    #             crash_log.write(str(error))
    #
    #         exit('Ошибка со стороны сервера, возможно, нерабочий прокси. Ошибка была записана в crashlog')
    #
    #     with open(config_paths['outerPath'], 'a', encoding='utf-8') as completed_data:
    #         completed_data.write(
    #             f'{"|".join(data[0])}|'
    #             f'{received_data}'
    #             f'\n'
    #         )
    # TODO: Associate start button and logic, replace print with Ui.append_text_output
