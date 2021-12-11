import time
import json
import requests as requests
from configparser import ConfigParser


def get_auth_cookie():
    cookie = requests.post('https://service.nalog.ru/static/personal-data-proc.json', data={
        'from': '/inn.do',
        'svc': 'inn',
        'personalData': '1'
    })

    return cookie.text


def update_cookies():
    config['COOKIES'] = \
        {
            'upd_inn': get_auth_cookie()
        }

    with open('config.ini', 'w') as conf:
        config.write(conf)


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
        reformatted_data.append({
            'c': 'find',
            'fam': fam,
            'nam': nam,
            'opt_otch': 1,
            'doctype': 21,
            'docno': docno,
            'bdate': bdate
        })

    return reformatted_data


def send_request(data, cookies, timeout=0, request_id=''):
    time.sleep(timeout)

    request = requests.post('https://service.nalog.ru/inn-new-proc.do',
                            data=data,
                            cookies=cookies
                            )

    print(request.json())
    request_id = request.json()['requestId'] if not request_id else request_id

    return request.json()['inn'] if 'inn' in request.json() else send_request({
        'c': 'get',
        'requestId': request_id
    }, cookies, timeout + 1, request_id)


if __name__ == '__main__':
    data_for_requests = parse_document("C:\\Users\\asus\\Downloads\\1000.txt")
    config = ConfigParser()
    config.read("config.ini")

    try:
        config['COOKIES']
    except KeyError:
        update_cookies()

    config_cookies = config['COOKIES']

    for data in data_for_requests:
        print(data)
        print(send_request(data, config_cookies))
