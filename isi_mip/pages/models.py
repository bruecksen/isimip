from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.blocks import ImageChooserBlock

from isi_mip.climatemodels.models import ImpactModel


class ContentPage(Page):
    content = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])
    content_panels = Page.content_panels + [
        FieldPanel('content'),
    ]

class ImpactModelsPage(Page):
    description = RichTextField()
    template = 'pages/impactmodels.html'

    content_panels = Page.content_panels + [
        FieldPanel('description')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(ImpactModelsPage, self).get_context(request, *args, **kwargs)
        context['general'] = ImpactModel.objects.all()
        return context

    class Meta:
        verbose_name = "Impact Models"
