from blog.models import BlogPage, BlogIndexPage
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils.functional import cached_property
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.blocks import FieldBlock, PageChooserBlock, CharBlock


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
    # THIS WILL ONLY WORK IF https://github.com/torchbox/wagtail/pull/2449
    page_model = BlogIndexPage
    # TODO: Waiting on Upstream. For now, the following will do:

    @cached_property
    def target_model(self):
        return self.page_model

    @cached_property
    def widget(self):
        from wagtail.wagtailadmin.widgets import AdminPageChooser
        ct = ContentType.objects.get_for_model(self.page_model)
        return AdminPageChooser(content_type=ct, can_choose_root=self.can_choose_root)


class IntegerBlock(FieldBlock):
    def __init__(self, required=True, help_text=None, max_value=None, min_value=None, **kwargs):
        self.field = forms.IntegerField(required=required, help_text=help_text, max_value=max_value, min_value=min_value)
        super().__init__(**kwargs)

class EmailBlock(FieldBlock):
    def __init__(self, required=True, help_text=None, **kwargs):
        self.field = forms.EmailField(required=required, help_text=help_text)
        super().__init__(**kwargs)


class BlogBlock(blocks.StructBlock):
    blog_index = SpecificPageChooserBlock(required=False, help_text='Select blog index page.')
    title = CharBlock(required=False, help_text='Per default, the title of the blog index will be used.')
    entry_count = IntegerBlock(required=True, min_value=1, max_value=5, default=4,
                               help_text='How many blog entries should be displayed?')

    class Meta:
        classname = 'blog'
        icon = 'image'
        template = 'blocks/blog_block.html'

    def get_context(self, value):
        context = super().get_context(value)
        blog_index = value.get('blog_index')
        title = value.get('title') or (blog_index.title if blog_index else 'Blog')
        entry_count = value.get('entry_count')

        entries = blog_index.blogs if blog_index else BlogPage.objects.all().order_by('-date')
        entries = entries[:entry_count]
        # context['teaser_template'] = 'widgets/page-teaser.html'
        context['count'] = entry_count
        context['title'] = title
        context['slug'] = blog_index.slug if blog_index else ''
        context['outter_col'] = int(3 * entry_count)
        context['inner_col'] = int(12 / entry_count)

        context['entries'] = []
        for entry in entries:
            entry_context = {
                'date': entry.date,
                'href': entry.url,
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