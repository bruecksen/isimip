from collections import OrderedDict
from django import template
from django.forms import BaseForm
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe, mark_for_escaping

register = template.Library()


class SimpleStringForm(template.Node):
    def __init__(self, fields=None):
        if fields is None:
            fields = OrderedDict()
        self.fields = fields

    def __str__(self):
        output = "".join(str(field) for field in self.fields.values())
        return mark_safe(output)

    def __repr__(self):
        return mark_safe(str(self))

    def __setitem__(self, key, value):
        self.fields[key] = value

    def __getitem__(self, item):
        return self.fields[item]

    def __iter__(self):
        return self.fields.values().__iter__()

@register.assignment_tag
def template_form(form, **kwargs):
    assert isinstance(form, BaseForm)
    newform = SimpleStringForm()
    for field in form:
        template = 'widgets/formfeld.html'
        string = render_to_string(template, {'field': field})
        newform[field.name] = string
    return newform
