from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from isi_mip.choiceorotherfield.models import ChoiceOrOtherField


class Region(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class ReferencePaper(models.Model):
    name = models.CharField(max_length=500)
    doi = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return "%s (%s)" %(self.name,self.doi) if self.doi else self.name


class ClimateDataSet(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class ClimateVariable(models.Model):
    name = models.CharField(max_length=500)
    abbrevation = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return "%s (%s)" % (self.name, self.abbrevation)


class SocioEconomicInputVariables(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class General(models.Model):
    name = models.CharField(max_length=500)
    region = models.ManyToManyField(Region)
    contact_person = models.ForeignKey(User, null=True, blank=True)
    version = models.CharField(max_length=500, null=True, blank=True)
    main_reference_paper = models.ForeignKey(ReferencePaper, null=True, blank=True, related_name='main_ref')
    additional_papers = models.ManyToManyField(ReferencePaper, blank=True)
    short_description = models.TextField(null=True, blank=True)

    # technical information
    RESOLUTION_CHOICES = ( ('0.5°x0.5°', '0.5°x0.5°'), )
    resolution = ChoiceOrOtherField(max_length=500, choices=RESOLUTION_CHOICES, blank=True, null=True)
    TEMPORAL_RESOLUTION_CLIMATE_CHOICES = (('daily', 'daily'), ('monthly', 'monthly'), ('annual', 'annual'),)
    temporal_resolution_climate = ChoiceOrOtherField(max_length=500, choices=TEMPORAL_RESOLUTION_CLIMATE_CHOICES, blank=True, null=True)
    temporal_resolution_co2 = ChoiceOrOtherField(max_length=500, choices=(('annual', 'annual'),), blank=True, null=True)
    temporal_resolution_land = ChoiceOrOtherField(max_length=500, choices=(('annual', 'annual'),), blank=True, null=True)
    temporal_resolution_soil = ChoiceOrOtherField(max_length=500, choices=(('annual', 'annual'),), blank=True, null=True)

    # input data
    climate_data_sets = models.ManyToManyField(ClimateDataSet, blank=True)
    climate_variables = models.ManyToManyField(ClimateVariable, blank=True)
    socioeconomic_input_variables = models.ManyToManyField(SocioEconomicInputVariables, blank=True)
    soil_dataset = models.TextField(null=True, blank=True, help_text='Soil dataset')
    additional_input_data_sets = models.TextField(null=True, blank=True, help_text='Additional input data sets')

    # other
    exceptions_to_protocol = models.TextField(null=True, blank=True, help_text='Did you have to overrule any settings prescribed by the protocol in order to get your model running?')
    spin_up = models.NullBooleanField(help_text='Did you spin-up your model?')
    spin_up_design = models.TextField(null=True, blank=True, help_text='Spin-up design')
    natural_vegetation_partition = models.TextField(null=True, blank=True, help_text='How are areas covered by different types of natural vegetation partitioned?')
    natural_vegetation_simulation = models.TextField(null=True, blank=True, help_text='Do your simulate your own (dynamic) natural vegetation? If so, please describe')
    natural_vegetation_cover_dataset = models.TextField(null=True, blank=True, help_text='If you prescribe natural vegetation cover, which dataset do you use?')
    management = models.TextField(null=True, blank=True, help_text='What specific management and autonomous adaptation measures did you apply?')
    extreme_events = models.TextField(null=True, blank=True, help_text='Key challenges for model in reproducing impacts of extreme events')
    anything_else = models.TextField(null=True, blank=True, help_text='Anything else necessary to reproduce and/or understand the simulation output')
    comments = models.TextField(null=True, blank=True, help_text='Additional comments')

    CACHE_KEY = "climatemodels/general/sector/%d"

    @property
    def sector(self):
        _sector = cache.get(self.CACHE_KEY % self.id)
        if not _sector:
            for i in Sector.subsectors:
                try:
                    _sector = self.__getattribute__(i)
                    break
                except ObjectDoesNotExist:
                    pass
        cache.set(self.CACHE_KEY % self.id, _sector)
        return _sector

    @sector.setter
    def sector(self, value):
        print(value)

    def __str__(self):
        return "%s (%s)" % (self.name, self.sector)
    # sector = property(get_sector,set_sector)


class Sector(models.Model):
    general = models.OneToOneField(General)

    subsectors = ['agriculture', 'energy', 'water', 'biomes', 'marineecosystems',
                  'biodiversity', 'health', 'coastalinfrastructure', 'permafrost']

    @staticmethod
    def get(name):
        if name.lower().strip() == 'water' or name == Water:
            return Water


    class Meta:
        abstract = True

    def __str__(self):
        return type(self).__name__

    """
    Sektoren:
        Agriculture                                     | Agriculture
        Energy                                          | Energy
        Water (global)                                  | Water
        Water (regional)                                | Water
        Biomes                                          | Biomes
        Forests                                         | Biomes
        Marine Ecosystems and Fisheries (global)        | MarineEcosystems
        Marine Ecosystems and Fisheries (regional)      | MarineEcosystems
        Biodiversity                                    | - General -
        Health                                          | - General -
        Coastal Infrastructure                          | - General -
        Permafrost                                      | - General -
    """


class Agriculture(Sector):
    # Key input and Management
    crops = models.TextField(null=True, blank=True, verbose_name='Crops')
    land_coverage = models.TextField(null=True, blank=True, verbose_name='Land coverage')
    planting_date_decision = models.TextField(null=True, blank=True, verbose_name='Planting date decision')
    planting_density = models.TextField(null=True, blank=True, verbose_name='Planting density')
    crop_cultivars = models.TextField(null=True, blank=True, verbose_name='Crop cultivars')
    fertilizer_application = models.TextField(null=True, blank=True, verbose_name='Fertilizer application')
    irrigation = models.TextField(null=True, blank=True, verbose_name='Irrigation')
    crop_residue = models.TextField(null=True, blank=True, verbose_name='Crop residue')
    initial_soil_water = models.TextField(null=True, blank=True, verbose_name='Initial soil water')
    initial_soil_nitrate_and_ammonia = models.TextField(null=True, blank=True, verbose_name='Initial soil nitrate and ammonia')
    initial_soil_C_and_OM = models.TextField(null=True, blank=True, verbose_name='Initial soil C and OM')
    initial_crop_residue = models.TextField(null=True, blank=True, verbose_name='Initial crop residue')
    # Key model processes
    lead_area_development = models.TextField(null=True, blank=True, verbose_name='Lead area development')
    light_interception = models.TextField(null=True, blank=True, verbose_name='Light interception')
    light_utilization = models.TextField(null=True, blank=True, verbose_name='Light utilization')
    yield_formation = models.TextField(null=True, blank=True, verbose_name='Yield formation')
    crop_phenology = models.TextField(null=True, blank=True, verbose_name='Crop phenology')
    root_distribution_over_depth = models.TextField(null=True, blank=True, verbose_name='Root distribution over depth')
    stresses_involved = models.TextField(null=True, blank=True, verbose_name='Stresses involved')
    type_of_water_stress = models.TextField(null=True, blank=True, verbose_name='Type of water stress')
    type_of_heat_stress = models.TextField(null=True, blank=True, verbose_name='Type of heat stress')
    water_dynamics = models.TextField(null=True, blank=True, verbose_name='Water dynamics')
    evapo_transpiration = models.TextField(null=True, blank=True, verbose_name='Evapo-transpiration')
    soil_CN_modeling = models.TextField(null=True, blank=True, verbose_name='Soil CN modeling')
    co2_effects = models.TextField(null=True, blank=True, verbose_name='CO2 Effects')
    # Methods for model calibration and validation
    parameters_number_and_description = models.TextField(null=True, blank=True, verbose_name='Parameters, number and description')
    calibrated_values = models.TextField(null=True, blank=True, verbose_name='Calibrated values')
    output_variable_and_dataset = models.TextField(null=True, blank=True, verbose_name='Output variable and dataset for calibration validation')
    spatial_scale_of_calibration_validation = models.TextField(null=True, blank=True, verbose_name='Spatial scale of calibration/validation')
    temporal_scale_of_calibration_validation = models.TextField(null=True, blank=True, verbose_name='Temporal scale of calibration/validation')
    criteria_for_evaluation = models.TextField(null=True, blank=True, verbose_name='Criteria for evaluation (validation)')


class Energy(Sector):
    # Model & method characteristics
    model_type = models.TextField(null=True, blank=True, verbose_name='Model type')
    temporal_extent = models.TextField(null=True, blank=True, verbose_name='Temporal extent')
    temporal_resolution = models.TextField(null=True, blank=True, verbose_name='Temporal resolution')
    data_format_for_input = models.TextField(null=True, blank=True, verbose_name='Data format for input')
    #_Impact_Types
    impact_types_energy_demand = models.TextField(null=True, blank=True, verbose_name='Energy demand (heat & cooling)')
    impact_types_temperature_effects_on_thermal_power = models.TextField(null=True, blank=True, verbose_name='temperature effects on thermal power')
    impact_types_weather_effects_on_renewables = models.TextField(null=True, blank=True, verbose_name='Weather effects on renewables')
    impact_types_water_scarcity_impacts = models.TextField(null=True, blank=True, verbose_name='Water scarcity impacts')
    impact_types_other = models.TextField(null=True, blank=True, verbose_name='Other (agriculture, infrastructure, adaptation)')
    #Output
    output_energy_demand = models.TextField(null=True, blank=True, verbose_name='Energy demand (heating & cooling)')
    output_energy_supply = models.TextField(null=True, blank=True, verbose_name='Energy supply')
    output_water_scarcity = models.TextField(null=True, blank=True, verbose_name='Water scarcity')
    output_economics = models.TextField(null=True, blank=True, verbose_name='Economics')
    output_other = models.TextField(null=True, blank=True, verbose_name='Other (agriculture, infrastructure, adaptation)')
    #_Further_information
    variables_not_directly_from_GCMs = models.TextField(null=True, blank=True, verbose_name='Variables not directly from GCMs')
    response_function_of_energy_demand_to_HDD_CDD = models.TextField(null=True, blank=True, verbose_name='Response function of energy demand to HDD/CDD')
    factor_definition_and_calculation = models.TextField(null=True, blank=True, verbose_name='Definition and calculation of variable potential and load factor')
    biomass_types = models.TextField(null=True, blank=True, verbose_name='Biomass types')
    maximum_potential_assumption = models.TextField(null=True, blank=True, verbose_name='Maximum potential assumption')
    bioenergy_supply_costs = models.TextField(null=True, blank=True, verbose_name='Bioenergy supply costs')
    socioeconomic_input = models.TextField(null=True, blank=True, verbose_name='Socio-economic input')


class Water(Sector):
    technological_progress = models.TextField(null=True, blank=True, help_text='Does your model account for GDP changes and technological progress? If so, how?')
    soil = models.TextField(null=True, blank=True, help_text='How many soil layers are there?')
    water_use = models.TextField(null=True, blank=True, help_text='What types of water use can your model include?')
    water_sectors = models.TextField(null=True, blank=True, help_text='For the global water model varsoc and pressoc runs, which water sectors did you include?')
    routing = models.TextField(null=True, blank=True, help_text='How do you route runoff in your model?')
    routing_data = models.TextField(null=True, blank=True, help_text='What routing data do you use?')
    land_use = models.TextField(null=True, blank=True, help_text='What effects of land-use change does your model include?')
    dams_reservoirs = models.TextField(null=True, blank=True, help_text='How are dams and reservoirs implemented?')
    calibration = models.NullBooleanField(help_text='Was the model calibrated?')

    calibration_years = models.TextField(null=True, blank=True, help_text='Which years were used for calibration?')
    calibration_dataset = models.TextField(null=True, blank=True, help_text='Which dataset was used for calibration?')
    calibration_catchments = models.TextField(null=True, blank=True, help_text='How many catchments was the calibration carried out?')
    vegetation = models.NullBooleanField(help_text='Do you account for CO2 fertilisation?')
    vegetation_presentation = models.TextField(null=True, blank=True, help_text='How is vegetation represented?')
    methods_evapotraspiration = models.TextField(null=True, blank=True, help_text='Potential evapotraspiration')
    methods_snowmelt = models.TextField(null=True, blank=True, help_text='Snow melt')


class Biomes(Sector):
    # technological_progress = models.TextField(null=True, blank=True)
    output = models.TextField(null=True, blank=True)
    output_per_pft = models.TextField(null=True, blank=True)
    considerations = models.TextField(null=True, blank=True, help_text='Things to consider, when calculating basic variables such as GPP, NPP, RA, RH from your modeling')
    # key model processes
    dynamic_vegetation = models.TextField(null=True, blank=True)
    nitrogen_limitation = models.TextField(null=True, blank=True)
    co2_effects = models.TextField(null=True, blank=True)
    light_interception = models.TextField(null=True, blank=True)
    light_utilization = models.TextField(null=True, blank=True)
    phenology = models.TextField(null=True, blank=True)
    water_stress = models.TextField(null=True, blank=True)
    heat_stress = models.TextField(null=True, blank=True)
    evapotranspiration_approaches = models.TextField(verbose_name='Evapo-transpiration approaches', null=True, blank=True)
    rooting_depth_differences = models.TextField(verbose_name='Differences in rooting depth', null=True, blank=True)
    root_distribution = models.TextField(verbose_name='Root distribution over depth', null=True, blank=True)
    permafrost = models.TextField(null=True, blank=True)
    closed_energy_balance = models.TextField(null=True, blank=True)
    soil_moisture_surface_temperature_coupling = models.TextField(null=True, blank=True)
    latent_heat = models.TextField(null=True, blank=True)
    sensible_heat = models.TextField(null=True, blank=True)
    # causes of mortality in vegetation models
    mortality_age = models.TextField(verbose_name='Age', null=True, blank=True)
    mortality_fire = models.TextField(verbose_name='Fire', null=True, blank=True)
    mortality_drought = models.TextField(verbose_name='Drought', null=True, blank=True)
    mortality_insects = models.TextField(verbose_name='Insects', null=True, blank=True)
    mortality_storm = models.TextField(verbose_name='Storm', null=True, blank=True)
    mortality_stochastic_random_disturbance = models.TextField(verbose_name='Stochastic random disturbance', null=True, blank=True)
    mortality_other = models.TextField(verbose_name='Other', null=True, blank=True)
    mortality_remarks = models.TextField(verbose_name='Remarks', null=True, blank=True)
    # NBP components
    nbp_fire = models.TextField(null=True, blank=True, verbose_name='Fire')
    nbp_landuse_change = models.TextField(null=True, blank=True, verbose_name='Land-use change')
    nbp_harvest = models.TextField(null=True, blank=True, verbose_name='Hharvest')
    nbp_other = models.TextField(null=True, blank=True, verbose_name='Other')
    nbp_comments = models.TextField(null=True, blank=True, verbose_name='Comments')
    # Plant Functional Types (PFTs)
    list_of_pfts = models.TextField(null=True, blank=True, verbose_name='List of PFTs')
    pfts_comments = models.TextField(null=True, blank=True, verbose_name='Comments')


class MarineEcosystems(Sector):
    defining_features = models.TextField(null=True, blank=True, verbose_name='Defining features')
    spatial_scale = models.TextField(null=True, blank=True, verbose_name='Spatial scale')
    spatial_resolution = models.TextField(null=True, blank=True, verbose_name='Spatial resolution')
    temporal_scale = models.TextField(null=True, blank=True, verbose_name='Temporal scale')
    temporal_resolution = models.TextField(null=True, blank=True, verbose_name='Temporal resolution')
    taxonomic_scope = models.TextField(null=True, blank=True, verbose_name='Taxonomic scope')
    vertical_resolution = models.TextField(null=True, blank=True, verbose_name='Vertical resolution')
    spatial_dispersal_included = models.TextField(null=True, blank=True, verbose_name='Spatial dispersal included')
    fishbase_used_for_mass_length_conversion = models.TextField(null=True, blank=True, verbose_name='FishBase used for mass-length conversion')


class Biodiversity(Sector): pass
class Health(Sector): pass
class CoastalInfrastructure(Sector): pass
class Permafrost(Sector): pass