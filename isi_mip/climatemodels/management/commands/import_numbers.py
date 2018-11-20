import re
import urllib.request
import logging
from datetime import date

from django.core.management.base import BaseCommand

from isi_mip.pages.models import HomePage

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Imports ISIMIP numbers from a textfile link to display on homepage'

    def get_number(self, url):
        try:
            data = urllib.request.urlopen(url)
            lines = data.read().splitlines()
            line = lines[len(lines) - 2].decode('utf-8')
            number = re.search(':(.*)', line).group(1)
            return number.strip()
        except:
            return None

    def handle(self, *args, **options):
        home_pages = HomePage.objects.live()
        for home_page in home_pages:
            number1 = None
            number2 = None
            if home_page.number1_link:
                number1 = self.get_number(home_page.number1_link)
                if number1:
                    print('%s: imported number %s' % (home_page.number1_link, number1))
                    home_page.number1_imported_number = number1
            if home_page.number2_link:
                number2 = self.get_number(home_page.number2_link)
                if number2:
                    print('%s: imported number %s' % (home_page.number2_link, number2))
                    home_page.number2_imported_number = number2
            if number1 or number2:
                home_page.save()
            else:
                print('nothing imported')
        