from django.utils import formats
from wagtail.wagtailcore.blocks import CharBlock, StructBlock, TextBlock, StreamBlock, PageChooserBlock, \
    URLBlock, DateBlock, ListBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock

from isi_mip.contrib.blocks import EmailBlock, IntegerBlock, HeadingBlock, HRBlock, ImageBlock, RichTextBlock
from isi_mip.twitter import TwitterTimeline


class RowBlock(StreamBlock):
    class Meta:
        icon = 'horizontalrule'
        template = 'blocks/row_block.html'


BASE_BLOCKS = [
    ('heading', HeadingBlock()),
    ('rich_text', RichTextBlock()),
    ('horizontal_ruler', HRBlock()),
    ('embed', EmbedBlock()),
    ('image', ImageBlock()),
]


class SmallTeaserBlock(StructBlock):
    title = CharBlock(required=True)
    picture = ImageChooserBlock()
    text = TextBlock(required=True)
    link = PageChooserBlock(required=True)

    class Meta:
        icon = 'fa fa-list-alt'
        template = 'blocks/small_teaser_block.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['title'] = value.get('title')
        image = value.get('picture')
        rendition = image.get_rendition('fill-640x360-c100')
        context['image'] = {'url': rendition.url, 'name': image.title}
        context['href'] = value.get('link').url
        context['description'] = value.get('text')
        context['arrow_right_link'] = True
        return context


class BigTeaserBlock(StructBlock):
    title = CharBlock(required=True)
    subtitle = CharBlock(required=False)
    picture = ImageChooserBlock()
    text = RichTextBlock()
    external_link = URLBlock(required=False, help_text="Will be ignored if an internal link is provided")
    internal_link = PageChooserBlock(required=False, help_text='If set, this has precedence over the external link.')

    from_date = DateBlock(required=False)
    to_date = DateBlock(required=False)

    class Meta:
        icon = 'fa fa-list-alt'
        template = 'blocks/big_teaser_block.html'

    def __init__(self, wideimage=False, local_blocks=None, **kwargs):
        super().__init__(local_blocks=local_blocks, **kwargs)
        self.wideimage = wideimage

    def get_context(self, value):
        context = super().get_context(value)
        context['super_title'] = value.get('title')

        image = value.get('picture')
        rendition = image.get_rendition('max-800x800')
        context['image'] = {'url': rendition.url, 'name': image.title}
        if value.get('internal_link'):
            context['href'] = value.get('internal_link').url
        else:
            context['href'] = value.get('external_link')
        if context['href']:
            context['text_right_link'] = True
            context['text_right_link_text'] = 'Learn more'

        context.update({
            'title': value.get('subtitle'),
            'description': value.get('text'),
            'divider': True,
            'date': "%s to %s" % (formats.date_format(value.get('from_date'), "SHORT_DATE_FORMAT"),
                                  formats.date_format(value.get('to_date'), "SHORT_DATE_FORMAT")),
        })

        context['wideimage'] = self.wideimage
        return context


class _IsiNumberBlock(StructBlock):
    number = CharBlock()
    title = CharBlock()
    text = CharBlock()


class IsiNumbersBlock(StructBlock):
    number1 = _IsiNumberBlock()
    number2 = _IsiNumberBlock()

    class Meta:
        icon = 'form'
        template = 'blocks/isi_numbers_block.html'


class TwitterBlock(StructBlock):
    username = CharBlock(required=True)
    count = IntegerBlock(default=20)

    # help_text='You will find username and widget_id @ https://twitter.com/settings/widgets/')
    # widget_id = CharBlock(required=True)
    # tweet_limit = CharBlock(required=True, max_length=2)

    def get_context(self, value):
        context = super().get_context(value)
        twitte = TwitterTimeline(count=(value.get('count')))
        context['timeline'] = twitte.get_timeline(value.get('username'))
        context['username'] = value.get('username') #context['timeline'][0]['screen_name']
        return context

    class Meta:
        icon = 'fa fa-twitter'
        template = 'widgets/twitter.html'


class PaperBlock(StructBlock):
    picture = ImageChooserBlock(required=False)
    author = CharBlock()
    title = CharBlock()
    journal = CharBlock()
    link = URLBlock()

    class Meta:
        icon = 'fa fa-file-text'
        template = 'widgets/page-teaser.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['author'] = value.get('author')
        context['title'] = value.get('title')
        context['description'] = value.get('journal')
        context['url'] = value.get('link')
        context['border'] = True
        image = value.get('picture')
        if image:
            rendition = image.get_rendition('fill-640x360-c100')
            context['image'] = {'url': rendition.url, 'name': image.title}
        context['source'] = {'description': 'Link to paper', 'href': value.get('link')}

        return context


class PapersBlock(StructBlock):
    see_all_offset = IntegerBlock(default=8, help_text='Show "See all" after x entries.')
    papers = ListBlock(PaperBlock)

    class Meta:
        icon = 'fa fa-file-text'
        template = 'blocks/outcomes_block.html'


class LinkBlock(StructBlock):
    title = CharBlock(required=True)
    picture = ImageChooserBlock(required=False)
    text = RichTextBlock(required=False)
    link = URLBlock(required=False)
    date = DateBlock(required=False)

    class Meta:
        classname = 'link'
        icon = 'fa fa-external-link'
        template = 'widgets/page-teaser-wide.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['arrow_right_link'] = True
        context['title'] = value.get('title')
        context['description'] = value.get('text')
        context['date'] = value.get('date')

        image = value.get('picture')
        if image:
            rendition = image.get_rendition('fill-640x360-c100')
            context['image'] = {'url': rendition.url, 'name': image.title}
        if value.get('link'):
            context['href'] = value.get('link')
        return context


class FAQBlock(StructBlock):
    question = CharBlock()
    answer = RichTextBlock()


class FAQsBlock(StructBlock):
    title = CharBlock()
    faqs = ListBlock(FAQBlock())

    class Meta:
        icon = 'fa fa-medkit'
        template = 'widgets/expandable.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['headline'] = value.get('title')
        context['list'] = []
        for faq in value.get('faqs'):
            res = {'term': faq.get('question'),
                   'definitions': [{'text': faq.get('answer')}],
                   'opened': True}
            context['list'] += [res]
        return context


class ContactBlock(StructBlock):
    name = CharBlock()
    website = URLBlock()
    email = EmailBlock()


class SectorBlock(StructBlock):
    name = CharBlock()
    image = ImageBlock(required=False)
    contacts = ListBlock(ContactBlock)


class ContactsBlock(StructBlock):
    sectors = ListBlock(SectorBlock)

    class Meta:
        icon = 'fa fa-male'
        template = 'blocks/contacts_block.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['sectors'] = []
        for sector in value.get('sectors'):
            sector_dict = {'name': sector.get('name'),
                           'text': ""
                           }
            for contact in sector.get('contacts'):
                n, w, e = contact.get('name'), contact.get('website'), contact.get('email')
                sector_dict['text'] += "<p>{n} <a target='_blank' href='{w}'><i class='fa fa-external-link' aria-hidden='true'></i></a> " \
                                       "<a target='_blank' href='mailto:{e}'><i class='fa fa-envelope' aria-hidden='true'></i></a></p>".format(n=n, w=w, e=e)
            try:
                sector_dict['image'] = {
                    'url': sector.get('image').get_rendition('fill-640x360-c100').url,
                    'name': sector.get('image').title
                }
            except:
                pass

            context['sectors'] += [sector_dict]
        return context


class PDFBlock(StructBlock):
    file = DocumentChooserBlock()
    description = CharBlock()

    def get_context(self, value):
        context = super().get_context(value)
        context['button'] = {
            'text': 'Download',
            'href': value.get('file').url
        }
        context['description'] = value.get('description')
        context['fontawesome'] = 'file-pdf-o'
        return context

    class Meta:
        icon = 'fa fa-file-pdf-o'
        template = 'widgets/download-link.html'


# def render_basic(self, value):
#         ret = super().render_basic(value)
#         if ret:
#             ret = 'PDF' + ret
#         return ret


class ProtocolBlock(StructBlock):
    complete_pdf = DocumentChooserBlock(label='Complete PDF')
    pdfs = ListBlock(PDFBlock(), label='Chapter PDFs')
    image = ImageBlock()
    version = CharBlock()

    class Meta:
        icon = 'fa fa-newspaper-o'
        template = 'blocks/protocol_block.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['links'] = []
        for pdf in value.get('pdfs'):
            context['links'] += [{
                'fontawesome': 'file-pdf-o',
                'href': pdf.get('file').url,
                'text': pdf.get('description')
            }]
        try:
            rendition = value.get('image').get_rendition('max-500x500')
            context['image'] = {'url': rendition.url, 'name': value.get('image').title}
        except:
            pass
        return context


_COLUMNS_BLOCKS = BASE_BLOCKS + [
    ('small_teaser', SmallTeaserBlock()),
    ('big_teaser', BigTeaserBlock()),
    ('isinumbers', IsiNumbersBlock()),
    ('link', LinkBlock()),
    ('faqs', FAQsBlock()),
    ('pdf', PDFBlock()),
]


class ColumnsBlock(StructBlock):
    left_column = StreamBlock(_COLUMNS_BLOCKS)
    right_column = StreamBlock(_COLUMNS_BLOCKS)  # , form_classname='pull-right')

    def get_context(self, value):
        context = super().get_context(value)
        context['left_column'] = value.get('left_column')
        context['right_column'] = value.get('right_column')
        return context

    class Meta:
        icon = 'fa fa-columns'
        label = 'Columns 1-1'
        template = None


class Columns1To1Block(ColumnsBlock):
    class Meta:
        label = 'Columns 1:1'
        template = 'widgets/columns-1-1.html'


class Columns1To2Block(ColumnsBlock):
    class Meta:
        label = 'Columns 1:2'
        template = 'widgets/columns-1-2.html'


class Columns2To1Block(ColumnsBlock):
    class Meta:
        label = 'Columns 2:1'
        template = 'widgets/columns-2-1.html'


class Columns1To1To1Block(ColumnsBlock):
    center_column = StreamBlock(_COLUMNS_BLOCKS)

    class Meta:
        label = 'Columns 1:1:1'
        template = 'widgets/columns-1-1-1.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['center_column'] = value.get('center_column')
        return context


class Columns1To1To1To1Block(StructBlock):
    first_column = StreamBlock(_COLUMNS_BLOCKS)
    second_column = StreamBlock(_COLUMNS_BLOCKS)
    third_column = StreamBlock(_COLUMNS_BLOCKS)
    fourth_column = StreamBlock(_COLUMNS_BLOCKS)

    class Meta:
        icon = 'fa fa-columns'
        label = 'Columns 1:1:1:1'
        template = 'widgets/columns-1-1-1-1.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['first_column'] = value.get('first_column')
        context['second_column'] = value.get('second_column')
        context['third_column'] = value.get('third_column')
        context['fourth_column'] = value.get('fourth_column')
        return context


COLUMNS_BLOCKS = [
    ('columns_1_to_1', Columns1To1Block()),
    ('columns_1_to_2', Columns1To2Block()),
    ('columns_2_to_1', Columns2To1Block()),
    ('columns_1_to_1_to_1', Columns1To1To1Block()),
    ('columns_1_to_1_to_1_to_1', Columns1To1To1To1Block()),

]
