from blog.models import BlogPage, BlogCategory, BlogIndexPage
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils.functional import cached_property
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.blocks import FieldBlock, PageChooserBlock
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock


def smart_truncate(text: str, min_length: int, max_length: int) -> str:
    """
    :param text:
    :param min_length: Minimal length of result string
    :param max_length: Maximal length of result string
    :return: Concattenated String
    """
    max_length = len(text) if max_length == 0 else max_length
    c_index = text.rfind('.', min_length, max_length)
    if c_index != -1:
        return text[:c_index+1]
    else:
        if len(text) > max_length:
            return text[:max_length-2]+'..'
        else:
            return text


class SpecificPageChooserBlock(PageChooserBlock):
    page_model = BlogIndexPage
    # TODO: THIS WILL ONLY WORK IF https://github.com/torchbox/wagtail/pull/2448
    # TODO: For now, the following will do:

    @cached_property
    def target_model(self):
        return self.page_model

    @cached_property
    def widget(self):
        from wagtail.wagtailadmin.widgets import AdminPageChooser
        ct = ContentType.objects.get_for_model(self.page_model)
        return AdminPageChooser(content_type=ct, can_choose_root=self.can_choose_root)


class IntegerBlock(FieldBlock):
    def __init__(self, required=True, help_text=None, **kwargs):
        self.field = forms.IntegerField(required=required, help_text=help_text)
        super().__init__(**kwargs)

class EmailBlock(FieldBlock):
    def __init__(self, required=True, help_text=None, **kwargs):
        self.field = forms.EmailField(required=required, help_text=help_text)
        super().__init__(**kwargs)


class BlogBlock(blocks.StructBlock):
    blog_index = SpecificPageChooserBlock(required=False, help_text='Select blog index page.')
    entry_count = IntegerBlock(required=True, help_text='How many blog entries should be displayed?')

    class Meta:
        classname = 'blog'
        icon = 'image'
        template = 'widgets/blog_block.html'

    def get_context(self, value):
        context = super().get_context(value)
        blog_index = value.get('blog_index')
        entry_count = value.get('entry_count')

        entries = blog_index.blogs if blog_index else BlogPage.objects.all().order_by('-date')
        entries = entries[:entry_count]
        context['teaser_template'] = 'widgets/page-teaser.html'
        context['count'] = entry_count
        context['title'] = blog_index.title if blog_index else 'Blog'
        context['slug'] = blog_index.slug if blog_index else ''
        context['outter_col'] = int(3 * entry_count)
        context['inner_col'] = int(12 / entry_count)

        context['entries'] = []
        for entry in entries:
            entry_context = {
                'date': entry.date,
                'href': entry.url,
                'text': {
                    'description': smart_truncate(entry.body,300,350),
                    'title': entry.title,
                    'arrow_right_link': True
                }
            }
            try:
                rendition = entry.header_image.get_rendition('max-800x800')
                entry_context['image'] = {'url': rendition.url, 'name': entry.header_image.title}
                entry_context['text']['description'] = smart_truncate(entry.body, 0, 100)
            except:
                pass

            context['entries'] += [entry_context]
        return context