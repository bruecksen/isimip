from wagtail.wagtailcore.blocks import StructBlock
from wagtail.wagtailcore.blocks.field_block import TextBlock, RichTextBlock

from isi_mip.climatemodels.models import InputData, OutputData, ImpactModel


class ImpactModelsBlock(StructBlock):
    description = RichTextBlock()

    def get_context(self, value):
        context = super().get_context(value)
        context['general'] = ImpactModel.objects.all()
        return context

    class Meta:
        template = 'blocks/impact_models_block.html'

class InputDataBlock(StructBlock):
    description = RichTextBlock()

    def get_context(self, value):
        context = super().get_context(value)
        context['title'] = 'Input Data'

        context['head'] = {'cols': [{'text': 'Data Set'}, {'text': 'Data Type'}, {'text': 'Description'}]}
        context['body'] = {
            'rowlimit': {'buttontext': 'See all <i class="fa fa-chevron-down"></i>', 'rownumber': 3},
            'rows': []
        }

        for inputdate in InputData.objects.all():
            context['body']['rows'] += [
                {'cols': [
                    {'text': inputdate.data_set},
                    {'text': inputdate.data_type},
                    {'text': inputdate.description}]
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
            drivers = ' '.join([x.data_set for x in outputdate.drivers.all()])
            context['body']['rows'] += [
                {'cols': [
                    {'text': outputdate.sector},
                    {'text': outputdate.model},
                    {'text': outputdate.scenario},
                    {'text': drivers},
                    {'text': outputdate.date}]
                }
            ]

        return context

    class Meta:
        template = 'blocks/output_data_block.html'