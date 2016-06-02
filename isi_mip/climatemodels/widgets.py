from django.forms.widgets import Select, TextInput, Widget
from django.utils.datastructures import MultiValueDict

class RefPaperWidget(Widget):
    pass


class MyBooleanSelect(Select):
    def __init__(self, nullable=False, attrs=None, choices=()):
        super().__init__(attrs=attrs, choices=choices)
        self.nullable = nullable


class MyMultiSelect(Select):
    def __init__(self, allowcustom=False, multiselect=False, attrs=None):
        super().__init__(attrs)
        self.allowcustom = allowcustom
        self.multiselect = multiselect
        self.allow_multiple_selected = multiselect

    def value_from_datadict(self, data, files, name):
        if self.multiselect and isinstance(data, MultiValueDict):
            return data.getlist(name)
        return data.get(name)


class MyTextInput(TextInput):
    def __init__(self, textarea=False, emailfield=False):
        super().__init__()
        self.textarea = textarea
        self.emailfield = emailfield