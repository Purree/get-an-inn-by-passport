import os
import time
import requests as requests
import random


def get_auth_cookie():
    """
    :return: String
    """
    cookie = requests.post('https://service.nalog.ru/static/personal-data-proc.json', data={
        'from': '/inn.do',
        'svc': 'inn',
        'personalData': '1'
    })

    return cookie.text


def get_random_proxy_from_file(path, iteration=0):
    """
    :param path: String Required Path to file with proxies
    :param iteration: String Optional Iteration of script (max=20)
    :return:
    """
    if iteration == 20:
        return ''

    if not os.path.exists(path):
        raise Exception('Путь не существует')

    proxy_line = random.choice(open(path, encoding='utf-8').readlines())  # get random line of document
    proxy_list = proxy_line.replace('\n', '').split(':')

    if len(proxy_list) == 4:
        proxy_line = f'{proxy_list[2]}:{proxy_list[3]}@{proxy_list[0]}:{proxy_list[1]}'
    elif len(proxy_list) == 2:
        proxy_line = f'{proxy_list[0]}:{proxy_list[1]}'
    else:
        return get_random_proxy_from_file(path, iteration + 1)

    return 'socks5://' + proxy_line


def send_request(request_data, cookies, timeout=0, interval=1, request_id='', proxy=None,
                 print_function=lambda data: print(data)):
    """
    Recursive function that get requestId from nalog.ru and after it get inn of user

    :param request_data: Dictionary Required
    :param cookies: Required because site wasn't work without upd_inn cookie
    :param timeout: Integer Optional
    :param interval: Integer Optional
    :param request_id: Integer|String Optional
    :param proxy: String|None Optional Socs5 proxy
    :param print_function: Function Optional Logs output function. For default - print in console
    :return: String User inn
    """

    active_proxy = {} if proxy is None else {'https': proxy}

    time.sleep(timeout)

    request = requests.post('https://service.nalog.ru/inn-new-proc.do',
                            data=request_data,
                            cookies=cookies,
                            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                                                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 '
                                                   'Safari/537.36'},
                            proxies=active_proxy
                            )

    print_function(f'{request.json()}')
    request_id = request.json()['requestId'] if not request_id else request_id

    if 'error_code' in request.json():
        return 'Информация не найдена' if request.json()['error_code'] == 1.0 \
            else 'Ошибка на стороне сайта, код ошибки: ' + str(request.json()['error_code'])

    return request.json()['inn'] if 'inn' in request.json() else send_request({
        'c': 'get',
        'requestId': request_id
    }, cookies, timeout + interval, interval, request_id, proxy, print_function)
