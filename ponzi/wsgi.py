"""
WSGI config for ponzi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
load_dotenv()
from threading import Thread
from transactions.models import Transaction
import requests
import time
from decimal import Decimal 
from coinbase.wallet.client import Client


from .balanceLuno import balanceLuno

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ponzi.settings')

application = get_wsgi_application()

# def s():
#   Timer(5.0, s).start()


# Timer(5.0, s).start()


def run():
    while True:
        time.sleep(3)
        try:
            balanceLuno()
            print('PASS1')
        except Exception as e:
            print(e)
            balanceLuno()
            print('pass2')


thread_run = Thread(target=run)
thread_run.start()

