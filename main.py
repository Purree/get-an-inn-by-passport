import time
import json
import requests as requests
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

userdata = []
with open('data.json', encoding='utf-8') as json_file:
    userdata = json.load(json_file)


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


try:
    config['COOKIES']
except KeyError:
    update_cookies()

config_cookies = config['COOKIES']


def send_request(data, cookies, timeout=0, request_id=''):
    time.sleep(timeout)

    request = requests.post('https://service.nalog.ru/inn-new-proc.do',
                            data=data,
                            cookies=cookies
                            )
    request_id = request.json()['requestId'] if not request_id else request_id

    print(request.json())
    return request.json()['inn'] if 'inn' in request.json() else send_request({
        'c': 'get',
        'requestId': request_id
    }, cookies, timeout + 1, request_id)


if __name__ == '__main__':
    print(send_request(userdata, config_cookies))
