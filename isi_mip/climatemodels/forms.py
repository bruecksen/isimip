from django import forms

from isi_mip.climatemodels.models import ImpactModel

class ImpactModelStartForm(forms.ModelForm):
    class Meta:
        model = ImpactModel
        fields = ('name', 'sector', 'owner')

class ImpactModelForm(forms.ModelForm):
    class Meta:
        model = ImpactModel
        exclude = ('main_reference_paper', 'other_references', 'owner')

        widgets = {
            # 'spatial_aggregation': forms.RadioSelect(),
            # 'region': forms.CheckboxSelectMultiple(),
            # 'region': SelectMultipleOrOther(),
            # 'region': forms.CheckboxSelectMultiple(),
            # 'spatial_aggregation': SelectOrOther(),
            # 'region': forms.TextInput()
            # 'spatial_aggregation': forms.TextInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['name'].widget.attrs['readonly'] = True

    def clean_name(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.name
        else:
            return self.cleaned_data['name']
    #
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