from collections import OrderedDict
from django import template
from django.forms import BaseForm
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe, mark_for_escaping

from isi_mip.climatemodels.widgets import MyTextInput, MyMultiSelect, MyBooleanSelect

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
        context = {'error': field.errors,
                   'help': field.help_text,
                   'id': field.name,
                   'label': field.label,
                   # 'type': field.field.widget.input_type,
                   #'type': 'number', # email, password
                   'value': field.value,
                   'required': field.field.required,
                   }
        context['readonly'] = 'readonly' in field.field.widget.attrs and field.field.widget.attrs['readonly']

        if isinstance(field.field.widget, MyTextInput):
            template = 'widgets/textinput.html'
        elif isinstance(field.field.widget, MyBooleanSelect):
            context['nullable'] = field.field.widget.nullable
            template = 'widgets/nullboolean.html'
        elif isinstance(field.field.widget, MyMultiSelect):
            context.update({
                'allowcustom': field.field.widget.allowcustom,
                'singleselect': not field.field.widget.multiselect,
                'options': []
            })
            value = field.value()
            for k, v in field.field.choices:
                if isinstance(value, list):
                    checked = str(k) in [str(x) for x in value]
                else:
                    checked = k == value
                if v == '---------' and not k:
                    continue
                context['options'] += [{'checked': checked, 'label': v, 'value': k}]

            if not any(opt['checked'] for opt in context['options']) and value:
                context['options'] += [{'checked': True, 'label': value, 'value': value}]

            template = 'widgets/multiselect.html'
        else:
            try:
                context['type'] = field.field.widget.input_type
            except:
                pass
            template = 'widgets/formfield.html'
        string = render_to_string(template, context)
        newform[field.name] = string
    return newform
