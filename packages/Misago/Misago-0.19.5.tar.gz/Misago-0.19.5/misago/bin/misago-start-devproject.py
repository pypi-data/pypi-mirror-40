#!/usr/bin/env python
# pylint: disable=E0401
"""
Creates a dev project for local development
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PROJECT_NAME = 'devproject'


def main():
    settings_file = os.path.join(BASE_DIR, PROJECT_NAME, PROJECT_NAME, 'settings.py')

    # Avoid recreating if already present
    if os.path.exists(settings_file):
        return

    from misago.core import setup

    setup.start_misago_project()
    fill_in_settings(settings_file)


def fill_in_settings(f):
    with open(f, 'r') as fd:
        s = fd.read()

        # Read PostgreSQL's config from env variables
        s = s.replace("'NAME': '',", "'NAME': os.environ.get('POSTGRES_DB'),")
        s = s.replace("'USER': '',", "'USER': os.environ.get('POSTGRES_USER'),")
        s = s.replace("'PASSWORD': '',", "'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),")
        s = s.replace("'HOST': 'localhost',", "'HOST': os.environ.get('POSTGRES_HOST'),")

        # Specify console backend for email
        s += "\n"
        s += "\n# Set dev instance to send e-mails to console"
        s += "\n"
        s += "\nEMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'"
        s += "\n"

        # Tie Debug Toolbar visibility to env variable
        s += "\n"
        s += "\n# Display debug toolbar if IN_MISAGO_DOCKER enviroment var is set to \"1\""
        s += "\n"
        s += "\nDEBUG_TOOLBAR_CONFIG = {"
        s += "\n    'SHOW_TOOLBAR_CALLBACK': 'misago.conf.debugtoolbar.enable_debug_toolbar'"
        s += "\n}"
        s += "\n"

        # Empty the contents of STATICFILES_DIRS (STATICFILES_DIRS = [])
        pos = s.find('STATICFILES_DIRS')
        s = s[:s.find('[', pos) + 1] + s[s.find(']', pos):]

        # Remove theme dir from template dirs
        pos = s.find("'DIRS': [")
        s = s[:s.find('[', pos) + 1] + s[s.find(']', pos):]

    with open(f, 'w') as fd:
        fd.write(s)


if __name__ == '__main__':
    sys.argv.append(PROJECT_NAME)
    sys.path.append(BASE_DIR)
    main()