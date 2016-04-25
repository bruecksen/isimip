from itertools import chain

from django.forms import RadioSelect
from django.forms.utils import flatatt
from django.forms.widgets import ChoiceFieldRenderer, RadioChoiceInput, MultiWidget, TextInput, \
    ChoiceInput, CheckboxChoiceInput, RendererMixin, Select, Widget
from django.template.loader import render_to_string
from django.utils.datastructures import MultiValueDict
from django.utils.encoding import python_2_unicode_compatible, force_text
from django.utils.html import format_html, html_safe
from django.utils.safestring import mark_safe


# class TextChoiceInput(ChoiceInput):
#     input_type = 'text'
#     def __init__(self, name, value, attrs, choice, index):
#         super().__init__(name, value, attrs, choice, index)
#         self.attrs['id'] += "_text"
#
#
# class MyChoiceFieldRenderer(ChoiceFieldRenderer):
#     choice_input_class = RadioChoiceInput
#     outer_html = '<ul class="choiceorotherfield" {id_attr}>{content}</ul>'
#     # outer_html = '<ul{id_attr}>{content}</ul>'
#     # inner_html = '<div>{choice_value}{sub_widgets}</div>'
#
#     def render(self):
#         id_ = self.attrs.get('id')
#         output = []
#         print(self.choices)
#         for i, choice in enumerate(self.choices):
#             w = self.choice_input_class(self.name, self.value,
#                                         self.attrs.copy(), choice, i)
#             output.append(format_html(self.inner_html,
#                                       choice_value=force_text(w), sub_widgets=''))
#
#         choicee = self.value in [x[0] for x in self.choices]
#         if not choicee:
#             valuee = self.value
#             valuer = self.value
#         else:
#             valuee = ''
#             valuer = None
#
#         xy = TextChoiceInput(self.name+"_text", valuer, self.attrs.copy(), [valuee, ''], index=len(self.choices))
#         xx = self.choice_input_class(self.name, valuer, self.attrs.copy(), [valuee, xy],
#                                      index=len(self.choices))
#         output.append(format_html(self.inner_html,
#                                   choice_value=force_text(xx),
#                                   sub_widgets=''))
#         options = format_html(self.outer_html,
#                               id_attr=format_html(' id="{}"', id_) if id_ else '',
#                               content=mark_safe('\n'.join(output)))
#         return options
#
# class MyCheckboxChoiceFieldRenderer(MyChoiceFieldRenderer):
#     choice_input_class = CheckboxChoiceInput
#
#
# class BaseOrOther(RendererMixin, Select):
#     class Media:
#         js = ('vendor/js/jquery-2.2.1.min.js', 'js/dings.js')
#         css = {
#             'all': ('css/dings.css',)
#         }
#
# class SelectMultipleOrOther(BaseOrOther):
#     renderer = MyCheckboxChoiceFieldRenderer
#     _empty_value = []
#
# class SelectOrOther(BaseOrOther):
#     renderer = MyChoiceFieldRenderer
#     _empty_value = ''
#

class MultiSelect(Select):
    allow_multiple_selected = True

    def __init__(self, allowcustom=False, multiselect=False, attrs=None):
        super().__init__(attrs)
        self.allowcustom = allowcustom
        self.multiselect = multiselect

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        template = 'widgets/multiselect.html'
        context = {'allowcustom': self.allowcustom,
                   'singleselect': not self.multiselect,
                   'id': name,
                   # 'label': '',
                   }
        context['options'] = []
        for k,v in chain(self.choices, choices):
            if isinstance(value, list):
                checked =  str(k) in [str(x) for x in value]
            else:
                checked = k == value
            context['options'] += [{'checked': checked, 'label': v, 'value': k}]

        return render_to_string(template, context)

    def value_from_datadict(self, data, files, name):
        if self.multiselect and isinstance(data, MultiValueDict):
            return data.getlist(name)
        return data.get(name)
