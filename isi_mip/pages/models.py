from django.db import models
from modelcluster.models import ClusterableModel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, PageChooserPanel, RichTextFieldPanel, \
    FieldRowPanel
from wagtail.wagtailcore.blocks import RichTextBlock, ListBlock, CharBlock
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page, Orderable

from isi_mip.climatemodels.models import ImpactModel
from isi_mip.contrib.blocks import BlogBlock
from isi_mip.pages.blocks import SmallTeaserBlock, PaperBlock, LinkBlock, FAQBlock, BigTeaserBlock

BASE_BLOCKS = [
    ('rich_text', RichTextBlock()),
]


class HomePage(Page):
    # parent_page_types = ['wagtailcore.Page']
    teaser_title = models.CharField(max_length=500)
    teaser_text = RichTextField()
    teaser_link_external = models.URLField("External link", blank=True, help_text="Will be ignored if an internal link is provided")
    teaser_link_internal = models.ForeignKey(
        'wagtailcore.Page',
        verbose_name="Or internal link",
        help_text='If set, this has precedence over the external link.',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content = StreamField([
        ('teasers', ListBlock(SmallTeaserBlock(), template='widgets/listblock.html')),
        ('bigteaser', BigTeaserBlock()),
        ('news', BlogBlock()),
    ])

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('teaser_title'),
            RichTextFieldPanel('teaser_text'),
            MultiFieldPanel([
                FieldPanel('teaser_link_external'),
                PageChooserPanel('teaser_link_internal'),

            ]),
        ],heading='Teaser'),
        StreamFieldPanel('content'),
    ]


    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if self.teaser_link_internal:
            link = self.teaser_link_internal.url
        else:
            link = self.teaser_link_external
        context['teaser'] = {
            'title': self.teaser_title,
            'text': self.teaser_text,
            'button': {
                'url': link,
                'text': 'Read more',
                'fontawesome': 'facebook',
            }
        }
        return context

# Header Pages
class AboutPage(Page):
    pass


class GettingStartedPage(Page):
    pass


class ImpactModelsPage(Page):
    description = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('description')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(ImpactModelsPage, self).get_context(request, *args, **kwargs)
        context['general'] = ImpactModel.objects.all()
        return context

    class Meta:
        verbose_name = "Impact Models"


class OutputDataPage(Page):
    pass


class OutcomesPage(Page):
    papers = StreamField([
        ('paper', PaperBlock()),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('papers'),
    ]


class FAQPage(Page):
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


# Footer Pages
class LinkListPage(Page):
    links = StreamField([
        ('link', LinkBlock()),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('links'),
    ]


class NewsletterPage(Page):
    pass


class DashboardPage(Page):
    pass


class ContactPage(Page):
    pass


# Extra Pages
class NewsPage(Page):
    template = 'pages/news.html'

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['news'] = ''
        return context
