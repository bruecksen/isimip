import xlsxwriter

from isi_mip.climatemodels.models import ImpactModel

# https://xlsxwriter.readthedocs.org/en/latest/

class ImpactModelToXLSX:
    def __init__(self, res, qs):
        self.workbook = xlsxwriter.Workbook(res)
        self.qs = qs
        self.xlsxdings()

    def xlsxdings(self):
        general = self.workbook.add_worksheet('General Information')

        general.set_column('A:A', 20)
        bold = self.workbook.add_format({'bold': True})
        fields = [field.name for field in ImpactModel._meta.fields[1:] if field.name is not 'owner' ]
        general.write_row(0,0, data=fields, cell_format=bold)
        # import ipdb; ipdb.set_trace()
        for i, impactmodel in enumerate(self.qs):
            data = impactmodel
            for j,f in enumerate(fields):
                general.write(i+1, j, str(getattr(data,f)))

        self.workbook.close()
