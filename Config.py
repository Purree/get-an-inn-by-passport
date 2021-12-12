from configparser import ConfigParser

from inn_requests import get_auth_cookie


class Config:
    config = None

    def __init__(self):
        self.config = ConfigParser()
        self.config.read("config.ini")

        self.validate_properties()

    @property
    def get_config(self):
        return self.config

    def set_cookies(self):
        self.config['COOKIES'] = \
            {
                'upd_inn': get_auth_cookie()
            }

        self.write_data_to_file()

    def set_timeouts(self, timeout=0, interval=1):
        self.config['TIMEOUTS'] = \
            {
                'timeout': timeout,
                'interval': interval
            }

        self.write_data_to_file()

    def set_paths(self, inner_path=None, outer_path=None):
        if inner_path is None and self.is_property_exist('PATHS'):
            inner_path = self.config['PATHS']['innerpath']

        if outer_path is None and self.is_property_exist('PATHS'):
            outer_path = self.config['PATHS']['outerpath']

        self.config['PATHS'] = \
            {
                'innerPath': inner_path,
                'outerPath': outer_path + '\\completed.txt'
            }

        self.write_data_to_file()

    def set_proxies(self, proxy):
        self.config['PROXIES'] = \
            {
                'https': proxy
            }

        self.write_data_to_file()

    def write_data_to_file(self):
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

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
            self.set_paths('', '.')

        if not self.is_property_exist('PROXIES'):
            self.set_proxies('')

