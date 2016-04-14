from blog.models import BlogIndexPage as _BlogIndexPage
from blog.models import BlogPage as _BlogPage
from django.shortcuts import render
from django.template.response import TemplateResponse
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.wagtailroutablepage.models import route, RoutablePage
from wagtail.wagtailadmin.edit_handlers import *
from wagtail.wagtailcore.blocks.field_block import RichTextBlock
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailforms.models import AbstractFormField, AbstractEmailForm
# from wagtailcaptcha.models import WagtailCaptchaEmailForm


from isi_mip.climatemodels.blocks import InputDataBlock, OutputDataBlock, ImpactModelsBlock
from isi_mip.climatemodels.models import ImpactModel, InputData
from isi_mip.contrib.blocks import BlogBlock, smart_truncate
from isi_mip.pages.blocks import SmallTeaserBlock, PaperBlock, LinkBlock, BigTeaserBlock, RowBlock, \
    IsiNumbersBlock, TwitterBlock, Columns1To1Block, ImageBlock, PDFBlock, ContactsBlock, FAQsBlock, Columns1To2Block, \
    Columns2To1Block


class BlogPage(_BlogPage):
    parent_page_types = ['pages.BlogIndexPage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['blog'] = self

        try:
            rendition = self.header_image.get_rendition('max-800x800')
            context['image'] = {'url': rendition.url, 'name': self.header_image.title}
        except:
            pass

        return context


class BlogIndexPage(_BlogIndexPage):
    subpage_types = ['pages.BlogPage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        entries = self.blogs
        context['title'] = self.title

        context['entries'] = []
        for entry in entries:
            entry_context = {
                'date': entry.date,
                'href': entry.slug,
                'description': smart_truncate(entry.body, 300, 350),
                'title': entry.title,
                'arrow_right_link': True
            }
            try:
                rendition = entry.header_image.get_rendition('max-800x800')
                entry_context['image'] = {'url': rendition.url, 'name': entry.header_image.title}
                entry_context['description'] = smart_truncate(entry.body, 0, 100)
            except:
                pass

            context['entries'] += [entry_context]
        return context


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


class HomePage(RoutablePageWithDefault):
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
            ('teaser', SmallTeaserBlock()),
            ('bigteaser', BigTeaserBlock(wideimage=True)),
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

    @route(r'^blog/$')
    @route(r'^blog/(?P<slug>\w+)/$')
    def blog(self, request, slug=None):
        context = {}
        if slug:
            entries = BlogIndexPage.objects.get(slug=slug).blogs
            context['title'] = slug.title()
        else:
            entries = BlogPage.objects.all().order_by('-date')
            context['title'] = 'News'
        template = 'pages/blog_list.html'
        context['entries'] = []
        for entry in entries:
            entry_context = {
                'date': entry.date,
                'href': entry.id,
                'description': smart_truncate(entry.body, 300, 350),
                'title': entry.title,
                'arrow_right_link': True
            }
            try:
                rendition = entry.header_image.get_rendition('max-800x800')
                entry_context['image'] = {'url': rendition.url, 'name': entry.header_image.title}
                entry_context['description'] = smart_truncate(entry.body, 0, 100)
            except:
                pass

            context['entries'] += [entry_context]

        return render(request, template, context)

    @route(r'^blog/(?P<slug>\w*)/(?P<id>\d+)/$')
    def blog_detail(self, request, id, slug=None):
        template = 'pages/blog_detail.html'
        entry = BlogPage.objects.get(id=id)
        context = {'blog': entry}

        try:
            rendition = entry.header_image.get_rendition('max-800x800')
            context['image'] = {'url': rendition.url, 'name': entry.header_image.title}
        except:
            pass

        return render(request, template, context)



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


class AboutPage(Page):
    content = StreamField([
        ('columns_1_to_1', Columns1To1Block()),
        ('columns_1_to_2', Columns1To2Block()),
        ('columns_2_to_1', Columns2To1Block()),
        ('image', ImageBlock()),
        ('pdf', PDFBlock()),
        ('paper', PaperBlock(template='widgets/page-teaser-wide.html')),
        ('bigteaser', BigTeaserBlock()),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('content')
    ]

    template = 'pages/default_page.html'


class GettingStartedPage(RoutablePageWithDefault):
    template = 'pages/default_page.html'
    parent_page_types = [HomePage]
    content = StreamField([
        ('input_data', InputDataBlock()),
        ('contact', ContactsBlock()),
        ('news', BlogBlock(template='blocks/flat_blog_block.html')),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]

    @route(r'^details/(\d+)/$')
    def details(self, request, id):
        inda = InputData.objects.get(id=id)
        template = 'pages/input_data_details_page.html'
        context = {'inda': inda}
        return render(request, template, context)


class ImpactModelsPage(RoutablePageWithDefault):
    parent_page_types = [HomePage]
    content = StreamField([
        ('impact_models', ImpactModelsBlock()),
        ('news', BlogBlock(template='blocks/flat_blog_block.html')),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]

    @route(r'^details/(\d+)/$')
    def details(self, request, id):
        im = ImpactModel.objects.get(id=id)
        template = 'pages/impact_models_details_page.html'
        im_values = im.values_to_tuples()
        model_details = []
        for k, v in im_values:
            res = {'term': k,
                   # 'notoggle': True,
                   'definitions': [{'text': "<i>%s</i>: %s" % x} for x in v]
                   }
            model_details += [res]
        im_sector_values = im.fk_sector.values_to_tuples()
        for k, v in im_sector_values:
            res = {'term': k,
                   'definitions': [{'text': "<i>%s</i>: %s" % x} for x in v]
                   }
            model_details += [res]
        model_details[0]['opened'] = True
        context = {
            'headline': im.name,
            'list': model_details
        }

        return render(request, template, context)

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
    content = StreamField([
        ('columns_1_to_1', Columns1To1Block()),
        ('faqs', FAQsBlock()),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]

    template = 'pages/default_page.html'


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
    page = ParentalKey('FormPage', related_name='form_fields')


class FormPage(AbstractRegisterFormPage):
    top_content = StreamField([
        ('richtext', RichTextBlock())
    ])
    bottom_content = StreamField([
        ('richtext', RichTextBlock())
    ])

    content_panels = [StreamFieldPanel('top_content')] + AbstractRegisterFormPage.content_panels + \
                     [StreamFieldPanel('bottom_content')]