import math

from wagtail.wagtailcore.blocks import StructBlock
from wagtail.wagtailcore.blocks.field_block import TextBlock, RichTextBlock

from isi_mip.climatemodels.models import InputData, OutputData, ImpactModel
from isi_mip.contrib.blocks import IntegerBlock


class ImpactModelsBlock(StructBlock):
    description = RichTextBlock()
    rows_per_page = IntegerBlock(default=20, min_value=1, required=True)

    def get_context(self, value):
        context = super().get_context(value)

        ims = ImpactModel.objects.all()

        context['tableid'] = 'selectortable'
        context['searchfield'] = {'value': ''}
        sector_options = [{'value': x} for x in ims.values_list('sector', flat=True).distinct().order_by('sector')]
        cdriver_options = [{'value': x} for x in InputData.objects.values_list('data_set', flat=True).distinct().order_by('data_set')]
        context['selectors'] = [
            {'colnumber': '2',  'all_value': 'Sector', 'options': sector_options},
            {'colnumber': '3', 'all_value': 'Climate Driver', 'options': cdriver_options},
        ]
        # tabelle
        context['id'] = 'selectortable'
        context['head'] = {
            'cols': [{'text': 'Model'}, {'text': 'Sector'}, {'text': 'Climate Driver'}, {'text': 'Contact'}]
        }
        # context['filter'] = {"2": "Water (global)"},  # pre defined filter

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
            cpeople = ["%s <a href='mailto:%s'>%s</a>" % (x.name, x.email, x.email) for x in imodel.contactperson_set.all()]
            values = [["<a href='details/%d/'>%s</a>" % (imodel.id, imodel.name)], [imodel.sector]]
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
        template = 'blocks/impact_models_block.html'


class InputDataBlock(StructBlock):
    description = RichTextBlock()
    row_limit = IntegerBlock(default=10, min_value=1, max_value=30)

    def get_context(self, value):
        context = super().get_context(value)
        context['title'] = 'Input Data'

        context['head'] = {'cols': [{'text': 'Data Set'}, {'text': 'Data Type'}, {'text': 'Description'}]}
        context['body'] = {
            'rowlimit': {'buttontext': 'See all <i class="fa fa-chevron-down"></i>', 'rownumber': 3},
            'rows': []
        }
        context['showalllink'] = {'buttontext': 'See all <i class="fa fa-chevron-down"></i>'}

        for i, idata in enumerate(InputData.objects.all()):
            link = "<a href='details/{ds}'>{ds}</a>".format(ds=idata.data_set)
            context['body']['rows'] += [
                {'cols': [
                    {'texts': [link]},
                    {'texts': [idata.data_type]},
                    {'texts': [idata.description]}],
                    'invisible': i >= value.get('row_limit')
                }
            ]

        return context

    class Meta:
        template = 'blocks/input_data_block.html'


class OutputDataBlock(StructBlock):
    description = RichTextBlock()

    def get_context(self, value):
        context = super().get_context(value)
        context['title'] = 'Overview'

        context['head'] = {'cols': [{'text': 'Sector'}, {'text': 'Model'}, {'text': 'Scenario'},
                                    {'text': 'Climate Driver'}, {'text': 'Date'}]}
        context['body'] = {
            'rows': []
        }

        for outputdate in OutputData.objects.all():
            drivers = [x.data_set for x in outputdate.drivers.all()]
            context['body']['rows'] += [
                {'cols': [
                    {'texts': [outputdate.sector]},
                    {'texts': [outputdate.model]},
                    {'texts': [outputdate.scenario]},
                    {'texts': drivers},
                    {'texts': [outputdate.date]}]
                }
            ]

        return context

    class Meta:
        template = 'blocks/output_data_block.html'