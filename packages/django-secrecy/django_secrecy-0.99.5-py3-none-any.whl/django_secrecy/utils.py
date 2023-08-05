import os
import json
import logging


logger = logging.getLogger('setup_log')

COLORS = {
    'white': '\033[0m',
    'red': '\033[31m',
    'green': '\033[32m',
    'orange': '\033[33m',
    'yellow': '\033[93m',
    'blue': '\033[34m',
    'purple': '\033[35m',
}

class Secrets:
    '''Get secrets params from "secrets.json" file
       generated with "generator <PROJ_NAME>"
    '''
    def __init__(self, SETTINGS_DIR, *args, **kwargs):
        self.SETTINGS_DIR = SETTINGS_DIR
        self.__dict__.update(self._get_secrets())

    def __getattr__(self, attr):
        logger.warning(f'Secret param {attr} not found!')
        return None

    def _get_secrets(self):
        SECRET_FILE = os.path.join(self.SETTINGS_DIR, 'secrets.json')
        try:
            with open(SECRET_FILE, 'r') as file:
                SECRETS = json.load(file)
        except FileNotFoundError:
            logger.warning('File not found! "generator <PROJ_NAME>" first please!')
            SECRETS = {}
        return SECRETS

# backwards compatibility
get_secrets = Secrets
