import math

from django.utils.html import urlize
from wagtail.wagtailcore.blocks import StructBlock
from wagtail.wagtailcore.blocks.field_block import TextBlock

from isi_mip.climatemodels.models import InputData, OutputData, BaseImpactModel, SimulationRound
from isi_mip.contrib.blocks import IntegerBlock, RichTextBlock


class ImpactModelsBlock(StructBlock):
    description = RichTextBlock()
    rows_per_page = IntegerBlock(default=20, min_value=1, required=True)

    def get_context(self, value, parent_context=None):
        context = super(ImpactModelsBlock, self).get_context(value, parent_context=parent_context)

        bims = BaseImpactModel.objects.select_related('sector').prefetch_related('impact_model', 'impact_model_owner', 'impact_model_owner__user')
        bims = bims.filter(impact_model__public=True).distinct().order_by('name')

        # Filter und Suchfelder
        context['tableid'] = 'selectortable'
        context['searchfield'] = {'value': ''}
        sector_options = [{'value': x} for x in bims.values_list('sector__name', flat=True).distinct().order_by('sector')]
        simulation_round_options = [{'value': x} for x in SimulationRound.objects.values_list('name', flat=True).distinct().order_by('-order')]
        context['selectors'] = [
            {'colnumber': '2', 'all_value': 'All Simulation Rounds', 'options': simulation_round_options, 'name': 'simulation_round'},
            {'colnumber': '3', 'all_value': 'All Sectors', 'options': sector_options, 'name': 'sector'},
        ]
        # Tabelle
        context['id'] = 'selectortable'
        context['head'] = {
            'cols': [{'text': 'Model'}, {'text': 'Simulation round'}, {'text': 'Sector'}, {'text': 'Contact Person'}, {'text': 'Email'}]
        }
        rows_per_page = value.get('rows_per_page')
        numpages = math.ceil(bims.count() / rows_per_page)
        context['pagination'] = {
            'rowsperpage': (rows_per_page),
            'numberofpages': numpages,  # number of pages with current filters
            'pagenumbers': [{'number': i + 1, 'invisible': False} for i in range(numpages)],
            'activepage': 1,  # set to something between 1 and numberofpages
        }
        context['norowvisible'] = False  # true when no row is visible

        context['body'] = {'rows': []}
        for i, bmodel in enumerate(bims):
            simulation_rounds = bmodel.impact_model.filter(public=True).values_list('simulation_round__name', flat=True)
            values = [["<a href='details/{0.id}/'>{0.name}</a>".format(bmodel, bmodel)], simulation_rounds, [bmodel.sector]]
            values += [["{0.name}<br/>".format(x) for x in bmodel.impact_model_owner.all()]]
            values += [["<a href='mailto:{0.email}'>{0.email}</a><br/>".format(x) for x in bmodel.impact_model_owner.all()]]
            row = {
                'invisible': i >= rows_per_page,
                'cols': [{'texts': x} for x in values],
            }
            context['body']['rows'] += [row]

        return context

    class Meta:
        icon = 'fa fa-database'
        template = 'blocks/impact_models_block.html'


class InputDataBlock(StructBlock):
    row_limit = IntegerBlock(default=10, min_value=1, max_value=30, label='Input Data Row Limit')

    def get_context(self, value, parent_context=None):
        context = super(InputDataBlock, self).get_context(value, parent_context=parent_context)

        context['head'] = {'cols': [{'text': 'Data Set'}, {'text': 'Data Type'}, {'text': 'Simulation round'}, {'text': 'Description'}]}
        context['body'] = {'rows': []}

        inputdata = InputData.objects.all()
        row_limit = value.get('row_limit')
        numpages = math.ceil(inputdata.count() / row_limit)

        for i, idata in enumerate(inputdata):
            link = "<a href='details/{0.id}'>{0.name}</a>".format(idata)
            context['body']['rows'] += [{
                'cols': [
                    {'texts': [link]},
                    {'texts': [idata.data_type]},
                    {'texts': [sr.name for sr in idata.simulation_round.all()]},
                    {'texts': [urlize(idata.description)]}], 'invisible': i >= row_limit
            }]
        context['pagination'] = {
            'rowsperpage': row_limit,
            'numberofpages': numpages,  # number of pages with current filters
            'pagenumbers': [{'number': i + 1, 'invisible': False} for i in range(numpages)],
            'activepage': 1,  # set to something between 1 and numberofpages
        }
        context['id'] = 'selectorable'
        context['tableid'] = 'selectorable'
        context['searchfield'] = {'value': ''}
        return context

    class Meta:
        icon = 'fa fa-database'
        template = 'blocks/input_data_block.html'


class OutputDataBlock(StructBlock):
    rows_per_page = IntegerBlock(default=20, min_value=1, required=True)

    def get_context(self, value, parent_context=None):
        context = super(OutputDataBlock, self).get_context(value, parent_context=parent_context)
        context['title'] = 'Overview'

        context['head'] = {'cols': [{'text': 'Sector'}, {'text': 'Model'}, {'text': 'Simulation Rounds'}, {'text': 'Experiments'},
                                    {'text': 'Climate Drivers'}, {'text': 'Date'}]}
        context['body'] = {
            'rows': [],
        }

        outputdata = OutputData.objects.order_by('-date', 'sector', 'model')
        for i, odat in enumerate(outputdata):
            drivers = [x.name for x in odat.drivers.all()]
            context['body']['rows'] += [{
                'invisible': i >= value.get('rows_per_page'),
                'cols': [
                    {'texts': [odat.sector]},
                    {'texts': [odat.model.base_model.name if odat.model else '']},
                    {'texts': [sr.name for sr in odat.simulation_round.all()]},
                    {'texts': [odat.experiments]},
                    {'texts': drivers},
                    {'texts': [odat.date]}
                ]
            }]
        numpages = math.ceil(outputdata.count() / value.get('rows_per_page'))
        context['pagination'] = {
            'rowsperpage': (value.get('rows_per_page')),
            'numberofpages': numpages,  # number of pages with current filters
            'pagenumbers': [{'number': i + 1, 'invisible': False} for i in range(numpages)],
            'activepage': 1,  # set to something between 1 and numberofpages
        }
        context['id'] = 'selectorable'
        context['tableid'] = 'selectorable'
        context['searchfield'] = {'value': ''}
        return context

    class Meta:
        icon = 'fa fa-database'
        template = 'blocks/output_data_block.html'
