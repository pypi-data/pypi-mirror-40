import sys
import logging

from django.conf import settings, global_settings
from django.core.management.base import BaseCommand

import otree.bots.runner
from otree.bots.runner import run_pytests

import otree.common_internal

logger = logging.getLogger('otree')

settings.STATICFILES_STORAGE = global_settings.STATICFILES_STORAGE

from otree.constants_internal import AUTO_NAME_BOTS_EXPORT_FOLDER

class Command(BaseCommand):
    help = ('Discover and run experiment tests in the specified '
            'modules or the current directory.')

    def _get_action(self, parser, signature):
        option_strings = list(signature)
        for idx, action in enumerate(parser._actions):
            if action.option_strings == option_strings:
                return parser._actions[idx]

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument(
            'session_config_name', nargs='?',
            help='If omitted, all sessions in SESSION_CONFIGS are run'
        )

        ahelp = (
            'Number of participants. '
            'Defaults to minimum for the session config.'
        )
        parser.add_argument(
            'num_participants', type=int, nargs='?',
            help=ahelp)

        parser.add_argument(
            '--export', nargs='?', const=AUTO_NAME_BOTS_EXPORT_FOLDER,
            help=(
                'Saves the data generated by the tests. '
                'Runs the "export data" command, '
                'outputting the CSV files to the specified directory, '
                'or an auto-generated one.'),
            )
        parser.add_argument(
            '--save', nargs='?', const=AUTO_NAME_BOTS_EXPORT_FOLDER,
            help=(
                'Alias for --export.'),
            )

        v_action = self._get_action(parser, ("-v", "--verbosity"))
        v_action.default = '1'
        v_action.help = (
            'Verbosity level; 0=minimal output, 1=normal output,'
            '2=verbose output (DEFAULT), 3=very verbose output')

    def execute(self, *args, **options):
        if int(options['verbosity']) > 3:
            logger = logging.getLogger('py.warnings')
            handler = logging.StreamHandler()
            logger.addHandler(handler)
        super(Command, self).execute(*args, **options)
        if int(options['verbosity']) > 3:
            logger.removeHandler(handler)

    def handle(self, **options):
        # use in-memory.
        # this is the simplest way to patch tests to use in-memory,
        # while still using Redis in production
        settings.CHANNEL_LAYERS['default'] = settings.CHANNEL_LAYERS['inmemory']
        # so we know not to use Huey
        otree.common_internal.USE_REDIS = False

        # To make tests run faster, autorefresh should be set to True
        # http://whitenoise.evans.io/en/latest/django.html#whitenoise-makes-my-tests-run-slow
        settings.WHITENOISE_AUTOREFRESH = True

        export_path = options["export"] or options["save"]
        preserve_data = bool(export_path)

        exit_code = run_pytests(
            session_config_name=options["session_config_name"],
            num_participants=options['num_participants'],
            preserve_data=preserve_data,
            export_path=export_path,
            verbosity=options['verbosity'],
        )

        if not preserve_data:
            logger.info('Tip: Run this command with the --export flag'
                        ' to save the data generated by bots.')

        sys.exit(exit_code)
