from modelcluster.models import ClusterableModel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore.blocks import RichTextBlock
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page, Orderable

from isi_mip.climatemodels.models import ImpactModel
from isi_mip.pages.blocks import SmallTeaserBlock, PaperBlock, LinkBlock, FAQBlock

BASE_BLOCKS = [
    ('rich_text', RichTextBlock()),
]


class HomePage(Page):
    template = 'pages/home.html'
    parent_page_types = ['wagtailcore.Page']
    teasers = StreamField([
        ('teaser', SmallTeaserBlock())
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('teasers'),
    ]


class OutcomesPage(Page):
    template = 'pages/outcomes.html'

    papers = StreamField([
        ('paper', PaperBlock()),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('papers'),
    ]


class LinkListPage(Page):
    template = 'pages/linklist.html'
    links = StreamField([
        ('link', LinkBlock()),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('links'),
    ]


class FAQPage(Page):
    template = 'pages/faq.html'
    for_modelers = StreamField([
        ('faq', FAQBlock()),
    ])
    for_researchers = StreamField([
        ('faq', FAQBlock()),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('for_modelers'),
        StreamFieldPanel('for_researchers'),
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


class NewsPage(Page):
    template = 'pages/news.html'
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['news'] = ''
        return context