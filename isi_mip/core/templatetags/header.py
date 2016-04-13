from django import template
from django.template.loader import render_to_string

from isi_mip.core.models import HeaderLinks
register = template.Library()


@register.simple_tag(takes_context=True)
def header(context, **kwargs):
    request = context['request']
    settings = HeaderLinks.for_site(request.site)

    page = context.get('page')

    links = []
    for link in settings.header_links.all():
        name = link.name
        target = link.target.specific
        if page and target == page:
            active = True
        else:
            active = False
        links.append({'url': target.url, 'text': name, 'active': active})

    context['links'] = links
    context.update(kwargs)
    template = 'widgets/header.html'
    return render_to_string(template, context=context)