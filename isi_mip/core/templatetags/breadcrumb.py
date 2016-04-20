from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag(takes_context=True)
def breadcrumb(context, page=None, **kwargs):
    page = page or context.get('page')
    if not page:
        return ''
    # depth = page.get_depth()
    # if depth <= 3:
    #     return ''
    children = page.get_ancestors().live() #.in_menu().specific()
    # print(page.get_ancestors().live())
    links = []
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
    links.append({
        'text': page.title,
        # 'href': page.url,
        # 'active': True,
    })
    context.update(kwargs)
    template = 'widgets/breadcrumb.html'
    return render_to_string(template, context=context)
