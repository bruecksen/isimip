from django.forms import TypedChoiceField, ChoiceField

from isi_mip.choiceorotherfield.widgets import SelectOrOther


class MyTypedChoiceField(TypedChoiceField):
    widget = SelectOrOther

    def validate(self, value):
        super(ChoiceField, self).validate(value)
