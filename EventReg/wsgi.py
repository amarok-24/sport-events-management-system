"""
WSGI config for EventReg project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

# from dotenv import load_dotenv
# load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EventReg.settings')

application = get_wsgi_application()