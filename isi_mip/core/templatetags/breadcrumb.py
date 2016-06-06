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
        links.append({
            'text': child.title,
            'href': child.url,
        })
    context = {
        'links': links,
    }
    links.append({
        'text': page.title,
        'href': page.url,
    })
    if subpage:
        links.append({
            'text': subpage['title'],
            'href': subpage['url'],
        })

        if 'subpage' in subpage:
            links.append({
                'text': subpage['subpage']['title'],
                'href': subpage['subpage']['url'],
            })

    links[-1]['href'] = ''
    context.update(kwargs)
    template = 'widgets/breadcrumb.html'
    return render_to_string(template, context=context)
