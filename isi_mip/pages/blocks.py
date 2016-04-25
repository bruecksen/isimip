from django.utils import formats
from wagtail.wagtailcore.blocks import CharBlock, StructBlock, TextBlock, StreamBlock, PageChooserBlock, RichTextBlock, \
    URLBlock, DateBlock, ListBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock

from isi_mip.contrib.blocks import EmailBlock


class RowBlock(StreamBlock):
    class Meta:
        icon = 'horizontalrule'
        template = 'blocks/row_block.html'


class ImageBlock(ImageChooserBlock):
    class Meta:
        icon = 'image'
        template = 'widgets/image.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['url'] = value.get_rendition('max-1200x1200').url
        context['name'] = value.title
        return context


BASE_BLOCKS = [
    ('rich_text', RichTextBlock()),
    ('embed', EmbedBlock()),
    ('image', ImageBlock()),
]


class SmallTeaserBlock(StructBlock):
    title = CharBlock(required=True)
    picture = ImageChooserBlock()
    text = TextBlock(required=True)
    link = PageChooserBlock(required=True)

    class Meta:
        #TODO: icon = 'image'
        template = 'blocks/small_teaser_block.html'


    def get_context(self, value):
        context = super().get_context(value)
        context['title'] = value.get('title')
        image = value.get('picture')
        rendition = image.get_rendition('max-800x800')
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
        #TODO: icon = 'image'
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

        context.update({
            'title': value.get('subtitle'),
            'description': value.get('text'),
            'text_right_link': True,
            'text_right_link_text': 'Learn more',
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
    username = CharBlock(required=True, help_text='You will find username and widget_id @ https://twitter.com/settings/widgets/')
    widget_id = CharBlock(required=True)
    tweet_limit = CharBlock(required=True, max_length=2)

    class Meta:
        template = 'blocks/twitter_block.html'


class PaperBlock(StructBlock):
    picture = ImageChooserBlock(required=False)
    author = CharBlock()
    title = CharBlock()
    journal = CharBlock()
    link = URLBlock()

    class Meta:
        # icon = 'doc-full'
        template = 'widgets/page-teaser.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['author'] = value.get('author')
        context['title'] = value.get('title')
        context['description'] = value.get('journal')
        context['url'] = value.get('link')
        image = value.get('picture')
        if image:
            rendition = image.get_rendition('max-500x500')
            context['image'] = {'url': rendition.url, 'name': image.title}
        context['source'] = {'description': value.get('link'), 'href': value.get('link')}

        return context


class PapersBlock(StructBlock):
    title = CharBlock()
    description = RichTextBlock(required=False)
    papers = ListBlock(PaperBlock)
    class Meta:
        template = 'blocks/outcomes_block.html'


class LinkBlock(StructBlock):
    title = CharBlock(required=True)
    picture = ImageChooserBlock(required=False)
    text = RichTextBlock(required=False)
    link = URLBlock(required=False)

    class Meta:
        classname = 'link'
        #TODO: icon = 'image'
        template = 'widgets/page-teaser-wide.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['arrow_right_link'] = True
        context['title'] = value.get('title')
        context['description'] = value.get('text')

        image = value.get('picture')
        if image:
            rendition = image.get_rendition('max-250x250')
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
    description = RichTextBlock()
    sectors = ListBlock(SectorBlock)
    class Meta:
        template = 'blocks/contacts_block.html'
    def get_context(self, value):
        context = super().get_context(value)
        context['sectors'] = []
        for sector in value.get('sectors'):
            sector_dict = {'name': sector.get('name'),
                           'text': ""
                           }
            for contact in sector.get('contacts'):
                n,w,e = contact.get('name'), contact.get('website'), contact.get('email')
                sector_dict['text'] += "{n}<br/><a target='_blank' href='{w}'>Homepage</a><br/>" \
                                              "<a target='_blank' href='mailto:{e}'>{e}</a><br/><br/>".format(n=n,w=w,e=e)
            try:
                sector_dict['image'] = {
                    'url': sector.get('image').get_rendition('max-1200x1200').url,
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
        image = ''
        template = 'widgets/download-link.html'


#     def render_basic(self, value):
#         ret = super().render_basic(value)
#         if ret:
#             ret = 'PDF' + ret
#         return ret



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
    right_column = StreamBlock(_COLUMNS_BLOCKS) #, form_classname='pull-right')

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

