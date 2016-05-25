from django import forms
from django.forms import inlineformset_factory

from isi_mip.climatemodels.fields import MyModelSingleChoiceField, MyModelMultipleChoiceField
from isi_mip.climatemodels.models import *
from isi_mip.climatemodels.widgets import MyMultiSelect, MyTextInput, MyBooleanSelect

ContactPersonFormset = inlineformset_factory(ImpactModel, ContactPerson,
                                             extra=1, max_num=2, min_num=1, fields='__all__',
                                             can_delete=False)


class ImpactModelStartForm(forms.ModelForm):
    owner = forms.ModelChoiceField(queryset=User.objects, label='Model owner')
    model = forms.ModelChoiceField(queryset=ImpactModel.objects.order_by('name'), required=False)
    name = forms.CharField(label='New Impact Model', required=False)
    sector = forms.ChoiceField(choices=ImpactModel.SECTOR_CHOICES, required=False)

    class Meta:
        model = ImpactModel
        fields = ('owner', 'model', 'name', 'sector')


class ImpactModelForm(forms.ModelForm):
    # references = forms.CharField(max_length=400, label='References', required=False)
    region = MyModelMultipleChoiceField(allowcustom=True, queryset=Region.objects, required=True)
    simulation_round = MyModelMultipleChoiceField(allowcustom=True, queryset=SimulationRound.objects)
    spatial_aggregation = MyModelSingleChoiceField(allowcustom=True, queryset=SpatialAggregation.objects)
    # 'main_reference_paper'
    # 'other_references'
    climate_data_sets = MyModelMultipleChoiceField(allowcustom=True, queryset=InputData.objects)
    climate_variables = MyModelMultipleChoiceField(allowcustom=True, queryset=ClimateVariable.objects)
    socioeconomic_input_variables = MyModelMultipleChoiceField(allowcustom=True, queryset=SocioEconomicInputVariables.objects)

    class Meta:
        model = ImpactModel
        exclude = ('other_references', 'owner')
        # fields = '__all__'
        widgets = {
            'name': MyTextInput(),
            'sector': MyMultiSelect(),
            'version': MyTextInput(),
            'main_reference_paper': MyTextInput(),
            'short_description': MyTextInput(),
            'spatial_resolution': MyMultiSelect(allowcustom=True),
            'temporal_resolution_climate': MyMultiSelect(allowcustom=True),
            'temporal_resolution_co2': MyMultiSelect(allowcustom=True),
            'temporal_resolution_land': MyMultiSelect(allowcustom=True),
            'temporal_resolution_soil': MyMultiSelect(allowcustom=True),
            'soil_dataset': MyTextInput(),
            'additional_input_data_sets': MyTextInput(),
            'exceptions_to_protocol': MyTextInput(),
            'spin_up': MyBooleanSelect(nullable=True),
            'spin_up_design': MyTextInput(),
            'natural_vegetation_partition': MyTextInput(),
            'natural_vegetation_dynamics': MyTextInput(),
            'natural_vegetation_cover_dataset': MyTextInput(),
            'management': MyTextInput(),
            'extreme_events': MyTextInput(),
            'anything_else': MyTextInput(),
            'comments': MyTextInput(textarea=True),
        }

    def clean_references(self):
        pass  # TODO das muss noch implementiert werden

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['name'].widget.attrs['readonly'] = True


# SEKTOREN ############################################################
class AgricultureForm(forms.ModelForm):
    template = 'edit_agriculture.html'

    class Meta:
        model = Agriculture
        exclude = ('impact_model',)
        widgets = {
            'crops': MyTextInput(),
            'land_coverage': MyTextInput(),
            'planting_date_decision': MyTextInput(),
            'planting_density': MyTextInput(),
            'crop_cultivars': MyTextInput(),
            'fertilizer_application': MyTextInput(),
            'irrigation': MyTextInput(),
            'crop_residue': MyTextInput(),
            'initial_soil_water': MyTextInput(),
            'initial_soil_nitrate_and_ammonia': MyTextInput(),
            'initial_soil_C_and_OM': MyTextInput(),
            'initial_crop_residue': MyTextInput(),
            'lead_area_development': MyTextInput(),
            'light_interception': MyTextInput(),
            'light_utilization': MyTextInput(),
            'yield_formation': MyTextInput(),
            'crop_phenology': MyTextInput(),
            'root_distribution_over_depth': MyTextInput(),
            'stresses_involved': MyTextInput(),
            'type_of_water_stress': MyTextInput(),
            'type_of_heat_stress': MyTextInput(),
            'water_dynamics': MyTextInput(),
            'evapo_transpiration': MyTextInput(),
            'soil_CN_modeling': MyTextInput(),
            'co2_effects': MyTextInput(),
            'parameters_number_and_description': MyTextInput(),
            'calibrated_values': MyTextInput(),
            'output_variable_and_dataset': MyTextInput(),
            'spatial_scale_of_calibration_validation': MyTextInput(),
            'temporal_scale_of_calibration_validation': MyTextInput(),
            'criteria_for_evaluation': MyTextInput(),
        }


class BiomesForestsForm(forms.ModelForm):
    template = 'edit_biomes.html'

    class Meta:
        model = BiomesForests
        exclude = ('impact_model',)
        widgets = {
            'output': MyTextInput(),
            'output_per_pft': MyTextInput(),
            'considerations': MyTextInput(),
            'dynamic_vegetation': MyTextInput(),
            'nitrogen_limitation': MyTextInput(),
            'co2_effects': MyTextInput(),
            'light_interception': MyTextInput(),
            'light_utilization': MyTextInput(),
            'phenology': MyTextInput(),
            'water_stress': MyTextInput(),
            'heat_stress': MyTextInput(),
            'evapotranspiration_approach': MyTextInput(),
            'rooting_depth_differences': MyTextInput(),
            'root_distribution': MyTextInput(),
            'permafrost': MyTextInput(),
            'closed_energy_balance': MyTextInput(),
            'soil_moisture_surface_temperature_coupling': MyTextInput(),
            'latent_heat': MyTextInput(),
            'sensible_heat': MyTextInput(),
            'mortality_age': MyTextInput(),
            'mortality_fire': MyTextInput(),
            'mortality_drought': MyTextInput(),
            'mortality_insects': MyTextInput(),
            'mortality_storm': MyTextInput(),
            'mortality_stochastic_random_disturbance': MyTextInput(),
            'mortality_other': MyTextInput(),
            'mortality_remarks': MyTextInput(),
            'nbp_fire': MyTextInput(),
            'nbp_landuse_change': MyTextInput(),
            'nbp_harvest': MyTextInput(),
            'nbp_other': MyTextInput(),
            'nbp_comments': MyTextInput(),
            'list_of_pfts': MyTextInput(),
            'pfts_comments': MyTextInput(),
        }


class EnergyForm(forms.ModelForm):
    template = 'edit_energy.html'

    class Meta:
        model = Energy
        exclude = ('impact_model',)
        widgets = {
            'model_type': MyTextInput(),
            'temporal_extent': MyTextInput(),
            'temporal_resolution': MyTextInput(),
            'data_format_for_input': MyTextInput(),
            'impact_types_energy_demand': MyTextInput(),
            'impact_types_temperature_effects_on_thermal_power': MyTextInput(),
            'impact_types_weather_effects_on_renewables': MyTextInput(),
            'impact_types_water_scarcity_impacts': MyTextInput(),
            'impact_types_other': MyTextInput(),
            'output_energy_demand': MyTextInput(),
            'output_energy_supply': MyTextInput(),
            'output_water_scarcity': MyTextInput(),
            'output_economics': MyTextInput(),
            'output_other': MyTextInput(),
            'variables_not_directly_from_GCMs': MyTextInput(),
            'response_function_of_energy_demand_to_HDD_CDD': MyTextInput(),
            'factor_definition_and_calculation': MyTextInput(),
            'biomass_types': MyTextInput(),
            'maximum_potential_assumption': MyTextInput(),
            'bioenergy_supply_costs': MyTextInput(),
            'socioeconomic_input': MyTextInput(),
        }


class MarineEcosystemsForm(forms.ModelForm):
    template = 'edit.html'

    class Meta:
        model = MarineEcosystems
        exclude = ('impact_model',)
        widgets = {
            'defining_features': MyTextInput(),
            'spatial_scale': MyTextInput(),
            'spatial_resolution': MyTextInput(),
            'temporal_scale': MyTextInput(),
            'temporal_resolution': MyTextInput(),
            'taxonomic_scope': MyTextInput(),
            'vertical_resolution': MyTextInput(),
            'spatial_dispersal_included': MyTextInput(),
            'fishbase_used_for_mass_length_conversion': MyTextInput(),
        }


class WaterForm(forms.ModelForm):
    template = 'edit.html'

    class Meta:
        model = Water
        exclude = ('impact_model',)
        widgets = {
            'technological_progress': MyTextInput(),
            'soil_layers': MyTextInput(),
            'water_use': MyTextInput(),
            'water_sectors': MyTextInput(),
            'routing': MyTextInput(),
            'routing_data': MyTextInput(),
            'land_use': MyTextInput(),
            'dams_reservoirs': MyTextInput(),
            'calibration': MyBooleanSelect(),
            'calibration_years': MyTextInput(),
            'calibration_dataset': MyTextInput(),
            'calibration_catchments': MyTextInput(),
            'vegetation': MyBooleanSelect(),
            'vegetation_representation': MyTextInput(),
            'methods_evapotraspiration': MyTextInput(),
            'methods_snowmelt': MyTextInput(),
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
