from django.apps import apps
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from isi_mip.choiceorotherfield.models import ChoiceOrOtherField


class Region(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name


class ReferencePaper(models.Model):
    name = models.CharField(max_length=500)
    doi = models.CharField(max_length=500, null=True, blank=True, unique=True)

    def __str__(self):
        return "%s (%s)" % (self.name, self.doi) if self.doi else self.name


class ClimateDataType(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name


class ClimateVariable(models.Model):
    name = models.CharField(max_length=500)
    abbrevation = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return "%s (%s)" % (self.name, self.abbrevation)


class InputPhase(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name


class SocioEconomicInputVariables(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name


class Scenario(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name

class SpatialAggregation(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name

class ContactPerson(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    institute = models.CharField(max_length=500, null=True, blank=True)
    impact_model = models.ForeignKey('ImpactModel', null=True, blank=True)

    def __str__(self):
        return "%s (%s) - %s" % (self.name, self.institute, self.email)


class InputData(models.Model):
    data_set = models.CharField(max_length=500, unique=True)
    data_type = models.ForeignKey(ClimateDataType, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    phase = models.ForeignKey(InputPhase, null=True, blank=True)

    def __str__(self):
        return self.data_set

    class Meta:
        verbose_name_plural = 'Input data'


class SimulationRound(models.Model):
    name = models.CharField(max_length=500, unique=True)
    def __str__(self):
        return self.name


class ImpactModel(models.Model):
    name = models.CharField(max_length=500)
    SECTOR_CHOICES = (
        ('Agriculture', 'Agriculture'),
        ('Energy', 'Energy'),
        ('Water (global)', 'Water (global)'),
        ('Water (regional)', 'Water (regional)'),
        ('Biomes', 'Biomes'),
        ('Forests', 'Forests'),
        ('Marine Ecosystems and Fisheries (global)', 'Marine Ecosystems and Fisheries (global)'),
        ('Marine Ecosystems and Fisheries (regional)', 'Marine Ecosystems and Fisheries (regional)'),
        ('Biodiversity', 'Biodiversity'),
        ('Health', 'Health'),
        ('Coastal Infrastructure', 'Coastal Infrastructure'),
        ('Permafrost', 'Permafrost'),
    )
    sector = models.CharField(max_length=500, choices=SECTOR_CHOICES)
    region = models.ManyToManyField(Region, help_text="For which regions does the model produce results?")
    # contact_person = models.ForeignKey(ContactPerson, null=True, blank=True)
    simulation_round = models.ManyToManyField(
        SimulationRound, blank=True,
        help_text="For which ISIMIP simulation round are these model details relevant?"
    )
    version = models.CharField(max_length=500, null=True, blank=True, verbose_name='Model Version')
    main_reference_paper = models.ForeignKey(
        ReferencePaper, null=True, blank=True, related_name='main_ref',
        help_text="The single paper that should be cited when referring to simulation output from this model")
    other_references = models.ManyToManyField(ReferencePaper, blank=True)
    short_description = models.TextField(
        null=True, blank=True, verbose_name="Short model description",
        help_text="This short description should assist other researchers in briefly describing the model in a paper.")

    # technical information
    spatial_aggregation = models.ForeignKey(SpatialAggregation, null=True, blank=True,
                                           help_text="e.g. regular grid, points, hyrdotopes...")
    resolution = ChoiceOrOtherField(
        max_length=500, choices=(('0.5°x0.5°', '0.5°x0.5°'),), blank=True, null=True,
        help_text="The spatial resolution at which the ISIMIP simulations were run, if on a regular grid. Data was provided on a 0.5°x0.5° grid")
    TEMPORAL_RESOLUTION_CLIMATE_CHOICES = (('daily', 'daily'), ('monthly', 'monthly'), ('annual', 'annual'),)
    temporal_resolution_climate = ChoiceOrOtherField(
        max_length=500, choices=TEMPORAL_RESOLUTION_CLIMATE_CHOICES, blank=True, null=True,
        help_text="ISIMIP data was provided in daily time steps")
    temporal_resolution_co2 = ChoiceOrOtherField(max_length=500, choices=(('annual', 'annual'),), blank=True, null=True,
                                                 help_text="ISIMIP data was provided in annual time steps")
    temporal_resolution_land = ChoiceOrOtherField(max_length=500, choices=(('annual', 'annual'),), blank=True, null=True,
                                                  help_text="ISIMIP data was provided in annual time steps")
    temporal_resolution_soil = ChoiceOrOtherField(max_length=500, choices=(('constant', 'constant'),), blank=True, null=True,
                                                  help_text="ISIMIP data was constant in time")

    # input data
    climate_data_sets = models.ManyToManyField(InputData, blank=True, verbose_name="Climate data sets used",
                                               help_text="The climate-input data sets used in this simulation round")
    climate_variables = models.ManyToManyField(
        ClimateVariable, blank=True,
        help_text="Include variables that were derived from those provided in the ISIMIP input data set")
    socioeconomic_input_variables = models.ManyToManyField(
        SocioEconomicInputVariables, blank=True, verbose_name="Socio-economic input variables",
        help_text="Include resolution if relevant"
    )
    soil_dataset = models.TextField(null=True, blank=True, help_text="HWSD or GSWP3 were provided")
    additional_input_data_sets = models.TextField(
        null=True, blank=True,
        help_text='List here any data sets used to drive the model that were not provided by ISIMIP'
    )

    # other
    exceptions_to_protocol = models.TextField(
        null=True, blank=True,
        help_text='Were any settings prescribed by the protocol overruled in order to run the model?'
    )
    spin_up = models.NullBooleanField(
        verbose_name='Did you spin-up your model?',
        help_text="`No` indicates the simulations were run starting in the first reporting year 1971"
    )
    spin_up_design = models.TextField(
        null=True, blank=True, verbose_name='Spin-up design',
        help_text="Include the length of the spin up, the CO2 concentration used, and any deviations from the spin-up procedure defined in the protocol."
    )
    natural_vegetation_partition = models.TextField(
        null=True, blank=True, help_text='How are areas covered by different types of natural vegetation partitioned?'
    )
    natural_vegetation_dynamics = models.TextField(
        null=True, blank=True,
        help_text='Is natural vegetation simulated dynamically? If so, please describe.'
    )
    natural_vegetation_cover_dataset = models.TextField(
        null=True, blank=True, help_text='If natural vegetation cover is prescribed, which dataset is used?'
    )
    management = models.TextField(
        null=True, blank=True,
        help_text='Which specific management and autonomous adaptation measures were applied? E.g. varying sowing dates in crop modles, dbh-related harvesting in forest models.'
    )
    extreme_events = models.TextField(
        null=True, blank=True,
        help_text='Which are the key challenges for this model in reproducing impacts of extreme events?'
    )
    anything_else = models.TextField(
        null=True, blank=True, help_text='Anything else necessary to reproduce and/or understand the simulation output'
    )
    comments = models.TextField(null=True, blank=True, verbose_name='Additional comments')

    owner = models.ForeignKey(User)


    CACHE_KEY = "climatemodels/impact_model/sector/%d"

    @property
    def fk_sector(self):
        sector = SECTOR_MAPPING[self.sector]
        sectorname = sector._meta.label_lower.rsplit('.')[-1]
        return getattr(self, sectorname)
        # TODO: check if the upper doesnt hit the database like the lower does.
        # return sector.objects.get(impact_model=self)

    def __str__(self):
        return "%s (%s)" % (self.name, self.sector)

    def save(self, *args, **kwargs):
        if not self.owner_id:
            self.owner_id = 1
        # if self.sector:
        #     if ImpactModel.objects.get(id=self.pk).sector != self.sector:
        #         import ipdb; ipdb.set_trace()
        super(ImpactModel, self).save(*args, **kwargs) # Call the "real" save() method.
        SECTOR_MAPPING[self.sector].objects.get_or_create(impact_model=self)

    class Meta:
        unique_together = ('name', 'sector')
        # verbose_name_plural = 'Impact Models'


class Sector(models.Model):
    impact_model = models.OneToOneField(ImpactModel)

    subsectors = ['agriculture', 'energy', 'water', 'biomes', 'marineecosystems',
                  'biodiversity', 'health', 'coastalinfrastructure', 'permafrost']

    @staticmethod
    def get(name):
        name = name.lower().strip()
        if "agriculture" in name:
            return Agriculture
        if "energy" in name:
            return Energy
        if "water" in name:
            return Water
        if "biomes" in name:
            return Biomes
        if "forests" in name:
            return Biomes
        if "marine" in name:
            return MarineEcosystems
        if "biodiversity" in name:
            return Biodiversity
        if "health" in name:
            return Health
        if "coastal" in name:
            return CoastalInfrastructure
        if "permafrost" in name:
            return Permafrost
        raise Exception("Couldn't match sector type")

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
    # Key input and Management # TODO: help_text="Provide a yes/no answer and a short description of how the process is included"
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
    # Key model processes TODO: "Please specify methods for model calibration and validation"
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
    # Methods for model calibration and validation # TODO: "Please specify methods for model calibration and validation"
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
    impact_types_energy_demand = models.TextField(null=True, blank=True, verbose_name='Energy demand (heating & cooling)')
    impact_types_temperature_effects_on_thermal_power = models.TextField(null=True, blank=True, verbose_name='Temperature effects on thermal power')
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
    technological_progress = models.TextField(
        null=True, blank=True,
        help_text='Does the model account for GDP changes and technological progress? If so, how are these integrated into the runs?'
    )
    soil_layers = models.TextField(null=True, blank=True,
                                   help_text='How many soil layers are used? Which qualities do they have?')
    water_use = models.TextField(null=True, blank=True, verbose_name='Water-use types',
                                 help_text='Which types of water use are included?')
    water_sectors = models.TextField(
        null=True, blank=True, verbose_name='Water-use sectors',
        help_text='For the global-water-model varsoc and pressoc runs, which water sectors were included? E.g. irrigation, domestic, manufacturing, electricity, livestock.')
    routing = models.TextField(null=True, blank=True, verbose_name='Runoff routing', help_text='How is runoff routed?')
    routing_data = models.TextField(null=True, blank=True, help_text='Which routing data are used?')
    land_use = models.TextField(null=True, blank=True, verbose_name='Land-use change effects',
                                help_text='Which land-use change effects are included?')
    dams_reservoirs = models.TextField(null=True, blank=True, verbose_name='Dams & Reservoirs',
                                       help_text='Describe how are dams and reservoirs are implemented')

    calibration = models.BooleanField(verbose_name='Was the model calibrated?', default=False)
    calibration_years = models.TextField(null=True, blank=True, verbose_name='Which years were used for calibration?')
    calibration_dataset = models.TextField(null=True, blank=True, verbose_name='Which dataset was used for calibration?',
                                           help_text='E.g. WFD, GSWP3')
    calibration_catchments = models.TextField(null=True, blank=True,
                                              verbose_name='How many catchments were callibrated?')
    vegetation = models.BooleanField(verbose_name='Is CO2 fertilisation accounted for?', default=False)
    vegetation_representation = models.TextField(null=True, blank=True, verbose_name='How is vegetation represented?')
    methods_evapotraspiration = models.TextField(null=True, blank=True, verbose_name='Potential evapotraspiration')
    methods_snowmelt = models.TextField(null=True, blank=True, verbose_name='Snow melt')


class Biomes(Sector):
    # technological_progress = models.TextField(null=True, blank=True)
    output = models.TextField(
        null=True, blank=True, verbose_name='Output format',
        help_text='Is output (e.g. PFT cover) written out per grid-cell area or per land and water area within a grid cell, or land only?'
    )
    output_per_pft = models.TextField(
        null=True, blank=True,
        help_text='Is output per PFT per unit area of that PFT, i.e. requiring weighting by the fractional coverage of each PFT to get the gridbox average?'
    )
    considerations = models.TextField(
        null=True, blank=True,
        help_text='Things to consider, when calculating basic variables such as GPP, NPP, RA, RH from the model.'
    )
    # key model processes # TODO: help_text="Please provide yes/no and a short description how the process is included"
    dynamic_vegetation = models.TextField(null=True, blank=True)
    nitrogen_limitation = models.TextField(null=True, blank=True)
    co2_effects = models.TextField(null=True, blank=True)
    light_interception = models.TextField(null=True, blank=True)
    light_utilization = models.TextField(null=True, blank=True, help_text="photosynthesis, RUE- approach?")
    phenology = models.TextField(null=True, blank=True)
    water_stress = models.TextField(null=True, blank=True)
    heat_stress = models.TextField(null=True, blank=True)
    evapotranspiration_approach = models.TextField(verbose_name='Evapo-transpiration approach', null=True, blank=True)
    rooting_depth_differences = models.TextField(verbose_name='Differences in rooting depth', null=True, blank=True,
                                                 help_text="Include how it changes.")
    root_distribution = models.TextField(verbose_name='Root distribution over depth', null=True, blank=True)
    permafrost = models.TextField(null=True, blank=True)
    closed_energy_balance = models.TextField(null=True, blank=True)
    soil_moisture_surface_temperature_coupling = models.TextField(
        null=True, blank=True, verbose_name='Coupling/feedback between soil moisture and surface temperature')
    latent_heat = models.TextField(null=True, blank=True)
    sensible_heat = models.TextField(null=True, blank=True)
    # causes of mortality in vegetation models # TODO: help_text="Describe briefly how the process is described in this model and in which way it is climate dependent."
    mortality_age = models.TextField(verbose_name='Age', null=True, blank=True)
    mortality_fire = models.TextField(verbose_name='Fire', null=True, blank=True)
    mortality_drought = models.TextField(verbose_name='Drought', null=True, blank=True)
    mortality_insects = models.TextField(verbose_name='Insects', null=True, blank=True)
    mortality_storm = models.TextField(verbose_name='Storm', null=True, blank=True)
    mortality_stochastic_random_disturbance = models.TextField(verbose_name='Stochastic random disturbance', null=True, blank=True)
    mortality_other = models.TextField(verbose_name='Other', null=True, blank=True)
    mortality_remarks = models.TextField(verbose_name='Remarks', null=True, blank=True)
    # NBP components # TODO: "Indicate whether the model includes the processes, and how the model accounts for the fluxes, i.e.what is the fate of the biomass? E.g.directly to atmsphere or let it go to other pool"
    nbp_fire = models.TextField(null=True, blank=True, verbose_name='Fire')
    nbp_landuse_change = models.TextField(null=True, blank=True, verbose_name='Land-use change',
                                          help_text="Deforestation, harvest and other land-use changes")
    nbp_harvest = models.TextField(
        null=True, blank=True, verbose_name='Harvest',
        help_text="1: crops, 2: harvest from forest management, 3: harvest from grassland management"
    )
    nbp_other = models.TextField(null=True, blank=True, verbose_name='Other processes')
    nbp_comments = models.TextField(null=True, blank=True, verbose_name='Comments')
    # Plant Functional Types (PFTs)
    list_of_pfts = models.TextField(
        null=True, blank=True, verbose_name='List of PFTs',
        help_text="Provide a list of PFTs using the folllowing format: <pft1_long_name> (<pft1_short_name>); <pft2_long_name> (<pft2_short_name>). Include long name in brackets if no short name is available."
    )
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
    fishbase_used_for_mass_length_conversion = models.TextField(
        null=True, blank=True, verbose_name='Is FishBase used for mass-length conversion?')


class Biodiversity(Sector): pass
class Health(Sector): pass
class CoastalInfrastructure(Sector): pass
class Permafrost(Sector): pass


class OutputData(models.Model):
    sector = models.CharField(max_length=500, choices=ImpactModel.SECTOR_CHOICES)
    model = models.ForeignKey(ImpactModel)
    scenario = models.ForeignKey(Scenario)
    drivers = models.ManyToManyField(InputData)
    date = models.DateField()

    def __str__(self):
        return "%s : %s : %s" % (self.sector, self.model.name, self.scenario.name)

    class Meta:
        verbose_name_plural = 'Output data'


SECTOR_MAPPING ={
    'Agriculture': Agriculture,
    'Energy': Energy,
    'Water (global)': Water,
    'Water (regional)': Water,
    'Biomes': Biomes,
    'Forests': Biomes,
    'Marine Ecosystems and Fisheries (global)': MarineEcosystems,
    'Marine Ecosystems and Fisheries (regional)': MarineEcosystems,
    'Biodiversity': Biodiversity,
    'Health': Health,
    'Coastal Infrastructure': CoastalInfrastructure,
    'Permafrost': Permafrost
}
