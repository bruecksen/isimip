from blog.models import BlogPage, BlogCategory
from django import forms
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.blocks import FieldBlock
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock


class IntegerBlock(FieldBlock):
    def __init__(self, required=True, help_text=None, **kwargs):
        self.field = forms.IntegerField(required=required, help_text=help_text)
        super().__init__(**kwargs)


class BlogBlock(blocks.StructBlock):
    blog_category = SnippetChooserBlock(target_model=BlogCategory, required=False, help_text='Filter blog by this category')
    entry_count = IntegerBlock(required=False, help_text='How many blog entries should be displayed?')

    class Meta:
        classname = 'blog'
        icon = 'image'
        template = 'widgets/blogblock.html'

    def get_context(self, value):
        context = super().get_context(value)
        blog_category = value.get('blog_category')
        entry_count = value.get('entry_count')
        entries = BlogPage.objects.all().order_by('-date')
        if blog_category:
            entries = entries.filter(categories__category=blog_category)
        if entry_count is not None:
            entries = entries[:entry_count]
        context['entries'] = entries
        return context
        # context['entries'] = []
        # for entry in entries:
        #     # context['entries'].append(entry)
        #     if entry.header_image:
        #         rendition = entry.header_image.get_rendition('max-1200x1200')
        #         entry['image_url'] = rendition.url
        #         entry['image_name'] = entry.header_image.title
        #     context['entries'].append(entry)
