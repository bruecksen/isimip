from blog.models import BlogIndexPage as _BlogIndexPage
from blog.models import BlogPage as _BlogPage
from django.db import models
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.wagtailroutablepage.models import route, RoutablePage
from wagtail.wagtailadmin.edit_handlers import *
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailforms.models import AbstractFormField, AbstractEmailForm

from isi_mip.climatemodels.blocks import InputDataBlock, OutputDataBlock, ImpactModelsBlock
from isi_mip.climatemodels.models import ImpactModel, InputData
from isi_mip.climatemodels.views import impact_model_details, impact_model_edit, input_data_details, \
    impact_model_download, impact_model_sector_edit
from isi_mip.contrib.blocks import BlogBlock, smart_truncate
from isi_mip.pages.blocks import *


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
    description = RichTextField(null=True, blank=True)
    flat = models.BooleanField(default=False, help_text='Whether or not the index page should display items as a flat list or as blocks.')

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        entries = self.blogs
        context['title'] = self.title

        context['entries'] = []
        for entry in entries:
            body = '' if entry.body.strip() == '<p><br/></p>' else entry.body
            entry_context = {
                'date': entry.date,
                'href': entry.slug,
                'description': smart_truncate(body, 300, 350),
                'title': entry.title,
                'arrow_right_link': True
            }
            try:
                rendition = entry.header_image.get_rendition('max-800x800')
                entry_context['image'] = {'url': rendition.url, 'name': entry.header_image.title}
                entry_context['description'] = smart_truncate(body, 0, 100)
            except:
                pass
            context['entries'] += [entry_context]
        return context

    def serve(self, request, *args, **kwargs):
        if self.flat:
        # if 'flat' in request.GET and request.GET['flat'] == 'True':
            self.template = 'pages/blog_index_flat_page.html'
        return super(BlogIndexPage, self).serve(request, *args, **kwargs)

    content_panels = _BlogIndexPage.content_panels + [
        RichTextFieldPanel('description'),
        FieldPanel('flat'),
    ]

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


class GenericPage(Page):
    template = 'pages/default_page.html'

    content = StreamField(BASE_BLOCKS + COLUMNS_BLOCKS)
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]


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
            ('blog', BlogBlock()),
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
                'href': link,
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


class AboutPage(Page):
    template = 'pages/default_page.html'

    content = StreamField(BASE_BLOCKS + COLUMNS_BLOCKS + [
        ('pdf', PDFBlock()),
        ('paper', PaperBlock(template='widgets/page-teaser-wide.html')),
        ('bigteaser', BigTeaserBlock()),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('content')
    ]


class GettingStartedPage(RoutablePageWithDefault):
    template = 'pages/default_page.html'
    parent_page_types = [HomePage]

    content = StreamField(COLUMNS_BLOCKS + [
        ('protocol', ProtocolBlock()),
        ('input_data', InputDataBlock()),
        ('contact', ContactsBlock()),
        ('blog', BlogBlock(template='blocks/flat_blog_block.html')),

    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]

    @route(r'^details/(?P<id>\d+)/$')
    def details(self, request, id):
        return input_data_details(self, request, id)


class ImpactModelsPage(RoutablePageWithDefault):
    template = 'pages/default_page.html'
    parent_page_types = [HomePage]

    content = StreamField([
        ('impact_models', ImpactModelsBlock()),
        ('blog', BlogBlock(template='blocks/flat_blog_block.html')),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]

    @route(r'^details/(?P<id>\d+)/$')
    def details(self, request, id):
        return impact_model_details(self, request, id)

    @route(r'edit/(?P<id>[0-9]*)/$')
    def edit(self, request, id=None):
        # return ImpactModelEdit.as_view()
        return impact_model_edit(self, request, id)

    @route(r'edit/sector/(?P<id>[0-9]*)/$')
    def edit_sector(self, request, id=None):
        return impact_model_sector_edit(self, request, id)

    @route(r'download/$')
    def download(self, request):
        return impact_model_download(self, request)

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
    template = 'pages/default_page.html'
    parent_page_types = [HomePage]

    content = StreamField([
        ('output_data', OutputDataBlock()),
        ('blog', BlogBlock(template='blocks/flat_blog_block.html')),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]


class OutcomesPage(Page):
    template = 'pages/default_page.html'

    content = StreamField([
        ('papers', PapersBlock()),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]


class FAQPage(Page):
    template = 'pages/default_page.html'
    parent_page_types = [HomePage]

    content = StreamField(COLUMNS_BLOCKS + [
        ('richtext', RichTextBlock()),
        ('faqs', FAQsBlock()),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]


class LinkListPage(Page):
    links = StreamField([
        ('link', LinkBlock()),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('links'),
    ]


class NewsletterPage(Page):
    def serve(self, request, *args, **kwargs):
        return redirect('/gettingstarted/newsletter/')
        # return render(request)


class DashboardPage(Page):
    pass


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields')


class FormPage(AbstractEmailForm):
    landing_page_template = 'pages/form_page_confirmation.html'
    subpage_types = []

    top_content = StreamField([('richtext', RichTextBlock())])
    confirmation_text = models.TextField(default='Your registration was submitted')
    bottom_content = StreamField([('richtext', RichTextBlock())])

    content_panels = AbstractEmailForm.content_panels + [
        StreamFieldPanel('top_content'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('confirmation_text', classname="full"),
        MultiFieldPanel([
            FieldPanel('to_address', classname="full"),
            FieldPanel('from_address', classname="full"),
            FieldPanel('subject', classname="full"),
        ], "Email"),
        StreamFieldPanel('bottom_content')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        message = {'tags': 'success', 'text': self.confirmation_text}
        context['confirmation_messages'] = [message]
        return context

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