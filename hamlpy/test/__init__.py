from __future__ import unicode_literals

import django
import os


os.environ['DJANGO_SETTINGS_MODULE'] = 'hamlpy.test.settings'
django.setup()
