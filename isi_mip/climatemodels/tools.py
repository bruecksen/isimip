from collections import OrderedDict
import xlsxwriter

from isi_mip.climatemodels.models import BaseImpactModel, ImpactModel, Sector, TechnicalInformation, \
    InputDataInformation, OtherInformation, SectorInformationField

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
        self.qs = qs
        self.xlsxdings()

    def xlsxdings(self):
        general = self.workbook.add_worksheet('General Information')
        general.set_column('A:A', 20)
        bold = self.workbook.add_format({'bold': True})
        models = [BaseImpactModel, ImpactModel, TechnicalInformation, InputDataInformation, OtherInformation]
        model_fields = OrderedDict()
        all_field_titles = []
        for model in models:
            fields = model._meta.fields
            filtered_fields = [field for field in fields if field.name not in ('id', 'owners', 'base_model', 'public', 'impact_model')]
            model_fields[model.__name__] = {
                'class': model,
                'fields': [f.name for f in filtered_fields],
            }
            all_field_titles.extend([x.verbose_name for x in filtered_fields])
        general.write_row(0, 0, data=all_field_titles, cell_format=bold)
        for i, impact_model in enumerate(self.qs):
            for j, field in enumerate(model_fields['BaseImpactModel']['fields']):
                data = getattr(impact_model.base_model, field) or ''
                general.write(i + 1, j, str(data))
            for j, field in enumerate(model_fields['ImpactModel']['fields'], start=j+1):
                data = getattr(impact_model, field) or ''
                general.write(i + 1, j, str(data))
            for j, field in enumerate(model_fields['TechnicalInformation']['fields'], start=j+1):
                instance = impact_model.technicalinformation
                data = getattr(instance, field) or ''
                general.write(i + 1, j, str(data))
            for j, field in enumerate(model_fields['InputDataInformation']['fields'], start=j+1):
                instance = impact_model.inputdatainformation
                data = getattr(instance, field) or ''
                general.write(i + 1, j, str(data))
            for j, field in enumerate(model_fields['OtherInformation']['fields'], start=j+1):
                instance = impact_model.otherinformation
                data = getattr(instance, field) or ''
                general.write(i + 1, j, str(data))

        for sector in Sector.objects.all():
            fields = []
            if sector.name in EMPTY_SECTORS:
                continue
            elif not sector.model.objects.filter(impact_model__in=self.qs).exists():
                continue
            else:
                fields = [field.name for field in sector.model._meta.fields if field.name not in ('id', 'data')]

            sector_name = 'M. E. and Fisheries (regional)' if sector.name == 'Marine Ecosystems and Fisheries (regional)' else sector.name
            sector_name = 'M. E. and Fisheries (global)' if sector.name == 'Marine Ecosystems and Fisheries (global)' else sector.name
            sectorsheet = self.workbook.add_worksheet(sector_name[0:31])
            generic_fields = SectorInformationField.objects.filter(information_group__sector=sector).order_by('information_group')
            sectorsheet.write_row(0, 0, data=[x.title() for x in fields], cell_format=bold)
            sectorsheet.write_row(0, len(fields), data=[x.name for x in generic_fields], cell_format=bold)
            for i, entry in enumerate(sector.model.objects.filter(impact_model__in=self.qs)):
                for j, f in enumerate(fields):
                    value = getattr(entry, f) or ''
                    sectorsheet.write(i + 1, j, str(value))
                for j, f in enumerate(generic_fields):
                    value = entry.data and entry.data.get(f.unique_identifier, '') or ''
                    sectorsheet.write(i + 1, len(fields) + j, str(value))

        self.workbook.close()
