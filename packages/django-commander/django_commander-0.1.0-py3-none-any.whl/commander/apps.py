from django.apps import AppConfig
from django.core import checks
from django.conf import settings


def commander_key_nondefault(app_configs, **kwargs):
    errors = []
    try:
        COMMANDER_KEY = settings.COMMANDER_KEY
    except AttributeError:
        COMMANDER_KEY = None
        errors.append(
            checks.Error(
                'Missing COMMANDER_KEY',
                hint='Add COMMANDER_KEY to your settings',
                id='commander.E001'
            )
        )

    if COMMANDER_KEY == 's00pers3cret!':
        errors.append(
            checks.Warning(
                'Invalid COMMANDER_KEY',
                hint='Switch to something other than the default / example key',
                id='commander.E002'
            )
        )

    return errors


class CommanderConfig(AppConfig):
    name = 'commander'

    def ready(self):
        checks.register(checks.Tags.security)(commander_key_nondefault)
