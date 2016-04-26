from itertools import chain

from django.forms.widgets import Select, TextInput, EmailInput
from django.template.loader import render_to_string
from django.utils.datastructures import MultiValueDict

class TomiTextInput(TextInput):
    def __init__(self, textarea=False, emailfield=False):
        super().__init__()
        self.textarea = textarea
        self.emailfield = emailfield

    def render(self, name, value, attrs=None):
        template = 'widgets/textarea.html' if self.textarea else 'widgets/textinput.html'
        context = {
            'id': name,
            # 'placeholder': name,
            'value': value or '',
            'readonly': 'readonly' in self.build_attrs() and self.build_attrs()['readonly']
        }
        if self.emailfield:
            context['type'] = 'email'
        return render_to_string(template, context)

class NullBooleanSelect(Select):
    def render(self, name, value, attrs=None, choices=()):
        template = 'widgets/nullboolean.html'
        context = {'id': name,
                   # 'label': 'Hollywood hat alle Apollo-Missionen auf dem Mond gedreht',
                   'value': value}
        return render_to_string(template, context)


class MultiSelect(Select):
    # allow_multiple_selected = True

    def __init__(self, allowcustom=False, multiselect=False, attrs=None):
        super().__init__(attrs)
        self.allowcustom = allowcustom
        self.multiselect = multiselect
        self.allow_multiple_selected = multiselect

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        template = 'widgets/multiselect.html'
        context = {'allowcustom': self.allowcustom,
                   'singleselect': not self.multiselect,
                   'id': name,
                   'options': []
                   }

        for k,v in chain(self.choices, choices):
            if isinstance(value, list):
                checked =  str(k) in [str(x) for x in value]
            else:
                checked = k == value
            if v=='---------' and not k:
                continue
            context['options'] += [{'checked': checked, 'label': v, 'value': k}]

        if not any(opt['checked'] for opt in context['options']) and value:
            context['options'] += [{'checked': True, 'label': value, 'value': value}]
        return render_to_string(template, context)

    def value_from_datadict(self, data, files, name):
        if self.multiselect and isinstance(data, MultiValueDict):
            return data.getlist(name)
        return data.get(name)
