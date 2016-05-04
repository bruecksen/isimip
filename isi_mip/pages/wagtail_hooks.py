from django.conf import settings
from django.utils.html import format_html_join
from wagtail.wagtailcore import hooks


@hooks.register('insert_editor_css')
def editor_css():
    # Add extra CSS files to the admin like font-awesome
    css_files = [
        'vendor/css/font-awesome.min.css',
        'css/wagtail-font-awesome.css'
    ]

    css_includes = format_html_join(
        '\n',
        '<link rel="stylesheet" href="{0}{1}">',
        ((settings.STATIC_URL, filename) for filename in css_files))

    return css_includes


class DjangoAdminLinkItem:
    def render(self, request):
        return '''<div class="wagtail-userbar__item ">
                    <div class="wagtail-action wagtail-icon wagtail-icon-pick">
                        <a href="/admin/" target="_parent">Djang Admin</a>
                    </div>
                </div>'''

class LogOutLinkItem:
    def render(self, request):
        return '''<div class="wagtail-userbar__item ">
            <div class="wagtail-action wagtail-icon">
                <a href="/auth/logout/?next=/" target="_parent">Logout</a>
            </div>
        </div>'''

@hooks.register('construct_wagtail_userbar')
def add_puppy_link_item(request, items):
    items.append(DjangoAdminLinkItem())
    items.append(LogOutLinkItem())