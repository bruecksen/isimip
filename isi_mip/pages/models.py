from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page

from isi_mip.climatemodels.models import General
from isi_mip.climatemodels.tables import ClimateModelTable

# class ShowInMenuMixin:
#     def __init__(self, *args, **kwargs):
#         self._meta.get_field('show_in_menus').default = True
#         super().__init__(*args, **kwargs)


# class ImpactModelsPage(ShowInMenuMixin, Page):

import django_filters


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = General
        fields = ['sector']


class ImpactModelsPage(Page):
    description = RichTextField()
    template = 'pages/impactmodels.html'

    content_panels = Page.content_panels + [
        FieldPanel('description')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(ImpactModelsPage, self).get_context(request, *args, **kwargs)
        # gfilter = ProductFilter(request.GET, queryset=General.objects.all())
        # table = ClimateModelTable(gfilter)
        # table.paginate(page=request.GET.get('page', 1), per_page=4)
        # RequestConfig(request).configure(table)
        # template = "climatemodels/list.html"
        # context = {"table": table}
        context['general'] = General.objects.all() #values('name', 'sector', 'contact_person')
        # context['table'] = table
        # context['filter'] = gfilter
        return context

    class Meta:
        verbose_name = "Impact Models"
        # parent_page_types = []
        # subpage_types = ['tours.Tour']
