import time
import requests as requests


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


def send_request(request_data, cookies, timeout=0, interval=1, request_id='', proxies=None,
                 print_function=lambda data: print(data)):
    """
    Recursive function that get requestId from nalog.ru and after it get inn of user

    :param request_data: Dictionary Required
    :param cookies: Required because site wasn't work without upd_inn cookie
    :param timeout: Integer Optional
    :param interval: Integer Optional
    :param request_id: Integer|String Optional
    :param proxies: Dictionary|None Optional
    :param print_function: Function Optional Logs output function. For default - print in console
    :return: String User inn
    """

    if proxies is None:
        proxies = {}

    time.sleep(timeout)

    request = requests.post('https://service.nalog.ru/inn-new-proc.do',
                            data=request_data,
                            cookies=cookies,
                            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                                                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 '
                                                   'Safari/537.36'},
                            proxies=proxies
                            )

    print_function(f'{request.json()}')
    request_id = request.json()['requestId'] if not request_id else request_id

    if 'error_code' in request.json():
        return 'Информация не найдена' if request.json()['error_code'] == 1.0 \
            else 'Ошибка на стороне сайта, код ошибки: ' + str(request.json()['error_code'])

    return request.json()['inn'] if 'inn' in request.json() else send_request({
        'c': 'get',
        'requestId': request_id
    }, cookies, timeout + interval, interval, request_id, proxies, print_function)
