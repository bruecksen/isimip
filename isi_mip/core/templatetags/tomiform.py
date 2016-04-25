from django import template
from django.forms import BoundField
from django.template.loader import render_to_string


register = template.Library()


@register.simple_tag(takes_context=True)
def multiselect(context, field, **kwargs):
    assert isinstance(field, BoundField)
    # request = context['request']
    #
    # page = context.get('page')
    import ipdb; ipdb.set_trace()
    blabla = {'allowcustom': True,
              'id': 'singleselect',
              'label': field.value(),
              'options': [{'checked': False, 'label': 'Alt', 'value': 'alt'},
                          {'checked': False, 'label': 'Neu', 'value': 'neu'},
                          {'checked': False, 'label': 'Von gestern', 'value': 'von gestern'},
                          {'checked': True, 'label': 'neu 2016', 'value': 'neu 2016'}],
              'singleselect': True}
    context.update(blabla)
    context.update(kwargs)
    template = 'widgets/multiselect.html'
    return render_to_string(template, context=context)
