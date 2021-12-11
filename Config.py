from configparser import ConfigParser

from inn_requests import get_auth_cookie


class Config:
    config = None

    def __init__(self):
        config = ConfigParser()
        self.config = config
        config.read("config.ini")

        self.validate_properties()

    @property
    def get_config(self):
        return self.config

    def set_cookies(self):
        self.config['COOKIES'] = \
            {
                'upd_inn': get_auth_cookie()
            }

        with open('config.ini', 'w') as conf:
            self.config.write(conf)

    def set_timeouts(self, timeout=0, interval=1):
        self.config['TIMEOUTS'] = \
            {
                'timeout': timeout,
                'interval': interval
            }

    def set_paths(self, inner_path, outer_path='.\\'):
        self.config['PATHS'] = \
            {
                'innerPath': inner_path,
                'outerPath': outer_path + 'completed.txt'
            }

    def set_proxies(self, proxy):
        self.config['PROXIES'] = \
            {
                'https': proxy
            }

    def is_property_exist(self, property_name):
        """
        Check is property exist

        :param property_name: Name of property what you want to check
        :return: boolean
        """

        try:
            self.config[property_name]
        except KeyError:
            return False

        return True

    def validate_properties(self):
        """
        Check is properties exist, set default values in it if not

        :return: None
        """
        if not self.is_property_exist('COOKIES'):
            self.set_cookies()

        if not self.is_property_exist('TIMEOUTS'):
            self.set_timeouts(0, 1)

        if not self.is_property_exist('PATHS'):
            self.set_paths('C:\\Users\\asus\\Downloads\\1000.txt')

        if not self.is_property_exist('PROXIES'):
            self.set_proxies('')

