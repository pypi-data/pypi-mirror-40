from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.management.commands import changepassword
from django.db import DEFAULT_DB_ALIAS
from django.utils.crypto import get_random_string

UserModel = get_user_model()


class Command(changepassword.Command):
    help = 'Sets a password to something random. This helps create a superuser when you can\'t log into a shell.'

    def add_arguments(self, parser):
        parser.add_argument(
            'username', nargs=1,
            help='Username to change password for.',
        )
        parser.add_argument(
            '--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS,
            help='Specifies the database to use. Default is "default".',
        )

    def handle(self, *args, **options):
        username = options['username'][0]
        try:
            u = UserModel._default_manager.using(options['database']).get(**{
                UserModel.USERNAME_FIELD: username
            })
        except UserModel.DoesNotExist:
            raise CommandError("user '%s' does not exist" % username)

        self.stdout.write("Changing password for user '%s'\n" % u)

        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@$%^*(-_)'
        password = get_random_string(30, chars)
        u.set_password(password)
        u.save()

        return "Password changed successfully for user '%s': %s" % (u, password)