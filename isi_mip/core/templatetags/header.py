from django import template
from django.template.loader import render_to_string

from isi_mip.core.models import HeaderLinks
register = template.Library()


@register.simple_tag(takes_context=True)
def header(context, **kwargs):
    request = context['request']
    settings = HeaderLinks.for_site(request.site)

    page = context.get('page')
    current_parent_page = page and page.get_parent() or None
    links = []
    for link in settings.header_links.all():
        name = link.name
        target = link.target.specific
        if page and target == page:
            active = True
        elif current_parent_page and current_parent_page.specific == target:
            active = True
        else:
            active = False
        children = []
        for child in link.menu_items:
            if child.block_type == 'jump_link':
                children.append({'url': child.value.get('link'), 'text': child.value.get('name'), 'is_anchor': True})
            elif child.block_type == 'page_link':
                child_page = child.value.get('page')
                children.append({'url': child_page.url, 'text': child.value.get('name'), 'active': child_page.specific == page})
        if target.url:
            links.append({'url': target.url, 'text': name, 'active': active, 'children': children})

    context = {
        'links': links
    }
    template = 'widgets/header.html'
    return render_to_string(template, context=context)
