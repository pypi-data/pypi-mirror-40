from functools import lru_cache
from io import StringIO

from django.core.management import (
    get_commands,
    load_command_class,
    call_command,
    CommandError)
from django.core.exceptions import ImproperlyConfigured


COMMAND_BLACKLIST = (
    ('shell', 'django.core'),
    ('dbshell', 'django.core'),
    ('runserver', 'django.contrib.staticfiles'),
    ('testserver', 'django.core'),
)


def get_filtered_commands():
    commands = get_commands()
    for filter_command, filter_module in COMMAND_BLACKLIST:
        if filter_command in commands and commands[filter_command] == filter_module:
            del commands[filter_command]
    return commands


class WebRunnableCommand:
    def __init__(self, app, name):
        self._app = app
        self._name = name
        self._cmd = load_command_class(app, name)
        self._parser = self._cmd.create_parser('manage.py', name)

    @property
    def app(self):
        return self._app

    @property
    def name(self):
        return self._name

    @property
    @lru_cache(maxsize=4)
    def usage(self):
        return self._parser.format_help()

    def run(self, argv, auto_noinput):
        args = argv.split()
        stdout = StringIO()
        response = ''

        has_noinput = True if '--noinput' in self.usage else False
        if has_noinput and auto_noinput:
            args.append('--noinput')

        try:
            ret_val = call_command(self._cmd, stdout=stdout, stderr=stdout, *args)
            response = "\n".join([
                f"Return value: {ret_val or None}",
                "-------",
                stdout.getvalue(),
            ])
        except (CommandError, ImproperlyConfigured) as exc:
            response = "\n".join([
                'Exception: ' + exc.__class__.__name__,
                str(exc),
            ])
        except SystemExit:
            pass
        stdout.close()

        return response
