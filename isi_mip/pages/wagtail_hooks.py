from django.conf import settings
from django.utils.html import format_html_join
from wagtail.wagtailcore import hooks

from isi_mip.climatemodels.models import ImpactModel, InputData, OutputData
from django.utils.safestring import mark_safe


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
def add_wagtail_icon_items(request, items):
    items.append(DjangoAdminLinkItem())
    items.append(LogOutLinkItem())


class ImpactModelsPanel(object):
    order = 50

    def render(self):
        impactmodels = ImpactModel.objects
        inputdata = InputData.objects
        outputdata = OutputData.objects
        output = """<section class="panel summary nice-padding">
                    <h2 class="visuallyhidden">Impact Model summary</h2>
                    <ul class="stats">
                            <li class="icon icon-cogs">
                        <a href="/admin/climatemodels/impactmodel/">
                            <span>{}</span> Impact Models
                        </a>
                    </li>
                    <li class="icon icon-order-down">
                        <a href="/admin/climatemodels/inputdata/">
                            <span>{}</span> Input Data sets
                        </a>
                    </li>
                    <li class="icon icon-order-up">
                        <a href="/admin/climatemodels/outputdata/">
                            <span>{}</span> Output Data sets
                        </a>
                    </li>
                    </ul>
                    </section>
                    """.format(impactmodels.count(), inputdata.count(), outputdata.count())

        return mark_safe(output)


@hooks.register('construct_homepage_panels')
def add_impact_models_panel(request, panels):
    return panels.append(ImpactModelsPanel())

class DjangoAdminMenuItem:
    order = 90000
    def render_html(self, request):
        output = '''<li class="menu-item">
                        <a href="/admin/" class="icon icon-pick">Django Admin</a>
                    </li>'''
        return output

@hooks.register('construct_main_menu')
def main_menu_django_admin_item(request, menu_items):
    menu_items.append(DjangoAdminMenuItem())