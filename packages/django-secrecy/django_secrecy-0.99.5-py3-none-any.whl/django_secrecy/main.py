from .generator import Generator
from .utils import COLORS


def main():
    generator = Generator()
    generator.handle()
    msg = (
        '-'*generator.line,
        f'{COLORS["red"]}ATTENTION! You have created the basic settings!{COLORS["white"]}',
        'For launching in production create DB params,',
        'use "python manage.py secrecy"!',
        'To add secret values, use "python manage.py secrecy --add"',
        f'{COLORS["red"]}Do not forget to add "development.py" to .gitignore{COLORS["white"]}',
        'For help use "generator -h"',
        f'{COLORS["green"]}Happy coding! :){COLORS["white"]}',
        '-'*generator.line,
    )
    print(*msg, sep='\n')


if __name__ == '__main__':
    main()