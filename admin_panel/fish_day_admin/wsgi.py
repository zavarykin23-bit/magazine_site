"""
WSGI config for fish_day_admin project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fish_day_admin.settings')

application = get_wsgi_application()
