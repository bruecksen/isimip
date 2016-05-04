import math

from django.utils.html import urlize
from wagtail.wagtailcore.blocks import StructBlock
from wagtail.wagtailcore.blocks.field_block import TextBlock, RichTextBlock

from isi_mip.climatemodels.models import InputData, OutputData, ImpactModel
from isi_mip.contrib.blocks import IntegerBlock


class ImpactModelsBlock(StructBlock):
    description = RichTextBlock()
    rows_per_page = IntegerBlock(default=20, min_value=1, required=True)

    def get_context(self, value):
        context = super().get_context(value)

        ims = ImpactModel.objects.order_by('name')

        # Filter und Suchfelder
        context['tableid'] = 'selectortable'
        context['searchfield'] = {'value': ''}
        sector_options = [{'value': x} for x in ims.values_list('sector', flat=True).distinct().order_by('sector')]
        cdriver_options = [{'value': x} for x in
                           InputData.objects.values_list('name', flat=True).distinct().order_by('name')]
        context['selectors'] = [
            {'colnumber': '2', 'all_value': 'All Sectors', 'options': sector_options, 'name': 'sector'},
            {'colnumber': '3', 'all_value': 'All Climate Drivers', 'options': cdriver_options, 'name': 'driver'},
        ]

        # Tabelle
        context['id'] = 'selectortable'
        context['head'] = {
            'cols': [{'text': 'Model'}, {'text': 'Sector'}, {'text': 'Climate Driver'}, {'text': 'Contact'}]
        }
        numpages = math.ceil(ims.count() / value.get('rows_per_page'))
        context['pagination'] = {
            'rowsperpage': (value.get('rows_per_page')),
            'numberofpages': numpages,  # number of pages with current filters
            'pagenumbers': [{'number': i + 1, 'invisible': False} for i in range(numpages)],
            'activepage': 1,  # set to something between 1 and numberofpages
        }
        context['norowvisible'] = False  # true when no row is visible

        bodyrows = []
        i = 0
        for imodel in ims:
            datasets = [str(x) for x in imodel.climate_data_sets.all()]
            # import ipdb; ipdb.set_trace()
            cpeople = ["{0.name}<br/><a href='mailto:{0.email}'>{0.email}</a>".format(x) for x in
                       imodel.contactperson_set.all()]
            values = [["<a href='details/{0.id}/'>{0.name}</a>".format(imodel)], [imodel.sector]]
            values += [datasets] + [["<br/>".join(cpeople)]]
            row = {
                'invisible': i >= value.get('rows_per_page'),
                'cols': [{'texts': x} for x in values]
            }
            i += 1
            bodyrows.append(row)

        context['body'] = {'rows': bodyrows}
        return context

    class Meta:
        icon = 'fa fa-database'
        template = 'blocks/impact_models_block.html'


class InputDataBlock(StructBlock):
    description = RichTextBlock()
    row_limit = IntegerBlock(default=10, min_value=1, max_value=30)

    def get_context(self, value):
        context = super().get_context(value)
        context['title'] = 'Input Data'

        context['head'] = {'cols': [{'text': 'Data Set'}, {'text': 'Data Type'}, {'text': 'Description'}]}
        context['body'] = {
            'rowlimit': {'buttontext': 'See all <i class="fa fa-chevron-down"></i>',
                         'rownumber': value.get('row_limit')},
            'rows': []
        }

        inputdata = InputData.objects.all()
        for i, idata in enumerate(inputdata):
            link = "<a href='details/{0.id}'>{0.name}</a>".format(idata)
            context['body']['rows'] += [
                {'cols': [
                    {'texts': [link]},
                    {'texts': [idata.data_type]},
                    {'texts': [urlize(idata.description)]}],
                    'invisible': i >= value.get('row_limit')
                }
            ]

        if value.get('row_limit') < inputdata.count():
            context['showalllink'] = {'buttontext': 'See all <i class="fa fa-chevron-down"></i>'}
        return context

    class Meta:
        icon = 'fa fa-database'
        template = 'blocks/input_data_block.html'


class OutputDataBlock(StructBlock):
    description = RichTextBlock()

    def get_context(self, value):
        context = super().get_context(value)
        context['title'] = 'Overview'

        context['head'] = {'cols': [{'text': 'Sector'}, {'text': 'Model'}, {'text': 'Scenario'},
                                    {'text': 'Climate Driver'}, {'text': 'Date'}]}
        context['body'] = {
            'rows': [],
        }

        for outputdata in OutputData.objects.all():
            drivers = [x.name for x in outputdata.drivers.all()]
            scenarios = ', '.join(x.name for x in outputdata.scenarios.all())
            context['body']['rows'] += [
                {'cols': [
                    {'texts': [outputdata.sector]},
                    {'texts': [outputdata.model]},
                    {'texts': [scenarios]},
                    {'texts': drivers},
                    {'texts': [outputdata.date]}]
                }
            ]
        context['id'] = 'selectorable'
        context['tableid'] = 'selectorable'
        context['searchfield'] = {'value': ''}
        return context

    class Meta:
        icon = 'fa fa-database'
        template = 'blocks/output_data_block.html'
