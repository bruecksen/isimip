import xlsxwriter

from isi_mip.climatemodels.models import ImpactModel, Sector

EMPTY_SECTORS = [
    'Agro-Economic Modelling',
    'Biodiversity',
    'Coastal Infrastructure',
    'Computable General Equilibrium Modelling',
    'Health',
    'Permafrost',
]


class ImpactModelToXLSX:
    # https://xlsxwriter.readthedocs.org/en/latest/
    def __init__(self, res, qs):
        self.workbook = xlsxwriter.Workbook(res, {'in_memory': True})
        self.qs = qs.order_by('name')
        self.xlsxdings()

    def xlsxdings(self):
        sectors = set(x.sector for x in self.qs)
        # if len(sectors) == 1:
        #     " NUR EIN SHEET "
        # elif len(sectors) < 1:
        #     raise Exception("No sector at all? This shouldn't happen.")
        # else:
        if True:
            general = self.workbook.add_worksheet('General Information')
            general.set_column('A:A', 20)
            bold = self.workbook.add_format({'bold': True})
            fields = [field.name for field in ImpactModel._meta.fields[1:] if field.name is not 'owner']
            general.write_row(0, 0, data=[x.title() for x in fields], cell_format=bold)

            for i, impactmodel in enumerate(self.qs):
                data = impactmodel
                for j, f in enumerate(fields):
                    inhalt = getattr(data, f) or ''
                    general.write(i + 1, j, str(inhalt))

            for sector_name in sorted(sectors):
                if sector_name in EMPTY_SECTORS:
                    continue
                xsector = Sector.get(sector_name)
                entries = xsector.objects.filter(impact_model__in=self.qs).order_by('impact_model__name')
                if not entries:
                    continue

                sector_name = 'M. E. and Fisheries (regional)' if sector_name == 'Marine Ecosystems and Fisheries (regional)' else sector_name
                sector_name = 'M. E. and Fisheries (global)' if sector_name == 'Marine Ecosystems and Fisheries (global)' else sector_name
                # sector_name = 'Computable General Equilibrium' if
                sectorsheet = self.workbook.add_worksheet(sector_name[0:31])
                fields = [field.name for field in xsector._meta.fields[1:]]
                sectorsheet.write_row(0, 0, data=[x.title() for x in fields], cell_format=bold)
                for i, entry in enumerate(entries):
                    data = entry
                    for j, f in enumerate(fields):
                        inhalt = getattr(data, f) or ''
                        sectorsheet.write(i + 1, j, str(inhalt))

            self.workbook.close()
