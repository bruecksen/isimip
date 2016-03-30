import json

import requests
from django.core.management.base import BaseCommand

from twitter import *


class Command(BaseCommand):
    help = 'Twitte'

    def handle(self, *args, **options):

        # bla = requests.get("https://twitter.com/i/search/timeline?f=realtime&q=@isimipimpacts&src=typd")
        # jsi = bla.json()
        # import ipdb; ipdb.set_trace()
        "https: // twitter.com / ISIMIPImpacts"
        # filename = options['filename'][0]
        # filename = 'data/Model_Experiment_Documentation.xlsx'
        # xls = XLSImport(filename)
        # xls.run()

