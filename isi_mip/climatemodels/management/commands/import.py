from datetime import date

from django.core.management.base import BaseCommand

from isi_mip.climatemodels.import_xlsx import XLSImport
from isi_mip.climatemodels.models import InputData, ClimateDataType, InputPhase, ClimateVariable, OutputData, \
    ImpactModel, Scenario


class Command(BaseCommand):
    help = 'Import XLSx file'

    # def add_arguments(self, parser):
    #     parser.add_argument('filename', nargs='+', type=str)

    def handle(self, *args, **options):
        # filename = options['filename'][0]
        filename = 'data/Model_Experiment_Documentation.xlsx'
        xls = XLSImport(filename)
        xls.run()
        inputdata = InputData.objects.get_or_create(name='Princeton')[0]
        inputdata.data_type = ClimateDataType.objects.get_or_create(name='Historical climate')[0]
        inputdata.scenario = Scenario.objects.get_or_create(name='hist-obs')[0]
        cvariables = [
            ('daily mean temperature', 'tas'),
            ('daily maximum temperature', 'tasmax'),
            ('daily minimum temperature', 'tasmin'),
            ('total precipitation', 'pr'),
            ('snowfall', 'prsn'),
        ]
        for name,abbr in cvariables:
            cv = ClimateVariable.objects.get_or_create(name=name,abbreviation=abbr)[0]
            inputdata.variables.add(cv)
        inputdata.phase = InputPhase.objects.get_or_create(name='ISIMIP2a')[0]
        inputdata.description = 'This data set provides global climate data for the period  1948-2008 on a 0.5°x0.5°C grid in daily time steps.  The data set was published by the Terrestrial Hydrology Group at Princeton University (LINK). The data set blends reanalysis data with observations.'
        inputdata.caveats = 'This dataset was updated in the ISIMIP repository on 4 February, 2016. When referring to this data set, the following paper should be cited:  Sheffield, J., G. Goteti, and E. F. Wood, 2006: Development of a 50-yr high-resolution global dataset of meteorological forcings for land surface modeling, J. Climate, 19 (13), 3088-3111'
        inputdata.save()
        cvariables = [
            ('surface air pressure', 'ps'),
            ('relative humidity', 'rhs or hurs'),
            ('long wave downwelling radiation', 'rlds'),
            ('short wave downwelling radiation', 'rsds'),
            ('near-surface wind magnitude', 'wind'),
            ('eastward near-surface wind', 'u'),
            ('northward near-surface wind', 'v'),
            ('bottom temperature',''),
            ('top temperature',''),
            ('salinity',''),
            ('O2',''),
            ('pH',''),
            ('currents',''),
            ('primary production','')
        ]
        for name,abbr in cvariables:
            cv = ClimateVariable.objects.get_or_create(name=name,abbreviation=abbr)[0]

        odata = OutputData.objects.get_or_create(
            sector='Agriculture',
            model=ImpactModel.objects.get(name='ORCHIDEE'),
            date=date(2016,4,16)
        )[0]
        for scen in ['hist-obs', 'co2', 'nosoc']:
            scenx = Scenario.objects.get_or_create(name=scen)[0]
            odata.scenarios.add(scenx)
        odata.drivers.add(inputdata)
        odata.save()
