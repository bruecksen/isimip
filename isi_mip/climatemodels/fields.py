from django import forms

from isi_mip.climatemodels.widgets import MyMultiSelect


class MyModelSingleChoiceField(forms.ModelChoiceField):
    def __init__(self, queryset, allowcustom=False, fieldname='name',
                 empty_label="---------", required=False, widget=None, label=None, initial=None,
                 help_text='', to_field_name=None, limit_choices_to=None,
                 *args, **kwargs
                 ):
        widget = widget or MyMultiSelect(multiselect=False, allowcustom=allowcustom)
        super().__init__(queryset, empty_label=empty_label, required=required, widget=widget,
                         label=label, initial=initial, help_text=help_text, to_field_name=to_field_name,
                         limit_choices_to=limit_choices_to, *args, **kwargs)
        self.fieldname = fieldname

    def add_new_choices(self, value):
        if value in self.empty_values:
            return None
        key = self.to_field_name or 'pk'
        try:
            self.queryset.get(**{key: value})
            new_value = value
        except (ValueError, TypeError, self.queryset.model.DoesNotExist):
            new_v = self.queryset.get_or_create(**{self.fieldname: value})[0]
            new_value = str(getattr(new_v, key))
        value = new_value
        return value

    def clean(self, value):
        value = self.add_new_choices(value)
        return super().clean(value)


class MyModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def __init__(self, queryset, allowcustom=False, fieldname='name', required=False, widget=None, label=None,
                 initial=None, help_text='', *args, **kwargs):
        widget = widget or MyMultiSelect(multiselect=True, allowcustom=allowcustom)
        super().__init__(queryset, required=required, widget=widget, label=label,
                 initial=initial, help_text=help_text, *args, **kwargs)
        self.fieldname = fieldname

    def add_new_choices(self, value):
        if value in self.empty_values:
            return None
        key = self.to_field_name or 'pk'
        new_values = []
        for pk in value:
            try:
                self.queryset.get(**{key: pk})
                new_values += [pk]
            except (ValueError, TypeError, self.queryset.model.DoesNotExist):
                new_v = self.queryset.get_or_create(**{self.fieldname: pk})[0]
                new_values += [str(getattr(new_v, key))]
        value = new_values
        return value

    def clean(self, value):
        value = self.add_new_choices(value)
        return super().clean(value)