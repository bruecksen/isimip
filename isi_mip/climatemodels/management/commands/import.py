from django.core.management.base import BaseCommand

from isi_mip.climatemodels.import_xlsx import XLSImport

class Command(BaseCommand):
    help = 'Import XLSx file'

    # def add_arguments(self, parser):
    #     parser.add_argument('filename', nargs='+', type=str)

    def handle(self, *args, **options):
        # filename = options['filename'][0]
        filename = 'data/Model_Experiment_Documentation.xlsx'
        xls = XLSImport(filename)
        xls.run()