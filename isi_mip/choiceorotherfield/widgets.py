from django.forms import RadioSelect
from django.forms.utils import flatatt
from django.forms.widgets import RadioFieldRenderer, ChoiceFieldRenderer, RadioChoiceInput, MultiWidget, TextInput, \
    ChoiceInput
from django.utils.encoding import python_2_unicode_compatible, force_text
from django.utils.html import format_html, html_safe
from django.utils.safestring import mark_safe


class TextChoiceInput(ChoiceInput):
    input_type = 'text'
    def __init__(self, name, value, attrs, choice, index):
        super().__init__(name, value, attrs, choice, index)
        self.attrs['id'] += "_text"


class MyChoiceFieldRenderer(ChoiceFieldRenderer):
    choice_input_class = RadioChoiceInput
    outer_html = '<ul class="choiceorotherfield" {id_attr}>{content}</ul>'

    def render(self):
        id_ = self.attrs.get('id')
        output = []

        for i, choice in enumerate(self.choices):
            w = self.choice_input_class(self.name, self.value,
                                        self.attrs.copy(), choice, i)
            output.append(format_html(self.inner_html,
                                      choice_value=force_text(w), sub_widgets=''))

        choicee = self.value in [x[0] for x in self.choices]
        print("value", self.value)
        if not choicee:
            valuee = self.value
            valuer = self.value
        else:
            valuee = ''
            valuer = None

        xy = TextChoiceInput(self.name+"_text", valuer, self.attrs.copy(), [valuee, ''], index=len(self.choices))
        xx = self.choice_input_class(self.name, valuer, self.attrs.copy(), [valuee, xy],
                                     index=len(self.choices))
        output.append(format_html(self.inner_html,
                                  choice_value=force_text(xx),
                                  sub_widgets=''))
        options = format_html(self.outer_html,
                              id_attr=format_html(' id="{}"', id_) if id_ else '',
                              content=mark_safe('\n'.join(output)))
        return options


class SelectOrOther(RadioSelect):
    renderer = MyChoiceFieldRenderer

    class Media:
        js = ('js/choiceorotherfield.js',)
        css = {
            'all': ('css/choiceorotherfield.css',)
        }
