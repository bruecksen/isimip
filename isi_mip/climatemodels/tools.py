from collections import OrderedDict
import xlsxwriter

from django.db.models import ManyToOneRel, ManyToManyRel, ManyToManyRel, ManyToManyField, ForeignKey

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

SKIP_FIELDS = [
    'id',
    'base_model',
    'public',
    'impact_model',
    'impact_model_owner',
    'impact_model_involved',
    'technicalinformation',
    'inputdatainformation',
    'otherinformation',
    'genericsector',
    'agriculture',
    'biomes',
    'forests',
    'energy',
    'marineecosystemsglobal',
    'marineecosystemsregional',
    'waterglobal',
    'waterregional',
    'biodiversity',
    'health',
    'coastalinfrastructure',
    'permafrost',
    'computablegeneralequilibriummodelling',
    'agroeconomicmodelling',
    'outputdata',
]

SORT_ORDER = {
    "contactperson": 1,
    "main_reference_paper": 1,
    "other_references": 2,
}


class ImpactModelToXLSX:
    # https://xlsxwriter.readthedocs.org/en/latest/
    def __init__(self, res, qs):
        self.workbook = xlsxwriter.Workbook(res, {'in_memory': True})
        self.qs = qs
        self.xlsxdings()

    def get_field_data(self, model, field_name):
        field = model._meta.get_field(field_name)
        if isinstance(field, ManyToManyField):
            data = ", ".join(["%s" % i for i in getattr(model, field_name).all()])
        elif isinstance(field, ManyToOneRel) or isinstance(field, ManyToManyRel):
            data = ", ".join(["%s" % i for i in getattr(model, "%s_set" % field_name).all()])
        else:
            data = getattr(model, field_name) or ''
        return data

    def xlsxdings(self):
        general = self.workbook.add_worksheet('General Information')
        general.set_column('A:A', 20)
        bold = self.workbook.add_format({'bold': True})
        models = [BaseImpactModel, ImpactModel, TechnicalInformation, InputDataInformation, OtherInformation]
        model_fields = OrderedDict()
        all_field_titles = []
        for model in models:
            fields = model._meta.get_fields()
            filtered_fields = [field for field in fields if field.name not in (SKIP_FIELDS)]
            filtered_fields.sort(key=lambda val: SORT_ORDER[val.name] if val.name in SORT_ORDER else 0)
            model_fields[model.__name__] = {
                'class': model,
                'fields': [f.name for f in filtered_fields],
            }
            for field in filtered_fields:
                if hasattr(field, 'verbose_name'):
                    all_field_titles.append(field.verbose_name.capitalize())
                else:
                    name = field.name.replace("_", " ").capitalize()
                    all_field_titles.append(name)
        general.write_row(0, 0, data=all_field_titles, cell_format=bold)
        for i, impact_model in enumerate(self.qs):
            for j, field in enumerate(model_fields['BaseImpactModel']['fields']):
                data = self.get_field_data(impact_model.base_model, field)
                general.write(i + 1, j, str(data))
            for j, field in enumerate(model_fields['ImpactModel']['fields'], start=j + 1):
                data = self.get_field_data(impact_model, field)
                general.write(i + 1, j, str(data))
            for j, field in enumerate(model_fields['TechnicalInformation']['fields'], start=j + 1):
                instance = impact_model.technicalinformation
                data = getattr(instance, field) or ''
                general.write(i + 1, j, str(data))
            for j, field in enumerate(model_fields['InputDataInformation']['fields'], start=j + 1):
                instance = impact_model.inputdatainformation
                data = self.get_field_data(instance, field)
                general.write(i + 1, j, str(data))
            for j, field in enumerate(model_fields['OtherInformation']['fields'], start=j + 1):
                instance = impact_model.otherinformation
                data = self.get_field_data(instance, field)
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


class ParticpantModelToXLSX:
    # https://xlsxwriter.readthedocs.org/en/latest/
    def __init__(self, res, qs):
        self.workbook = xlsxwriter.Workbook(res, {'in_memory': True})
        self.qs = qs
        self.process_xlsx()

    def process_xlsx(self):
        general = self.workbook.add_worksheet('Participants')
        general.set_column('A:A', 20)
        bold = self.workbook.add_format({'bold': True})
        header = ['Name', 'Email', 'Instiute', 'Country', 'Model', 'Sector', 'Comment']
        general.write_row(0, 0, data=header, cell_format=bold)
        for i, participant in enumerate(self.qs):
            general.write(i + 1, 0, participant.userprofile.name)
            general.write(i + 1, 1, participant.email)
            general.write(i + 1, 2, participant.userprofile.institute)
            general.write(i + 1, 3, participant.userprofile.country and participant.userprofile.country.name or '')
            models = [str(model) for model in participant.userprofile.involved.all()]
            general.write(i + 1, 4, ", ".join(models))
            sectors = [sector.name for sector in participant.userprofile.sector.all()]
            general.write(i + 1, 5, ", ".join(sectors))
            general.write(i + 1, 6, participant.userprofile.comment)
        self.workbook.close()
