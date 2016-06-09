from django import forms
from django.forms import inlineformset_factory
from dateutil.parser import parse

from isi_mip.climatemodels.fields import MyModelSingleChoiceField, MyModelMultipleChoiceField
from isi_mip.climatemodels.models import *
from isi_mip.climatemodels.widgets import MyMultiSelect, MyTextInput, MyBooleanSelect, RefPaperWidget

ContactPersonFormset = inlineformset_factory(ImpactModel, ContactPerson,
                                             extra=1, max_num=2, min_num=1, fields='__all__',
                                             can_delete=False, help_texts='The scientists responsible for performing the simulations for this sector')


class ImpactModelStartForm(forms.ModelForm):
    owner = forms.ModelChoiceField(queryset=User.objects, label='Model owner')
    model = forms.ModelChoiceField(queryset=ImpactModel.objects.order_by('name'), required=False)
    name = forms.CharField(label='New Impact Model', required=False)
    sector = forms.ChoiceField(choices=ImpactModel.SECTOR_CHOICES, required=False)

    class Meta:
        model = ImpactModel
        fields = ('owner', 'model', 'name', 'sector')


class ImpactModelForm(forms.ModelForm):
    region = MyModelMultipleChoiceField(allowcustom=True, queryset=Region.objects, required=True)
    simulation_round = MyModelMultipleChoiceField(allowcustom=True, queryset=SimulationRound.objects)
    spatial_aggregation = MyModelSingleChoiceField(allowcustom=True, queryset=SpatialAggregation.objects)
    climate_data_sets = MyModelMultipleChoiceField(allowcustom=True, queryset=InputData.objects)
    climate_variables = MyModelMultipleChoiceField(allowcustom=True, queryset=ClimateVariable.objects)
    socioeconomic_input_variables = MyModelMultipleChoiceField(allowcustom=True, queryset=SocioEconomicInputVariables.objects)
    class Meta:
        model = ImpactModel
        exclude = ('owner',)
        widgets = {
            'name': MyTextInput(),
            'sector': MyMultiSelect(),
            'version': MyTextInput(),
            'main_reference_paper': RefPaperWidget(),
            'other_references': RefPaperWidget(),
            'short_description': MyTextInput(textarea=True),
            'spatial_resolution': MyMultiSelect(allowcustom=True),
            'spatial_resolution_info': MyTextInput(textarea=True),
            'temporal_resolution_climate': MyMultiSelect(allowcustom=True),
            'temporal_resolution_co2': MyMultiSelect(allowcustom=True),
            'temporal_resolution_land': MyMultiSelect(allowcustom=True),
            'temporal_resolution_soil': MyMultiSelect(allowcustom=True),
            'temporal_resolution_info': MyTextInput(textarea=True),
            'climate_variables_info': MyTextInput(textarea=True),
            'soil_dataset': MyTextInput(),
            'additional_input_data_sets': MyTextInput(),
            'exceptions_to_protocol': MyTextInput(textarea=True),
            'spin_up': MyBooleanSelect(nullable=True),
            'spin_up_design': MyTextInput(textarea=True),
            'natural_vegetation_partition': MyTextInput(textarea=True),
            'natural_vegetation_dynamics': MyTextInput(textarea=True),
            'natural_vegetation_cover_dataset': MyTextInput(),
            'management': MyTextInput(textarea=True),
            'extreme_events': MyTextInput(textarea=True),
            'anything_else': MyTextInput(textarea=True),
        }

    @staticmethod
    def _ref_paper(args):
        if not args['doi'] and not args['title']:
            return None
        if args['doi']:
            rp = ReferencePaper.objects.get_or_create(doi=args['doi'])[0]
            rp.title = args['title']
        else:
            try:
                rp = ReferencePaper.objects.get_or_create(title=args['title'])[0]
            except ReferencePaper.MultipleObjectsReturned:
                rp = ReferencePaper.objects.create(title=args['title'], doi=args['doi'])
        rp.lead_author = args['lead_author']
        rp.journal_name = args['journal_name']
        rp.journal_volume = args['journal_volume']
        rp.journal_pages = args['journal_pages']
        rp.first_published = args['first_published']
        rp.save()
        return rp

    def clean_main_reference_paper(self):
        myargs = {
            'lead_author': self.data.getlist('main_reference_paper-author')[0],
            'title': self.data.getlist('main_reference_paper-title')[0],
            'journal_name': self.data.getlist('main_reference_paper-journal')[0],
            'doi': self.data.getlist('main_reference_paper-doi')[0],
            'journal_volume': self.data.getlist('main_reference_paper-volume')[0] or None,
            'journal_pages': self.data.getlist('main_reference_paper-page')[0]
        }
        try:
            myargs['first_published'] = parse(self.data.getlist('main_reference_paper-date')[0])
        except:
            myargs['first_published'] = None
        return self._ref_paper(myargs)


    def clean_other_references(self):
        rps = []
        for i in range(len(self.data.getlist('other_references-title')) -1):
            myargs = {
                'lead_author': self.data.getlist('other_references-author')[i],
                'title': self.data.getlist('other_references-title')[i],
                'journal_name': self.data.getlist('other_references-journal')[i],
                'doi': self.data.getlist('other_references-doi')[i],
                'journal_volume': self.data.getlist('other_references-volume')[i] or None,
                'journal_pages': self.data.getlist('other_references-page')[i]
            }
            try:
                myargs['first_published'] = parse(self.data.getlist('other_references-date')[i])
            except:
                myargs['first_published'] = None
            rps.append(self._ref_paper(myargs))
            # paperparse = self._ref_paper(myargs)
            # if paperparse:
            #     rps.append(paperparse)
        return rps

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
            'crops': MyTextInput(textarea=True),
            'land_coverage': MyTextInput(textarea=True),
            'planting_date_decision': MyTextInput(textarea=True),
            'planting_density': MyTextInput(textarea=True),
            'crop_cultivars': MyTextInput(textarea=True),
            'fertilizer_application': MyTextInput(textarea=True),
            'irrigation': MyTextInput(textarea=True),
            'crop_residue': MyTextInput(textarea=True),
            'initial_soil_water': MyTextInput(textarea=True),
            'initial_soil_nitrate_and_ammonia': MyTextInput(textarea=True),
            'initial_soil_C_and_OM': MyTextInput(textarea=True),
            'initial_crop_residue': MyTextInput(textarea=True),
            'lead_area_development': MyTextInput(textarea=True),
            'light_interception': MyTextInput(textarea=True),
            'light_utilization': MyTextInput(textarea=True),
            'yield_formation': MyTextInput(textarea=True),
            'crop_phenology': MyTextInput(textarea=True),
            'root_distribution_over_depth': MyTextInput(textarea=True),
            'stresses_involved': MyTextInput(textarea=True),
            'type_of_water_stress': MyTextInput(textarea=True),
            'type_of_heat_stress': MyTextInput(textarea=True),
            'water_dynamics': MyTextInput(textarea=True),
            'evapo_transpiration': MyTextInput(textarea=True),
            'soil_CN_modeling': MyTextInput(textarea=True),
            'co2_effects': MyTextInput(textarea=True),
            'parameters_number_and_description': MyTextInput(textarea=True),
            'calibrated_values': MyTextInput(textarea=True),
            'output_variable_and_dataset': MyTextInput(textarea=True),
            'spatial_scale_of_calibration_validation': MyTextInput(textarea=True),
            'temporal_scale_of_calibration_validation': MyTextInput(textarea=True),
            'criteria_for_evaluation': MyTextInput(textarea=True),
        }


class BiomesForestsForm(forms.ModelForm):
    template = 'edit_biomes.html'

    class Meta:
        model = BiomesForests
        exclude = ('impact_model',)
        widgets = {
            'output': MyTextInput(),
            'output_per_pft': MyTextInput(),
            'considerations': MyTextInput(textarea=True),
            'dynamic_vegetation': MyTextInput(textarea=True),
            'nitrogen_limitation': MyTextInput(textarea=True),
            'co2_effects': MyTextInput(textarea=True),
            'light_interception': MyTextInput(textarea=True),
            'light_utilization': MyTextInput(textarea=True),
            'phenology': MyTextInput(textarea=True),
            'water_stress': MyTextInput(textarea=True),
            'heat_stress': MyTextInput(textarea=True),
            'evapotranspiration_approach': MyTextInput(textarea=True),
            'rooting_depth_differences': MyTextInput(textarea=True),
            'root_distribution': MyTextInput(textarea=True),
            'permafrost': MyTextInput(textarea=True),
            'closed_energy_balance': MyTextInput(textarea=True),
            'soil_moisture_surface_temperature_coupling': MyTextInput(textarea=True),
            'latent_heat': MyTextInput(textarea=True),
            'sensible_heat': MyTextInput(textarea=True),
            'mortality_age': MyTextInput(textarea=True),
            'mortality_fire': MyTextInput(textarea=True),
            'mortality_drought': MyTextInput(textarea=True),
            'mortality_insects': MyTextInput(textarea=True),
            'mortality_storm': MyTextInput(textarea=True),
            'mortality_stochastic_random_disturbance': MyTextInput(textarea=True),
            'mortality_other': MyTextInput(textarea=True),
            'mortality_remarks': MyTextInput(textarea=True),
            'nbp_fire': MyTextInput(textarea=True),
            'nbp_landuse_change': MyTextInput(textarea=True),
            'nbp_harvest': MyTextInput(textarea=True),
            'nbp_other': MyTextInput(textarea=True),
            'nbp_comments': MyTextInput(textarea=True),
            'list_of_pfts': MyTextInput(textarea=True),
            'pfts_comments': MyTextInput(textarea=True),
        }


class EnergyForm(forms.ModelForm):
    template = 'edit_energy.html'

    class Meta:
        model = Energy
        exclude = ('impact_model',)
        widgets = {
            'model_type': MyTextInput(textarea=True),
            'temporal_extent': MyTextInput(textarea=True),
            'temporal_resolution': MyTextInput(textarea=True),
            'data_format_for_input': MyTextInput(textarea=True),
            'impact_types_energy_demand': MyTextInput(textarea=True),
            'impact_types_temperature_effects_on_thermal_power': MyTextInput(textarea=True),
            'impact_types_weather_effects_on_renewables': MyTextInput(textarea=True),
            'impact_types_water_scarcity_impacts': MyTextInput(textarea=True),
            'impact_types_other': MyTextInput(textarea=True),
            'output_energy_demand': MyTextInput(textarea=True),
            'output_energy_supply': MyTextInput(textarea=True),
            'output_water_scarcity': MyTextInput(textarea=True),
            'output_economics': MyTextInput(textarea=True),
            'output_other': MyTextInput(textarea=True),
            'variables_not_directly_from_GCMs': MyTextInput(textarea=True),
            'response_function_of_energy_demand_to_HDD_CDD': MyTextInput(textarea=True),
            'factor_definition_and_calculation': MyTextInput(textarea=True),
            'biomass_types': MyTextInput(textarea=True),
            'maximum_potential_assumption': MyTextInput(textarea=True),
            'bioenergy_supply_costs': MyTextInput(textarea=True),
            'socioeconomic_input': MyTextInput(textarea=True),
        }


class MarineEcosystemsForm(forms.ModelForm):
    template = 'edit.html'

    class Meta:
        model = MarineEcosystems
        exclude = ('impact_model',)
        widgets = {
            'defining_features': MyTextInput(textarea=True),
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
    template = 'edit_water.html'

    class Meta:
        model = Water
        exclude = ('impact_model',)
        widgets = {
            'technological_progress': MyTextInput(textarea=True),
            'soil_layers': MyTextInput(textarea=True),
            'water_use': MyTextInput(textarea=True),
            'water_sectors': MyTextInput(textarea=True),
            'routing': MyTextInput(textarea=True),
            'routing_data': MyTextInput(textarea=True),
            'land_use': MyTextInput(textarea=True),
            'dams_reservoirs': MyTextInput(textarea=True),
            'calibration': MyBooleanSelect(),
            'calibration_years': MyTextInput(),
            'calibration_dataset': MyTextInput(),
            'calibration_catchments': MyTextInput(),
            'vegetation': MyBooleanSelect(),
            'vegetation_representation': MyTextInput(),
            "methods_evapotranspiration": MyTextInput(textarea=True),
            'methods_snowmelt': MyTextInput(textarea=True),
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
