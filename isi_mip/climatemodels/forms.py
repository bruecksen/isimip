from django import forms
from django.forms import ModelMultipleChoiceField, ModelChoiceField

from isi_mip.climatemodels.models import ImpactModel
from isi_mip.climatemodels.widgets import MultiSelect


class ImpactModelStartForm(forms.ModelForm):
    class Meta:
        model = ImpactModel
        fields = ('name', 'sector', 'owner')

class ImpactModelForm(forms.ModelForm):
    class Meta:
        model = ImpactModel
        exclude = ('main_reference_paper', 'other_references', 'owner')

        widgets = {
            'sector': MultiSelect(allowcustom=True),
            'region': MultiSelect(multiselect=True, allowcustom=True),
            # 'simulation_round':
        }

    def do_the_thing(self):
        for fieldname in self.fields:
            field = self.fields[fieldname]
            if isinstance(field.widget, MultiSelect) and field.widget.allowcustom:
                # print(self.data[fieldname])
                if isinstance(field, ModelChoiceField):
                    self.do_one_thing(field, fieldname)

    def do_one_thing(self, field, fieldname):
        newvalues = set(x for x in self.data.getlist(fieldname) if not x.isdigit())
        oldvalues = [x for x in self.data.getlist(fieldname) if x.isdigit()]
        key = field.to_field_name or 'pk'
        newkeys = []
        for pk in newvalues:
            try:
                field.queryset.filter(**{key: pk})
            except ValueError:
                xxx = field.queryset.get_or_create(name=pk)[0] # TODO: This won't hold a lot of scenarios
                newkeys+=[str(xxx.pk)]
        self.data = self.data.copy()
        self.data.setlist(fieldname, oldvalues + newkeys)
        print(self.data)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.pk:
    #         self.fields['name'].widget.attrs['readonly'] = True
    #
    # def clean_name(self):
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.pk:
    #         return instance.name
    #     else:
    #         return self.cleaned_data['name']

    # def __init__(self, *args, **kwargs):
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Fieldset(
    #             'Basic Information',
    #             'name',
    #             'sector',
    #             'region',
    #             # 'main_reference_paper',
    #             'version',
    #             'short_description',
    #
    #             'spatial_aggregation',
    #         ),
    #         ButtonHolder(
    #             Submit('submit', 'Submit', css_class='button white')
    #         )
    #     )
    #     super().__init__(*args, **kwargs)