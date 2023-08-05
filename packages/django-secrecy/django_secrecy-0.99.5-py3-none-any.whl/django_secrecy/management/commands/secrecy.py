import os
import base64
import json
import getpass
import secrets

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = '''
        Create JSON file whith secrets settings varible.
        Default VARIBLES:
            DB name > string;
            DB username > string;
            DB password > very strong password;
            SECRET_KEY;
        '''
    requires_migrations_checks = False
    requires_system_checks = False
    db_name = None
    username = None
    db_pass = None
    SECRET_KEY = base64.b64encode(os.urandom(60)).decode()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.secret_file = os.path.join(settings.SETTINGS_DIR,
                                        'secrets.json')

    def add_arguments(self, parser):
        parser.add_argument(
            '--add',
            action='store_true',
            dest='add',
            help='Add secret value, the NAME is always capitalized!'
        )
        parser.add_argument(
            '--show',
            action='store_true',
            help='Print in console secrets params from secret.json, except password DB!'
        )

    def handle(self, *args, **options):
        if not os.path.exists(self.secret_file):
            exit('Please start "generator" first!')
        if options['add']:
            self._add_param()
        elif options['show']:
            self._show_params()
        else:
            self._db_setup()

    def _check_param(self, *args):
        if '' in args:
            exit('ERROR: Empty data!')

    def _db_setup(self):
        self.db_name = input('DB NAME > ')
        self.username = input('DB USERNAME > ')
        self._check_param(self.db_name, self.username)
        while True:
            self.db_pass = getpass.getpass(prompt='DB PASSWORD > ')
            db_pass2 = getpass.getpass(prompt='DB PASSWORD (again) > ')
            if self.db_pass and secrets.compare_digest(self.db_pass, db_pass2):
                break
            else:
                self.stdout.write(self.style.ERROR('Passwords do not match or empty - repeat!'))
        self._create_secrets()

    def _add_param(self):
        name = input('Type NAME of value > ')
        value = input('Type secret value > ')
        self._check_param(name, value)
        self._update_file({name.upper(): value})

    def _create_secrets(self):
        secret = {
            'NAME': self.db_name,
            'USER': self.username,
            'PASSWORD': self.db_pass,
            'SECRET_KEY': self.SECRET_KEY,
        }
        self._update_file(secret)

    def _update_file(self, custom_secret):
        with open(self.secret_file, 'r') as file:
            secrets = json.load(file)
        secrets.update(custom_secret)
        self._write_file(secrets)
        msg = (
            self.style.SUCCESS('Secrets updated!'),
            self.style.WARNING('Don\'t forget add <NEW_SECRET> value in settings'),
            '<NEW_SECRET> = secrets.<NEW_SECRET>',
        )
        self.stdout.write('\n'.join(msg))

    def _write_file(self, secret):
        with open(self.secret_file, 'w') as file:
            json.dump(secret, file)

    def _show_params(self):
        with open(self.secret_file, 'r') as file:
            secrets = json.load(file)
        line = 0
        n = self.style.WARNING('Name')
        v = self.style.WARNING('Value')
        for name, value in secrets.items():
            if name not in ('PASSWORD', 'SECRET_KEY'):
                params = f'{n}: {name}, \t {v}: {value}'
                line = line if line > len(params) else len(params)
                self.stdout.write(params)
                self.stdout.write('-' * line)
