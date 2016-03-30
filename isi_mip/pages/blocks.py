from django.utils import formats
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock

# class MissionStatementTeaserBlock(blocks.StructBlock):
#     title = blocks.CharBlock(required=True)
#     text = blocks.TextBlock(required=True)
#     link = blocks.PageChooserBlock(required=True)
#
#     class Meta:
#         template = 'widgets/head-super.html'
#
#     def get_context(self, value):
#         context = super().get_context(value)
#         context['button'] = {
#             'url': value.get('link'),
#             'text': 'Read more',
#             'fontawesome': 'facebook',
#         }
#         return context

class SmallTeaserBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    picture = ImageChooserBlock()
    text = blocks.TextBlock(required=True)
    link = blocks.PageChooserBlock(required=True)

    class Meta:
        icon = 'image'
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

class BigTeaserBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    subtitle = blocks.CharBlock(required=False)
    picture = ImageChooserBlock()
    text = blocks.RichTextBlock()
    link = blocks.PageChooserBlock(required=True)
    from_date = blocks.DateBlock(required=False)
    to_date = blocks.DateBlock(required=False)

    class Meta:
        icon = 'image'
        template = 'widgets/bigteaser.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['title'] = value.get('title')

        image = value.get('picture')
        rendition = image.get_rendition('fill-1920x640-c100')
        context['image'] = {'url': rendition.url, 'name': image.title}
        context['href'] = value.get('link').url
        context['text'] = {
            'title': value.get('subtitle'),
            'description': value.get('text'),
            'text_right_link': True,
            'text_right_link_text': 'Learn more',
            'divider': True,
            'date': "%s to %s" % (formats.date_format(value.get('from_date'), "SHORT_DATE_FORMAT"),
                                  formats.date_format(value.get('to_date'), "SHORT_DATE_FORMAT")),
        }
        return context


class PaperBlock(blocks.StructBlock):
    picture = ImageChooserBlock(required=False)
    author = blocks.CharBlock()
    link = blocks.URLBlock()
    journal = blocks.CharBlock()

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


class LinkBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    picture = ImageChooserBlock(required=False)
    text = blocks.RichTextBlock(required=False)
    link = blocks.URLBlock(required=False)

    class Meta:
        classname = 'link'
        icon = 'image'
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


class FAQBlock(blocks.StructBlock):
    question = blocks.CharBlock()
    answer = blocks.TextBlock()

# class PDFBlock(DocumentChooserBlock):
#     class Meta:
#         image = ''
#     def render_basic(self, value):
#         ret = super().render_basic(value)
#         if ret:
#             ret = 'PDF' + ret
#         return ret