from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag(takes_context=True)
def breadcrumb(context, page=None, subpage=None, **kwargs):
    page = page or context.get('page')
    subpage = subpage or context.get('subpage')
    if not page:
        return ''
    links = []

    children = page.get_ancestors().live()
    for child in children[1:]:
        active = False
        links.append({
            'text': child.title,
            'href': child.url,
            'active': active,
        })
    context = {
        'links': links,
    }

    if not subpage:
        links.append({
            'text': page.title,
        })

    else:
        links.append({
            'text': page.title,
            'href': page.url,
            'active': True,
        })
        links.append({
            'text': subpage.title,
        })
    context.update(kwargs)
    template = 'widgets/breadcrumb.html'
    return render_to_string(template, context=context)
