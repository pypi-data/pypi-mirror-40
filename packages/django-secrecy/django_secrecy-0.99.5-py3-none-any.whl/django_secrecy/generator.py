import os
import sys
import base64
import shutil
import argparse
import json

from .tpl.base_tpl import SETTINGS_TPL
from .utils import COLORS


class Generator:
    """ Generate secrets.json file
        for secrets params django project
        etc:
            'SECRET_KEY': 'KJH(&*@#BKJSDA'
            'MY_SECRET_TOKEN': 'secret TOKEN'

    """
    line = 60

    def __init__(self):
        self.project_name = None
        self.create_dev = None
        self.BASE_DIR, self.SETTINGS_PATH, self.secret_file = self._get_path()
    
    def _check(self, x: str) -> bool: return os.path.exists(x)
    
    def _msg(self, msg: str, msg_type: str = 'success') -> str:
        start = COLORS['green'] if msg_type == 'success' else COLORS['red']
        end = COLORS["white"]
        return f'{start}{msg}{end}'
   
    def _get_proj_name(self):
        description = (
            "Start generator with your project name\n"
            "in project root dir\n"
            "like: generator <project_name>\n"
        )
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument("project_name", type=str, help="Django project name")
        parser.add_argument(
            '--dev',
            action='store_true',
            dest='dev',
            help='Create basic development.py'
        )
        args = parser.parse_args()
        self.create_dev = True if args.dev else False
        return args.project_name

    def _get_path(self):
        self.project_name = self._get_proj_name()
        path = os.getcwd()
        base_dir_settings = os.path.join(path, self.project_name)
        if not self._check(os.path.join(base_dir_settings, 'wsgi.py')):
            msg = (
                '*'*self.line,
                'Sorry, project not found!',
                'Are you shure that you in PROJECT ROOT?',
                '*'*self.line,
            )
            exit(self._msg('\n'.join(msg), 'alert'))
        settings_path = os.path.join(base_dir_settings, 'settings')
        secret_file = os.path.join(settings_path, 'secrets.json')
        return base_dir_settings, settings_path, secret_file

    def _create_settings(self):
        if self._check(self.SETTINGS_PATH):
            return self._msg('You have already created the settings.', 'alert')
        os.mkdir(self.SETTINGS_PATH)
        TPL_PATH = os.path.join(
                        os.path.dirname(
                            os.path.abspath(__file__)), 'tpl')
        TPL = (
            ('init_tpl.py', '__init__.py'),
            ('development_tpl.py', 'development.py'),
            ('production_tpl.py', 'production.py'),
        )
        for file in TPL:
            tpl = os.path.join(TPL_PATH, file[0])
            dist = os.path.join(self.SETTINGS_PATH, file[1])
            try:
                shutil.copy(tpl, dist)
            except FileNotFoundError:
                exit(f'Critical Error: template does not exist > {tpl}')
        self._create_base()
        return self._msg('The settings was created successfully.')

    def _create_base(self):
        base_path = os.path.join(self.SETTINGS_PATH, 'base.py')
        with open(base_path, 'w') as file:
            file.write(SETTINGS_TPL.format(PROJ_NAME=self.project_name))

    def _create_file(self):
        if self._check(self.secret_file):
            return self._msg('The secrets.json already exists.', 'alert')
        secrets = {
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'SECRET_KEY': base64.b64encode(os.urandom(60)).decode(),
        }
        with open(self.secret_file, 'w') as file:
            json.dump(secrets, file)
        return self._msg('The secrets.json was created successfully.')

    def _remove_default(self):
        default = os.path.join(self.BASE_DIR, 'settings.py')
        old = os.path.join(self.BASE_DIR, 'settings.old')
        try:
            shutil.move(default, old)
        except FileNotFoundError:
            print(self._msg('*** File "settings.py" already moved! ***', 'alert'))

    def _create_dev(self):
        dev_path = os.path.join(self.SETTINGS_PATH, 'development.py')
        if self._check(dev_path):
            exit(self._msg('*** File development.py already exists! ***', 'alert'))
        dev_tpl_path = os.path.join(
                        os.path.dirname(
                            os.path.abspath(__file__)),
                            'tpl',
                            'development_tpl.py')
        shutil.copy(dev_tpl_path, dev_path)
        exit(self._msg('*** File development.py created! ***'))

    def handle(self):
        if self.create_dev and self._check(self.SETTINGS_PATH):
            self._create_dev()
        create_settings = self._create_settings()
        create_file = self._create_file()
        msg = (
            '-'*self.line,
            create_settings,
            '-'*self.line,
            create_file,
        )
        # rename default settings file
        self._remove_default()
        print(*msg, sep='\n')
