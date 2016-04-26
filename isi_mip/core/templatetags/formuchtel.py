from django import template
from django.forms import BaseForm
from django.template.loader import render_to_string

register = template.Library()


@register.assignment_tag(takes_context=True)
def nussform(context, form, **kwargs):
    assert isinstance(form, BaseForm)
    newform = {}
    for field in form:
        template ='widgets/formfeld.html'
        newform[field.name] = render_to_string(template, {'field': field})
    return newform