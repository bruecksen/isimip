from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag(takes_context=True)
def breadcrumb(context, page=None, **kwargs):
    page = page or context.get('page')
    if not page:
        return ''
    depth = page.get_depth()
    if depth <= 3:
        return ''
    children = page.get_ancestors().live().in_menu().specific()
    links = []
    for child in children:
        active = False
        links.append({
            'text': child.title,
            'url': child.url,
            'active': active,
        })
    context = {
        'links': links,
    }
    links.append({
        'text': page.title,
        'url': page.url,
        'active': True,
    })
    context.update(kwargs)
    template = 'widgets/breadcrumb.html'
    return render_to_string(template, context=context)
