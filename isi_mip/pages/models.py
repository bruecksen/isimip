from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page

from isi_mip.climatemodels.models import General


class ImpactModelsPage(Page):
    description = RichTextField()
    template = 'pages/impactmodels.html'

    content_panels = Page.content_panels + [
        FieldPanel('description')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(ImpactModelsPage, self).get_context(request, *args, **kwargs)
        context['general'] = General.objects.all()
        return context

    class Meta:
        verbose_name = "Impact Models"