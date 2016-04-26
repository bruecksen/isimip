from django import forms
from django.forms import ModelChoiceField, inlineformset_factory

from isi_mip.climatemodels.models import *
from isi_mip.climatemodels.widgets import MultiSelect, TomiTextInput, NullBooleanSelect

ContactPersonFormset = inlineformset_factory(ImpactModel, ContactPerson, extra=1, max_num=2, fields='__all__')

class ImpactModelStartForm(forms.ModelForm):
    class Meta:
        model = ImpactModel
        fields = ('name', 'sector', 'owner')

class CustomModelForm(forms.ModelForm):
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
                xxx = field.queryset.get_or_create(name=pk)[0]  # TODO: This won't hold a lot of scenarios
                newkeys += [str(xxx.pk)]
        self.data = self.data.copy()
        self.data.setlist(fieldname, oldvalues + newkeys)
        # print(self.data)

class ImpactModelForm(CustomModelForm):
    references = forms.CharField(max_length=400, label='References', required=False)
    class Meta:
        model = ImpactModel
        exclude = ('main_reference_paper', 'other_references', 'owner')
        # fields = ['__all__', 'references']
        fields = '__all__'
        widgets = {
            'name': TomiTextInput(),
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
            'spin_up': NullBooleanSelect(),
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
        pass # TODO das muss noch implementiert werden


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['name'].widget.attrs['readonly'] = True


class EnergyForm(forms.ModelForm):
    class Meta:
        model = Energy
        exclude = ('impact_model',)
        # fields = '__all__'
        widgets = {
            # Model & method characteristics
            'model_type': TomiTextInput(),
            'temporal_extent': TomiTextInput(),
            'temporal_resolution': TomiTextInput(),
            'data_format_for_input': TomiTextInput(),
            # Impact Types
            'impact_types_energy_demand': TomiTextInput(),
            'impact_types_temperature_effects_on_thermal_power': TomiTextInput(),
            'impact_types_weather_effects_on_renewables': TomiTextInput(),
            'impact_types_water_scarcity_impacts': TomiTextInput(),
            'impact_types_other': TomiTextInput(),
            # Output
            'output_energy_demand': TomiTextInput(),
            'output_energy_supply': TomiTextInput(),
            'output_water_scarcity': TomiTextInput(),
            'output_economics': TomiTextInput(),
            'output_other': TomiTextInput(),
            # Further Information
            'variables_not_directly_from_GCMs': TomiTextInput(),
            'response_function_of_energy_demand_to_HDD_CDD': TomiTextInput(),
            'factor_definition_and_calculation': TomiTextInput(),
            'biomass_types': TomiTextInput(),
            'maximum_potential_assumption': TomiTextInput(),
            'bioenergy_supply_costs': TomiTextInput(),
            'socioeconomic_input': TomiTextInput(),
        }


class AgricultureForm(forms.ModelForm):
    class Meta:
        model = Agriculture
        fields = '__all__'
        widgets = {
            'crops': TomiTextInput(),
            'land_coverage': TomiTextInput(),
            'planting_date_decision': TomiTextInput(),
            'planting_density': TomiTextInput(),
            'crop_cultivars': TomiTextInput(),
            'fertilizer_application': TomiTextInput(),
            'irrigation': TomiTextInput(),
            'crop_residue': TomiTextInput(),
            'initial_soil_water': TomiTextInput(),
            'initial_soil_nitrate_and_ammonia': TomiTextInput(),
            'initial_soil_C_and_OM': TomiTextInput(),
            'initial_crop_residue': TomiTextInput(),
            'lead_area_development': TomiTextInput(),
            'light_interception': TomiTextInput(),
            'light_utilization': TomiTextInput(),
            'yield_formation': TomiTextInput(),
            'crop_phenology': TomiTextInput(),
            'root_distribution_over_depth': TomiTextInput(),
            'stresses_involved': TomiTextInput(),
            'type_of_water_stress': TomiTextInput(),
            'type_of_heat_stress': TomiTextInput(),
            'water_dynamics': TomiTextInput(),
            'evapo_transpiration': TomiTextInput(),
            'soil_CN_modeling': TomiTextInput(),
            'co2_effects': TomiTextInput(),
            'parameters_number_and_description': TomiTextInput(),
            'calibrated_values': TomiTextInput(),
            'output_variable_and_dataset': TomiTextInput(),
            'spatial_scale_of_calibration_validation': TomiTextInput(),
            'temporal_scale_of_calibration_validation': TomiTextInput(),
            'criteria_for_evaluation': TomiTextInput(),
        }

class WaterForm(forms.ModelForm):
    class Meta:
        model = Water
        fields = '__all__'

class BiomesForestsForm(forms.ModelForm):
    class Meta:
        model = BiomesForests
        fields = '__all__'

class MarineEcosystemsForm(forms.ModelForm):
    class Meta:
        model = MarineEcosystems
        fields = '__all__'

class EmptyForm(forms.Form):
    pass

def get_sector_form(sector):
    mapping = {
        'energy': EnergyForm,
        'agriculture': AgricultureForm,
        'waterglobal': WaterForm,
        'waterregional': WaterForm,
        'marineecosystemsregional': MarineEcosystemsForm,
        'marineecosystemsglobal': MarineEcosystemsForm,
        'biomes': BiomesForestsForm,
        'forests': BiomesForestsForm,
        'permafrost': EmptyForm,
        'health': EmptyForm,
        'biodiversity': EmptyForm,
        'coastalinfrastructure': EmptyForm,
        'agroeconomicmodelling': EmptyForm,
        'computablegeneralequilibriummodelling': EmptyForm,
    }
    return mapping[sector]