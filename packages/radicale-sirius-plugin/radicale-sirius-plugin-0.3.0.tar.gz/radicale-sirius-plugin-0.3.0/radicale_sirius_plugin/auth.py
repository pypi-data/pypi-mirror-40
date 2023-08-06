from radicale.auth import BaseAuth
import requests
import time
from threading import Lock


class CacheEntry:
    '''Cache structure for login procedure

    '''

    def __init__(self, valid, token, username, expiration):
        '''
        :param valid: True if login was successfull
        :type valid: bool
        :param token: Sirius local token
        :type token: str
        :param username: School username
        :type username: str
        :param expiration: expiration date in unix timestamp
        :type expiration: int
        '''

        self.valid = valid
        self.token = token
        self.username = username
        self.expiration = expiration

    def expired(self):
        '''Check if entry is expired

        :return: True of expired
        :rtype: bool
        '''

        return self.expiration < time.time()


class Auth(BaseAuth):
    def __init__(self, configuration, logger):
        '''Auth configuration

        :param configuration: Application configuration 
        :param logger: Application logger object
        '''

        super().__init__(configuration, logger)
        self.cache = {}
        self.load_config()
        self.lock = Lock()

    def load_config(self):
        '''Load configuration data

        :raises ValueError: Raise if configuration file is not valid
        '''

        self.cache_expire = 180
        if self.configuration.has_option("auth", "cache_expire"):
            try:
                value = int(self.configuration.get("auth", "cache_expire"))
            except:
                raise ValueError("'cache_expire' is not number")
            self.cache_expire = max(self.cache_expire, value)
        self.logger.info("Configuration 'cache_expire' is %r",
                         self.cache_expire)

    def login_using_sirius(self, username, token):
        '''Check if Sirius api accept username and token

        :param username: School username
        :type username: str
        :param token: Sirius local token
        :type token: str
        :return: True if success
        :rtype: bool
        '''

        if '/' in username:
            return False
        resp = requests.get(url='https://sirius.fit.cvut.cz/api/v1/people/' +
                            username, params=dict(access_token=token))
        return resp.status_code == 200

    def is_authenticated_cached(self, username, token):
        '''Check user validity and cache result

        :param username: School username
        :type username: str
        :param token: Sirius local token
        :type token: str
        :return: True
        :rtype: bool
        '''

        with self.lock:
            if username in self.cache:
                entry = self.cache[username]
                if entry.expired():
                    self.cache[username] = None
                else:
                    return entry.valid

            valid = self.login_using_sirius(username, token)
            expired = time.time()
            if valid:
                expired = expired + 1800
            self.cache[username] = CacheEntry(valid, token, username, expired)
            return valid

    def is_authenticated2(self, login, user, password):
        '''Authenticate user against Sirius API

        :param login: login name in form "{school_username}|{sirius_token}"
        :type login: [type]
        :param user: the user from ``map_login_to_user(login)``.
        :type user: string
        :param password: anything
        :type password: any
        :return: True if success
        :rtype: bool
        '''

        # Username and token are needed for SIRIUS API access, by default only username is saved
        data = login.split('|', 1)
        if len(data) != 2:
            return False
        return self.is_authenticated_cached(data[0], data[1])
