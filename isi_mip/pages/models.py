import csv

from django.http.response import HttpResponse
from django.template.response import TemplateResponse
from icalendar import Event, vText
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.wagtailroutablepage.models import route, RoutablePage
from wagtail.wagtailadmin.edit_handlers import *
from wagtail.wagtailcore.blocks.field_block import TextBlock
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailforms.models import AbstractFormField, AbstractEmailForm
from wagtail.wagtailimages.blocks import ImageChooserBlock
# from wagtailcaptcha.models import WagtailCaptchaEmailForm


from isi_mip.climatemodels.blocks import InputDataBlock, OutputDataBlock, ImpactModelsBlock
from isi_mip.climatemodels.models import ImpactModel
from isi_mip.contrib.blocks import BlogBlock
from isi_mip.pages.blocks import SmallTeaserBlock, PaperBlock, LinkBlock, FAQBlock, BigTeaserBlock, RowBlock, \
    IsiNumbersBlock, TwitterBlock, Columns1To1Block, ImageBlock, PDFBlock


class RoutablePageWithDefault(RoutablePage):
    @route(r'^$')
    def base(self, request):
        return TemplateResponse(
            request,
            self.get_template(request),
            self.get_context(request)
        )

    class Meta:
        abstract = True


class HomePage(Page):
    parent_page_types = ['wagtailcore.Page']

    teaser_title = models.CharField(max_length=500)
    teaser_text = RichTextField()
    teaser_link_external = models.URLField("External link", blank=True,
                                           help_text="Will be ignored if an internal link is provided")
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
        ('row', RowBlock([
            ('teaser',SmallTeaserBlock()),
            ('bigteaser', BigTeaserBlock()),
            ('news', BlogBlock()),
            ('numbers', IsiNumbersBlock()),
            ('twitter', TwitterBlock()),
            ])
        )
    ])

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('teaser_title'),
            RichTextFieldPanel('teaser_text'),
            MultiFieldPanel([
                FieldPanel('teaser_link_external'),
                PageChooserPanel('teaser_link_internal'),

            ]),
        ], heading='Teaser'),
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
    #
    # @route(r'^ical/$')
    # def ical(self, request):
    #     filename = "event.ics"
    #     from datetime import datetime
    #     event = Event()
    #     event.add('summary', 'Python meeting about calendaring')
    #     event.add('dtstart', datetime(2005, 4, 4, 10, 0, 0))
    #     event['location'] = vText('Odense, Denmark')
    #     response = HttpResponse(event.to_ical(), content_type='text/calendar')
    #     response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    #     return response


class AbstractRegisterFormPage(AbstractEmailForm):
    parent_page_types = [HomePage]
    subpage_types = []

    # template = 'pages/contact_page.html'
    landing_page_template = 'pages/contact_page_confirmation.html'

    confirmation_text = models.TextField(default='Your registration was submitted')

    content_panels = AbstractEmailForm.content_panels + [
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('confirmation_text', classname="full"),
        MultiFieldPanel([
            FieldPanel('to_address', classname="full"),
            FieldPanel('from_address', classname="full"),
            FieldPanel('subject', classname="full"),
        ], "Email")
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        message = {'tags': 'success', 'text': self.confirmation_text}
        context['confirmation_messages'] = [message]
        return context

    class Meta:
        abstract = True


class RegisterFormField(AbstractFormField):
    page = ParentalKey('AboutPage', related_name='form_fields')


class AboutPage(AbstractRegisterFormPage):
    top_content = StreamField([
        ('columns_1_to_1', Columns1To1Block()),
        ('image', ImageBlock()),
        ('pdf', PDFBlock())
    ])
    bottom_content = StreamField([
        ('columns_1_to_1', Columns1To1Block()),
        ('image', ImageBlock()),
        ('pdf', PDFBlock())
    ])

    content_panels = [StreamFieldPanel('top_content')] + AbstractRegisterFormPage.content_panels + \
                     [StreamFieldPanel('bottom_content')]


class GettingStartedPage(Page):
    parent_page_types = [HomePage]
    content = StreamField([
        ('input_data', InputDataBlock()),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]

class ImpactModelsPage(RoutablePageWithDefault):
    parent_page_types = [HomePage]
    content = StreamField([
        ('impact_models', ImpactModelsBlock()),
        ('news', BlogBlock(template='widgets/flat_blog_block.html')),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]

    # @route(r'^csv/$')
    # def csv(self, request):
    #     # Create the HttpResponse object with the appropriate CSV header.
    #     response = HttpResponse(content_type='text/csv')
    #     response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    #
    #     writer = csv.writer(response)
    #     writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    #     writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
    #
    #     return response



class OutputDataPage(Page):
    parent_page_types = [HomePage]
    content = StreamField([
        ('output_data', OutputDataBlock()),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]


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


# Extra Pages
class NewsPage(Page):
    template = 'pages/news.html'

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['news'] = ''
        return context
