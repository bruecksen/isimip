from django import forms
from django.db import transaction
from django.forms import ModelChoiceField, inlineformset_factory

from isi_mip.climatemodels.models import *
from isi_mip.climatemodels.widgets import MultiSelect, TomiTextInput, BooleanSelect

ContactPersonFormset = inlineformset_factory(ImpactModel, ContactPerson, extra=1, max_num=2, fields='__all__')


class ImpactModelStartForm(forms.ModelForm):
    class Meta:
        model = ImpactModel
        fields = ('name', 'sector', 'owner')


class MyModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    # widget = MultiSelect(multiselect=True, allowcustom=True)

    def __init__(self, queryset, multiselect=False, allowcustom=False, fieldname='name', required=True, widget=None, label=None,
                 initial=None, help_text='', *args, **kwargs):

        widget = widget or MultiSelect(multiselect=multiselect, allowcustom=allowcustom)
        super().__init__(queryset, required=required, widget=widget, label=label,
                 initial=initial, help_text=help_text, *args, **kwargs)
        self.fieldname = fieldname

    def add_new_choices(self, value):
        key = self.to_field_name or 'pk'
        new_values = []
        for pk in value:
            try:
                self.queryset.filter(**{key: pk})
                new_values += [pk]
            except (ValueError, TypeError):
                new_value = self.queryset.get_or_create(**{self.fieldname:pk})[0]
                new_values += [str(getattr(new_value, key))]

        value = new_values
        return value

    def clean(self, value):
        value = self.add_new_choices(value)
        return super().clean(value)


class ImpactModelForm(forms.ModelForm):
    references = forms.CharField(max_length=400, label='References', required=False)
    region = MyModelMultipleChoiceField(multiselect=True, allowcustom=True, queryset=Region.objects)
    simulation_round = MyModelMultipleChoiceField(multiselect=True, allowcustom=True, queryset=SimulationRound.objects)
    spatial_aggregation = MyModelMultipleChoiceField(allowcustom=True, queryset=SpatialAggregation.objects)
    # 'main_reference_paper'
    # 'other_references'
    climate_data_sets = MyModelMultipleChoiceField(multiselect=True, allowcustom=True, queryset=InputData.objects)
    climate_variables = MyModelMultipleChoiceField(multiselect=True, allowcustom=True, queryset=ClimateVariable.objects)
    socioeconomic_input_variables = MyModelMultipleChoiceField(multiselect=True, allowcustom=True, queryset=SocioEconomicInputVariables.objects)

    class Meta:
        model = ImpactModel
        exclude = ('main_reference_paper', 'other_references', 'owner')
        # fields = '__all__'
        widgets = {
            'name': TomiTextInput(),
            'sector': MultiSelect(),
            'version': TomiTextInput(),
            'short_description': TomiTextInput(),
            'spatial_resolution': MultiSelect(allowcustom=True),
            'temporal_resolution_climate': MultiSelect(allowcustom=True),
            'temporal_resolution_co2': MultiSelect(allowcustom=True),
            'temporal_resolution_land': MultiSelect(allowcustom=True),
            'temporal_resolution_soil': MultiSelect(allowcustom=True),
            'soil_dataset': TomiTextInput(),
            'additional_input_data_sets': TomiTextInput(),
            'exceptions_to_protocol': TomiTextInput(),
            'spin_up': BooleanSelect(nullable=True),
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
        pass  # TODO das muss noch implementiert werden

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['name'].widget.attrs['readonly'] = True


#### SECTOREN
class AgricultureForm(forms.ModelForm):
    template = 'edit_agriculture.html'

    class Meta:
        model = Agriculture
        exclude = ('impact_model',)
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


class BiomesForestsForm(forms.ModelForm):
    template = 'edit_biomes.html'

    class Meta:
        model = BiomesForests
        exclude = ('impact_model',)
        widgets = {
            'output': TomiTextInput(),
            'output_per_pft': TomiTextInput(),
            'considerations': TomiTextInput(),
            'dynamic_vegetation': TomiTextInput(),
            'nitrogen_limitation': TomiTextInput(),
            'co2_effects': TomiTextInput(),
            'light_interception': TomiTextInput(),
            'light_utilization': TomiTextInput(),
            'phenology': TomiTextInput(),
            'water_stress': TomiTextInput(),
            'heat_stress': TomiTextInput(),
            'evapotranspiration_approach': TomiTextInput(),
            'rooting_depth_differences': TomiTextInput(),
            'root_distribution': TomiTextInput(),
            'permafrost': TomiTextInput(),
            'closed_energy_balance': TomiTextInput(),
            'soil_moisture_surface_temperature_coupling': TomiTextInput(),
            'latent_heat': TomiTextInput(),
            'sensible_heat': TomiTextInput(),
            'mortality_age': TomiTextInput(),
            'mortality_fire': TomiTextInput(),
            'mortality_drought': TomiTextInput(),
            'mortality_insects': TomiTextInput(),
            'mortality_storm': TomiTextInput(),
            'mortality_stochastic_random_disturbance': TomiTextInput(),
            'mortality_other': TomiTextInput(),
            'mortality_remarks': TomiTextInput(),
            'nbp_fire': TomiTextInput(),
            'nbp_landuse_change': TomiTextInput(),
            'nbp_harvest': TomiTextInput(),
            'nbp_other': TomiTextInput(),
            'nbp_comments': TomiTextInput(),
            'list_of_pfts': TomiTextInput(),
            'pfts_comments': TomiTextInput(),
        }


class EnergyForm(forms.ModelForm):
    template = 'edit_energy.html'

    class Meta:
        model = Energy
        exclude = ('impact_model',)
        widgets = {
            'model_type': TomiTextInput(),
            'temporal_extent': TomiTextInput(),
            'temporal_resolution': TomiTextInput(),
            'data_format_for_input': TomiTextInput(),
            'impact_types_energy_demand': TomiTextInput(),
            'impact_types_temperature_effects_on_thermal_power': TomiTextInput(),
            'impact_types_weather_effects_on_renewables': TomiTextInput(),
            'impact_types_water_scarcity_impacts': TomiTextInput(),
            'impact_types_other': TomiTextInput(),
            'output_energy_demand': TomiTextInput(),
            'output_energy_supply': TomiTextInput(),
            'output_water_scarcity': TomiTextInput(),
            'output_economics': TomiTextInput(),
            'output_other': TomiTextInput(),
            'variables_not_directly_from_GCMs': TomiTextInput(),
            'response_function_of_energy_demand_to_HDD_CDD': TomiTextInput(),
            'factor_definition_and_calculation': TomiTextInput(),
            'biomass_types': TomiTextInput(),
            'maximum_potential_assumption': TomiTextInput(),
            'bioenergy_supply_costs': TomiTextInput(),
            'socioeconomic_input': TomiTextInput(),
        }


class MarineEcosystemsForm(forms.ModelForm):
    template = 'edit.html'

    class Meta:
        model = MarineEcosystems
        exclude = ('impact_model',)
        widgets = {
            'defining_features': TomiTextInput(),
            'spatial_scale': TomiTextInput(),
            'spatial_resolution': TomiTextInput(),
            'temporal_scale': TomiTextInput(),
            'temporal_resolution': TomiTextInput(),
            'taxonomic_scope': TomiTextInput(),
            'vertical_resolution': TomiTextInput(),
            'spatial_dispersal_included': TomiTextInput(),
            'fishbase_used_for_mass_length_conversion': TomiTextInput(),
        }


class WaterForm(forms.ModelForm):
    template = 'edit.html'

    class Meta:
        model = Water
        exclude = ('impact_model',)
        widgets = {
            'technological_progress': TomiTextInput(),
            'soil_layers': TomiTextInput(),
            'water_use': TomiTextInput(),
            'water_sectors': TomiTextInput(),
            'routing': TomiTextInput(),
            'routing_data': TomiTextInput(),
            'land_use': TomiTextInput(),
            'dams_reservoirs': TomiTextInput(),
            'calibration': BooleanSelect(),
            'calibration_years': TomiTextInput(),
            'calibration_dataset': TomiTextInput(),
            'calibration_catchments': TomiTextInput(),
            'vegetation': BooleanSelect(),
            'vegetation_representation': TomiTextInput(),
            'methods_evapotraspiration': TomiTextInput(),
            'methods_snowmelt': TomiTextInput(),
        }


def get_sector_form(sector):
    mapping = {
        'agriculture': AgricultureForm,
        'agroeconomicmodelling': None,
        'biodiversity': None,
        'biomes': BiomesForestsForm,
        'coastalinfrastructure': None,
        'computablegeneralequilibriummodelling': None,
        'energy': EnergyForm,
        'forests': BiomesForestsForm,
        'health': None,
        'marineecosystemsglobal': MarineEcosystemsForm,
        'marineecosystemsregional': MarineEcosystemsForm,
        'permafrost': None,
        'waterglobal': WaterForm,
        'waterregional': WaterForm,
    }
    return mapping[sector]
