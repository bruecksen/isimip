from django.utils import formats
from wagtail.wagtailcore.blocks import CharBlock, StructBlock, TextBlock, StreamBlock, PageChooserBlock, RichTextBlock, \
    URLBlock, DateBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock


class RowBlock(StreamBlock):
    class Meta:
        icon = 'horizontalrule'
        template = 'wrapper/row_block.html'


class ImageBlock(ImageChooserBlock):
    class Meta:
        icon = 'image'
        template = 'widgets/image.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['url'] = value.get_rendition('max-1200x1200').url
        context['name'] = value.title
        return context


class SmallTeaserBlock(StructBlock):
    title = CharBlock(required=True)
    picture = ImageChooserBlock()
    text = TextBlock(required=True)
    link = PageChooserBlock(required=True)

    class Meta:
        #TODO: icon = 'image'
        template = 'widgets/small_teaser_block.html'


    def get_context(self, value):
        context = super().get_context(value)
        context['title'] = value.get('title')
        image = value.get('picture')
        rendition = image.get_rendition('max-800x800')
        context['image'] = {'url': rendition.url, 'name': image.title}
        context['href'] = value.get('link').url
        context['text'] = {
            'description': value.get('text'),
            'arrow_right_link': True
        }
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
        template = 'widgets/bigteaser.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['title'] = value.get('title')

        image = value.get('picture')
        rendition = image.get_rendition('fill-1920x640-c100')
        context['image'] = {'url': rendition.url, 'name': image.title}
        if value.get('internal_link'):
            context['href'] = value.get('internal_link').url
        else:
            context['href'] = value.get('external_link')
        context['text'] = {
            'title': value.get('subtitle'),
            'description': value.get('text'),
            'text_right_link': True,
            'text_right_link_text': 'Learn more',
            'divider': True,
            'date': "%s to %s" % (formats.date_format(value.get('from_date'), "SHORT_DATE_FORMAT"),
                                  formats.date_format(value.get('to_date'), "SHORT_DATE_FORMAT")),
        }
        context['wideimage'] = True
        return context


class IsiNumbersBlock(StructBlock):
    number1 = CharBlock()
    number2 = CharBlock()
    class Meta:
        icon = 'form'
        template = 'wrapper/isi_numbers_block.html'


class TwitterBlock(StructBlock):
    username = CharBlock(required=True, help_text='You will find username and widget_id @ https://twitter.com/settings/widgets/')
    widget_id = CharBlock(required=True)
    tweet_limit = CharBlock(required=True, max_length=2)

    class Meta:
        template = 'widgets/twitter_block.html'

############### ABOUT



class PaperBlock(StructBlock):
    picture = ImageChooserBlock(required=False)
    author = CharBlock()
    link = URLBlock()
    journal = CharBlock()

    class Meta:
        classname = 'paper'
        icon = 'doc-full'
        template = 'widgets/paper.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['author'] = value.get('author')
        context['journal'] = value.get('journal')
        context['url'] = value.get('link')
        image = value.get('picture')
        rendition = image.get_rendition('max-1200x1200')
        context['image'] = {'url': rendition.url, 'name': image.title}
        return context


class LinkBlock(StructBlock):
    title = CharBlock(required=True)
    picture = ImageChooserBlock(required=False)
    text = RichTextBlock(required=False)
    link = URLBlock(required=False)

    class Meta:
        classname = 'link'
        #TODO: icon = 'image'
        template = 'widgets/link.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['title'] = value.get('title')
        image = value.get('picture')
        if image:
            rendition = image.get_rendition('max-1200x1200')
            context['image'] = {'url': rendition.url, 'name': image.title}
        context['text'] = value.get('text')
        if value.get('link'):
            context['url'] = value.get('link').url
        return context


class FAQBlock(StructBlock):
    question = CharBlock()
    answer = TextBlock()


BASE_BLOCKS = [
    ('rich_text', RichTextBlock()),
]

CONTENT_BLOCKS = BASE_BLOCKS + [
    ('link', LinkBlock()),
    ('embed', EmbedBlock()),
]

class ColumnsBlock(StructBlock):
    left_column = StreamBlock(CONTENT_BLOCKS)
    right_column = StreamBlock(CONTENT_BLOCKS, form_classname='pull-right')

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