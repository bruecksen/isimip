from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock


class SmallTeaserBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    picture = ImageChooserBlock()
    text = blocks.TextBlock(required=True)
    link = blocks.PageChooserBlock(required=True)

    class Meta:
        classname = 'small teaser'
        icon = 'image'
        template = 'widgets/smallteaser.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['title'] = value.get('title')
        image = value.get('picture')
        rendition = image.get_rendition('max-1200x1200')
        context['image'] = {'url': rendition.url, 'name': image.title}
        context['text'] = value.get('text')
        context['url'] = value.get('link').url
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