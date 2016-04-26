from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, ButtonHolder, Submit, Row
from django import forms
from django.forms import ModelMultipleChoiceField, ModelChoiceField, modelformset_factory, inlineformset_factory
from django.forms.formsets import formset_factory

from isi_mip.climatemodels.models import ImpactModel, ContactPerson
from isi_mip.climatemodels.widgets import MultiSelect, TomiTextInput

ContactPersonFormset = inlineformset_factory(ImpactModel, ContactPerson, extra=1, max_num=2, fields='__all__')

class ImpactModelStartForm(forms.ModelForm):
    class Meta:
        model = ImpactModel
        fields = ('name', 'sector', 'owner')

class ImpactModelForm(forms.ModelForm):
    # references = forms.CharField(max_length=400, label='References')
    class Meta:
        model = ImpactModel
        exclude = ('main_reference_paper', 'other_references', 'owner')
        # fields = ['__all__', 'references']
        fields = '__all__'
        widgets = {
            'sector': MultiSelect(allowcustom=True),
            'region': MultiSelect(multiselect=True, allowcustom=True),
            'simulation_round': MultiSelect(multiselect=True, allowcustom=True),
            'version': TomiTextInput(),
            'short_description': TomiTextInput(),
            # 'main_reference_paper'
            # 'other_references'
            # 'references':

            # TECH
            'spatial_aggregation': MultiSelect(allowcustom=True),
            'spatial_resolution': MultiSelect(allowcustom=True),
            'temporal_resolution_climate': MultiSelect(allowcustom=True),
            'temporal_resolution_co2': MultiSelect(allowcustom=True),
            'temporal_resolution_land': MultiSelect(allowcustom=True),
            'temporal_resolution_soil': MultiSelect(allowcustom=True),

            # INPUT DATA
            'climate_data_sets': MultiSelect(multiselect=True, allowcustom=True),
            'climate_variables': MultiSelect(multiselect=True, allowcustom=True),
            'socioeconomic_input_variables': MultiSelect(multiselect=True, allowcustom=True),
            'soil_dataset': TomiTextInput(),
            'additional_input_data_sets': TomiTextInput(),

            #OTHER
            'exceptions_to_protocol': TomiTextInput(),
            'spin_up': MultiSelect(), # TODO: see if this holds.
            'spin_up_design': TomiTextInput(),
            'natural_vegetation_partition': TomiTextInput(),
            'natural_vegetation_dynamics': TomiTextInput(),
            'natural_vegetation_cover_dataset': TomiTextInput(),
            'management': TomiTextInput(),
            'extreme_events': TomiTextInput(),
            'anything_else': TomiTextInput(),
            'comments': TomiTextInput(textarea=True),

        }

    def clean_references(self):
        import ipdb; ipdb.set_trace()
        pass

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
        # print(self.data)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                'Basic Information',
                'name', 'sector', 'region', 'simulation_round', 'version', 'short_description',
            ),
            Fieldset(
                'Technical Information',
                'spatial_aggregation', 'spatial_resolution', 'temporal_resolution_climate',
                'temporal_resolution_co2', 'temporal_resolution_land', 'temporal_resolution_soil'
            ),
            Fieldset(
                'Input Data',
                'climate_data_sets', 'climate_variables', 'socioeconomic_input_variables', 'soil_dataset',
                'additional_input_data_sets'
            ),
            Fieldset(
                'Other',
                'exceptions_to_protocol', 'spin_up', 'spin_up_design', 'natural_vegetation_partition',
                'natural_vegetation_dynamics', 'natural_vegetation_cover_dataset', 'management',
                'extreme_events', 'anything_else', 'comments',
            ),
        )
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
