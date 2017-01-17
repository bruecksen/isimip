from blog.models import BlogIndexPage as _BlogIndexPage
from blog.models import BlogPage as _BlogPage
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import models
from django.http.response import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.text import slugify
from modelcluster.fields import ParentalKey
from wagtail.contrib.wagtailroutablepage.models import route, RoutablePageMixin
from wagtail.wagtailadmin.edit_handlers import *
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailforms.models import AbstractFormField, AbstractEmailForm

from isi_mip.climatemodels.blocks import InputDataBlock, OutputDataBlock, ImpactModelsBlock
from isi_mip.climatemodels.models import ImpactModel, BaseImpactModel
from isi_mip.climatemodels.views import impact_model_details, impact_model_edit, input_data_details, \
    impact_model_download, impact_model_sector_edit, STEP_BASE, STEP_DETAIL, STEP_TECHNICAL_INFORMATION, STEP_INPUT_DATA, STEP_OTHER, STEP_SECTOR
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

    content_panels = _BlogIndexPage.content_panels + [
        RichTextFieldPanel('description'),
    ]
    settings_panels = Page.settings_panels + [
        FieldPanel('flat'),
    ]

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
                rendition = entry.header_image.get_rendition('fill-640x360-c100')
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


class TOCPage(Page):
    show_toc = models.BooleanField(default=False, help_text='Show Table of Contents')

    settings_panels = Page.settings_panels + [
        FieldPanel('show_toc'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if self.show_toc:
            context['toc'] = []
            for block in self.content:
                if block.block_type == 'heading':
                    link = "#"+slugify(block.value, allow_unicode=True)
                    context['toc'] += [{'href': link, 'text': block.value}]
        return context

    class Meta:
        abstract = True


class RoutablePageWithDefault(RoutablePageMixin, TOCPage):
    @route(r'^$')
    def base(self, request):
        return TemplateResponse(
            request,
            self.get_template(request),
            self.get_context(request)
        )

    class Meta:
        abstract = True


class GenericPage(TOCPage):
    template = 'pages/default_page.html'
    content = StreamField(BASE_BLOCKS + COLUMNS_BLOCKS)
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]


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
        context['noborder'] = True
        return context


class AboutPage(TOCPage):
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
    parent_page_types = [HomePage, 'GettingStartedPage']

    content = StreamField(BASE_BLOCKS + COLUMNS_BLOCKS + [
        ('protocol', ProtocolBlock()),
        ('input_data', InputDataBlock()),
        ('contact', ContactsBlock()),
        ('blog', BlogBlock(template='blocks/flat_blog_block.html')),

    ])
    input_data_description = RichTextField(null=True, blank=True, verbose_name='Input Data Details Description')

    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]
    details_content_panels = [
        RichTextFieldPanel('input_data_description'),
    ]
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(details_content_panels, heading='Input Data Details'),
        ObjectList(RoutablePageWithDefault.promote_panels, heading='Promote'),
        ObjectList(RoutablePageWithDefault.settings_panels, heading='Settings', classname="settings"),
    ])

    @route(r'^details/(?P<id>\d+)/$')
    def details(self, request, id):
        return input_data_details(self, request, id)


class ImpactModelsPage(RoutablePageWithDefault):
    template = 'pages/default_page.html'
    parent_page_types = [HomePage]

    content = StreamField(BASE_BLOCKS + COLUMNS_BLOCKS + [
        ('impact_models', ImpactModelsBlock()),
        ('blog', BlogBlock(template='blocks/flat_blog_block.html')),
    ])
    private_model_message = models.TextField()
    common_attributes_text = models.TextField()

    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]
    settings_panels = RoutablePageWithDefault.settings_panels + [
        FieldPanel('private_model_message'),
        FieldPanel('common_attributes_text'),
    ]

    @route(r'^details/(?P<id>\d+)/$')
    def details(self, request, id):
        return impact_model_details(self, request, id)

    @route(r'edit/(?P<id>[0-9]*)/$')
    def edit_base(self, request, id=None):
        return impact_model_edit(self, request, id, STEP_BASE)

    @route(r'edit/detail/(?P<id>[0-9]*)/$')
    def edit_detail(self, request, id=None):
        return impact_model_edit(self, request, id, STEP_DETAIL)

    @route(r'edit/technical-information/(?P<id>[0-9]*)/$')
    def edit_technical_information(self, request, id=None):
        return impact_model_edit(self, request, id, STEP_TECHNICAL_INFORMATION)

    @route(r'edit/input-data/(?P<id>[0-9]*)/$')
    def edit_input_data(self, request, id=None):
        return impact_model_edit(self, request, id, STEP_INPUT_DATA)

    @route(r'edit/other/(?P<id>[0-9]*)/$')
    def edit_other(self, request, id=None):
        return impact_model_edit(self, request, id, STEP_OTHER)

    @route(r'edit/sector/(?P<id>[0-9]*)/$')
    def edit_sector(self, request, id=None):
        return impact_model_edit(self, request, id, STEP_SECTOR)

    @route(r'download/$')
    def download(self, request):
        return impact_model_download(self, request)


class OutputDataPage(TOCPage):
    template = 'pages/default_page.html'
    parent_page_types = [HomePage]

    content = StreamField(BASE_BLOCKS + COLUMNS_BLOCKS + [
        ('output_data', OutputDataBlock()),
        ('blog', BlogBlock(template='blocks/flat_blog_block.html')),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]


class OutcomesPage(TOCPage):
    template = 'pages/default_page.html'

    content = StreamField(BASE_BLOCKS + COLUMNS_BLOCKS + [
        ('papers', PapersBlock()),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]


class FAQPage(TOCPage):
    template = 'pages/default_page.html'
    parent_page_types = [HomePage]

    content = StreamField(BASE_BLOCKS + COLUMNS_BLOCKS + [
        ('faqs', FAQsBlock()),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]


class LinkListPage(TOCPage):
    template = 'pages/default_page.html'

    content = StreamField(BASE_BLOCKS + [
        ('links', ListBlock(LinkBlock(), template='blocks/link_list_block.html', icon='fa fa-list-ul')),
        ('supporters', SupportersBlock())
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]


class DashboardPage(Page):
    impact_models_description = RichTextField(null=True,blank=True)
    content_panels = Page.content_panels + [
        RichTextFieldPanel('impact_models_description'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        base_impact_models = BaseImpactModel.objects.filter(owners=request.user).order_by('name')
        impage = ImpactModelsPage.objects.get()
        impage_details = lambda imid: "<a href='{0}'>{{0}}</a>".format(
            impage.url + impage.reverse_subpage('details', args=(imid, )))
        impage_edit = lambda imid: "<a href='{0}'>{{0}}</a>".format(
            impage.url + impage.reverse_subpage('edit', args=(imid,)))
        context['head'] = {
            'cols': [{'text': 'Model'}, {'text': 'Simulation round'}, {'text': 'Sector'}, {'text': 'Edit'}, {'text': 'Public'}]
        }

        bodyrows = []
        for bims in base_impact_models:
            for imodel in bims.impact_model.all():
                values = [
                    [impage_details(imodel.id).format(bims.name)],
                    [imodel.simulation_round.name],
                    [bims.sector],
                    [impage_edit(imodel.id).format("<i class='fa fa-edit'></i>")],
                    ['<i class="fa fa-{}" aria-hidden="true"></i>'.format('check' if imodel.public else 'times')],
                ]
                row = {
                    'cols': [{'texts': x} for x in values],
                }
                bodyrows.append(row)
        context['body'] = {'rows': bodyrows}
        return context

    def serve(self, request, *args, **kwargs):
        request.is_preview = getattr(request, 'is_preview', False)
        if not request.user.is_authenticated():
            messages.info(request, 'This is a restricted area. To proceed you need to log in.')
            return HttpResponseRedirect(reverse('login'))

        context = self.get_context(request, *args, **kwargs)
        template = self.get_template(request, *args, **kwargs)

        return TemplateResponse(request, template, context)


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields')


class FormPage(AbstractEmailForm):
    landing_page_template = 'pages/form_page_confirmation.html'
    subpage_types = []

    top_content = StreamField(BASE_BLOCKS + COLUMNS_BLOCKS)
    confirmation_text = models.TextField(default='Your registration was submitted')
    bottom_content = StreamField(BASE_BLOCKS + COLUMNS_BLOCKS)

    button_name = models.CharField(max_length=500, verbose_name='Button name', default='Submit')

    content_panels = AbstractEmailForm.content_panels + [
        StreamFieldPanel('top_content'),
        StreamFieldPanel('bottom_content')
    ]
    form_content_panels = [
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('button_name'),
        FieldPanel('confirmation_text', classname="full"),
        MultiFieldPanel([
            FieldPanel('to_address', classname="full"),
            FieldPanel('from_address', classname="full"),
            FieldPanel('subject', classname="full"),
        ], "Email"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(form_content_panels, heading='Form Builder'),
        ObjectList(AbstractEmailForm.promote_panels, heading='Promote'),
        ObjectList(AbstractEmailForm.settings_panels, heading='Settings', classname="settings"),
    ])

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