from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models

from isi_mip.choiceorotherfield.models import ChoiceOrOtherField
from isi_mip.sciencepaper.models import Paper


class Region(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )


class ReferencePaper(Paper):
    def __str__(self):
        if self.doi:
            return "%s (<a target='_blank' href='http://dx.doi.org/%s'>%s</a>)" % (self.title, self.doi, self.doi)
        else:
            return self.title


class ClimateDataType(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class ClimateVariable(models.Model):
    name = models.CharField(max_length=500, unique=True)
    abbreviation = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        if self.abbreviation:
            return '{0.name} ({0.abbreviation})'.format(self)
        return self.name


    def as_span(self):
        if self.abbreviation:
            return '<abbr title="{0.name}">{0.abbreviation}</abbr>'.format(self)
        return self.name

    class Meta:
        ordering = ('name',)


class InputPhase(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class SocioEconomicInputVariables(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Socio-economic input variable'
        ordering = ('name', )


class Scenario(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class SpatialAggregation(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class ContactPerson(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    institute = models.CharField(max_length=500, null=True, blank=True)
    impact_model = models.ForeignKey('ImpactModel', null=True, blank=True)

    def __str__(self):
        return "%s (%s) - %s" % (self.name, self.institute, self.email)

    class Meta:
        ordering = ('name',)


class InputData(models.Model):
    name = models.CharField(max_length=500, unique=True)
    data_type = models.ForeignKey(ClimateDataType, null=True, blank=True)
    scenario = models.ForeignKey(Scenario, null=True, blank=True)
    variables = models.ManyToManyField(ClimateVariable, blank=True)
    phase = models.ForeignKey(InputPhase, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    caveats = models.TextField(null=True, blank=True)
    download_instructions = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Input data'
        ordering = ('name',)


class SimulationRound(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class ImpactModel(models.Model):
    name = models.CharField(max_length=500)
    SECTOR_CHOICES = (
        ('Agriculture', 'Agriculture'),
        ('Agro-Economic Modelling', 'Agro-Economic Modelling'),
        ('Biodiversity', 'Biodiversity'),
        ('Biomes', 'Biomes'),
        ('Coastal Infrastructure', 'Coastal Infrastructure'),
        ('Computable General Equilibrium Modelling', 'Computable General Equilibrium Modelling'),
        ('Energy', 'Energy'),
        ('Forests', 'Forests'),
        ('Health', 'Health'),
        ('Marine Ecosystems and Fisheries (global)', 'Marine Ecosystems and Fisheries (global)'),
        ('Marine Ecosystems and Fisheries (regional)', 'Marine Ecosystems and Fisheries (regional)'),
        ('Permafrost', 'Permafrost'),
        ('Water (global)', 'Water (global)'),
        ('Water (regional)', 'Water (regional)'),
    )
    sector = models.CharField(max_length=500, choices=SECTOR_CHOICES)
    region = models.ManyToManyField(Region, help_text="For which regions does the model produce results?")
    # contact_person = models.ForeignKey(ContactPerson, null=True, blank=True)
    simulation_round = models.ManyToManyField(
        SimulationRound, blank=True,
        help_text="For which ISIMIP simulation round are these model details relevant?"
    )
    version = models.CharField(max_length=500, null=True, blank=True, verbose_name='Model version')
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
    spatial_resolution = ChoiceOrOtherField(
        max_length=500, choices=(('0.5°x0.5°', '0.5°x0.5°'),), blank=True, null=True, verbose_name='Spatial Resolution',
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
    NA_YES_NO = ((None, '---------'), (True, 'Yes'), (False, 'No'))
    spin_up = models.NullBooleanField(
        verbose_name='Did you spin-up your model?',
        help_text="'No' indicates the simulations were run starting in the first reporting year 1971",
        choices=NA_YES_NO
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

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('name', 'sector')
        ordering = ('name', )
        # verbose_name_plural = 'Impact Models'

    def save(self, *args, **kwargs):
        if not self.owner_id:
            self.owner_id = 1
        # if self.sector:
        #     if ImpactModel.objects.get(id=self.pk).sector != self.sector:
        #         import ipdb; ipdb.set_trace()
        super().save(*args, **kwargs)
        SECTOR_MAPPING[self.sector].objects.get_or_create(impact_model=self)

    def __str__(self):
        return "%s (%s)" % (self.name, self.sector)

    @property
    def fk_sector_name(self):
        sector = SECTOR_MAPPING[self.sector]
        sectorname = sector._meta.label_lower.rsplit('.')[-1]
        return sectorname

    @property
    def fk_sector(self):
        return getattr(self, self.fk_sector_name)

    def _get_verbose_field_name(self, field: str) -> str:
        return self._meta.get_field_by_name(field)[0].verbose_name.title()

    def values_to_tuples(self) -> list:
        vname = self._get_verbose_field_name
        cpers_str = "{0.name} (<a href='mailto:{0.email}'>{0.email}</a>) {0.institute}"
        cpers = ', '.join([cpers_str.format(x) for x in self.contactperson_set.all()])
        return [
            ('Basic information', [
                # (vname('name'), self.name),
                (vname('sector'), self.sector),
                (vname('region'), ' '.join([x.name for x in self.region.all()])),
                ('Contact Person', cpers),
                (vname('simulation_round'), ' '.join([x.name for x in self.simulation_round.all()])),
                (vname('version'), self.version),
                # (vname('main_reference_paper'), self.main_reference_paper),
                # (vname('short_description'), self.short_description),
            ]),
            ('Technical Information', [
                (vname('spatial_aggregation'), self.spatial_aggregation),
                (vname('spatial_resolution'), self.spatial_resolution),
                (vname('temporal_resolution_climate'), self.temporal_resolution_climate),
                (vname('temporal_resolution_co2'), self.temporal_resolution_co2),
                (vname('temporal_resolution_land'), self.temporal_resolution_land),
                (vname('temporal_resolution_soil'), self.temporal_resolution_soil),
            ]),
            ('Input Data', [
                (vname('climate_data_sets'), ' '.join([x.name for x in self.climate_data_sets.all()])),
                (vname('climate_variables'), ' '.join([x.as_span() for x in self.climate_variables.all()])),
                (vname('socioeconomic_input_variables'), ' '.join([x.name for x in self.socioeconomic_input_variables.all()])),
                (vname('soil_dataset'), self.soil_dataset),
                (vname('additional_input_data_sets'), self.additional_input_data_sets),
            ]),
            ('Other', [
                (vname('exceptions_to_protocol'), self.exceptions_to_protocol),
                (vname('spin_up'), 'Yes' if self.spin_up else 'No'),
                (vname('spin_up_design'), self.spin_up_design if self.spin_up else ''),
                (vname('natural_vegetation_partition'), self.natural_vegetation_partition),
                (vname('natural_vegetation_dynamics'), self.natural_vegetation_dynamics),
                (vname('natural_vegetation_cover_dataset'), self.natural_vegetation_cover_dataset),
                (vname('management'), self.management),
                (vname('extreme_events'), self.extreme_events),
                (vname('anything_else'), self.anything_else),
                (vname('comments'), self.comments),
            ])
        ]


class Sector(models.Model):
    impact_model = models.OneToOneField(ImpactModel)

    @staticmethod
    def get(name: str):
        name = name.lower().strip()
        if "agriculture" in name:
            return Agriculture
        if "energy" in name:
            return Energy
        if "water" in name:
            if "regional" in name:
                return WaterRegional
            return WaterGlobal
        if "biomes" in name:
            return Biomes
        if "forests" in name:
            return Forests
        if "marine" in name:
            if "regional" in name:
                return MarineEcosystemsRegional
            return MarineEcosystemsGlobal
        if "biodiversity" in name:
            return Biodiversity
        if "health" in name:
            return Health
        if "coastal" in name or "infrastructure" in name:
            return CoastalInfrastructure
        if "permafrost" in name:
            return Permafrost
        if "equilibrium":
            return ComputableGeneralEquilibriumModelling
        if "agro-economic" in name:
            return AgroEconomicModelling
        raise Exception("Couldn't match sector type:", name)

    class Meta:
        abstract = True

    def __str__(self):
        return type(self).__name__

    def _get_verbose_field_name(self, field: str) -> str:
        return self._meta.get_field_by_name(field)[0].verbose_name.title()

    def values_to_tuples(self) -> list:
        return []


class Agriculture(Sector):
    # Key input and Management, help_text="Provide a yes/no answer and a short description of how the process is included"
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
    # Key model processes, help_text="Please specify methods for model calibration and validation"
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
    # Methods for model calibration and validation , help_text="Please specify methods for model calibration and validation"
    parameters_number_and_description = models.TextField(null=True, blank=True, verbose_name='Parameters, number and description')
    calibrated_values = models.TextField(null=True, blank=True, verbose_name='Calibrated values')
    output_variable_and_dataset = models.TextField(null=True, blank=True, verbose_name='Output variable and dataset for calibration validation')
    spatial_scale_of_calibration_validation = models.TextField(null=True, blank=True, verbose_name='Spatial scale of calibration/validation')
    temporal_scale_of_calibration_validation = models.TextField(null=True, blank=True, verbose_name='Temporal scale of calibration/validation')
    criteria_for_evaluation = models.TextField(null=True, blank=True, verbose_name='Criteria for evaluation (validation)')

    def values_to_tuples(self) -> list:
        vname = self._get_verbose_field_name
        return [
            ('Key input and Management', [
                (vname('crops'), self.crops),
                (vname('land_coverage'), self.land_coverage),
                (vname('planting_date_decision'), self.planting_date_decision),
                (vname('planting_density'), self.planting_density),
                (vname('crop_cultivars'), self.crop_cultivars),
                (vname('fertilizer_application'), self.fertilizer_application),
                (vname('irrigation'), self.irrigation),
                (vname('crop_residue'), self.crop_residue),
                (vname('initial_soil_water'), self.initial_soil_water),
                (vname('initial_soil_nitrate_and_ammonia'), self.initial_soil_nitrate_and_ammonia),
                (vname('initial_soil_C_and_OM'), self.initial_soil_C_and_OM),
                (vname('initial_crop_residue'), self.initial_crop_residue)
            ]),
            ('Key model processes', [
                (vname('lead_area_development'), self.lead_area_development),
                (vname('light_interception'), self.light_interception),
                (vname('light_utilization'), self.light_utilization),
                (vname('yield_formation'), self.yield_formation),
                (vname('crop_phenology'), self.crop_phenology),
                (vname('root_distribution_over_depth'), self.root_distribution_over_depth),
                (vname('stresses_involved'), self.stresses_involved),
                (vname('type_of_water_stress'), self.type_of_water_stress),
                (vname('type_of_heat_stress'), self.type_of_heat_stress),
                (vname('water_dynamics'), self.water_dynamics),
                (vname('evapo_transpiration'), self.evapo_transpiration),
                (vname('soil_CN_modeling'), self.soil_CN_modeling),
                (vname('co2_effects'), self.co2_effects),
            ]),
            ('Methods for model calibration and validation', [
                (vname('parameters_number_and_description'), self.parameters_number_and_description),
                (vname('calibrated_values'), self.calibrated_values),
                (vname('output_variable_and_dataset'), self.output_variable_and_dataset),
                (vname('spatial_scale_of_calibration_validation'), self.spatial_scale_of_calibration_validation),
                (vname('temporal_scale_of_calibration_validation'), self.temporal_scale_of_calibration_validation),
                (vname('criteria_for_evaluation'), self.criteria_for_evaluation)
            ])
        ]


class BiomesForests(Sector):
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
    # key model processes , help_text="Please provide yes/no and a short description how the process is included"
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
    # causes of mortality in vegetation models , help_text="Describe briefly how the process is described in this model and in which way it is climate dependent."
    mortality_age = models.TextField(verbose_name='Age', null=True, blank=True)
    mortality_fire = models.TextField(verbose_name='Fire', null=True, blank=True)
    mortality_drought = models.TextField(verbose_name='Drought', null=True, blank=True)
    mortality_insects = models.TextField(verbose_name='Insects', null=True, blank=True)
    mortality_storm = models.TextField(verbose_name='Storm', null=True, blank=True)
    mortality_stochastic_random_disturbance = models.TextField(verbose_name='Stochastic random disturbance', null=True, blank=True)
    mortality_other = models.TextField(verbose_name='Other', null=True, blank=True)
    mortality_remarks = models.TextField(verbose_name='Remarks', null=True, blank=True)
    # NBP components , help_text="Indicate whether the model includes the processes, and how the model accounts for the fluxes, i.e.what is the fate of the biomass? E.g.directly to atmsphere or let it go to other pool"
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

    def values_to_tuples(self) -> list:
        vname = self._get_verbose_field_name
        return [
            ('Model output specifications', [
                (vname('output'), self.output),
                (vname('output_per_pft'), self.output_per_pft),
                (vname('considerations'), self.considerations),
                ]),
            ('Key model processes', [
                (vname('dynamic_vegetation'), self.dynamic_vegetation),
                (vname('nitrogen_limitation'), self.nitrogen_limitation),
                (vname('co2_effects'), self.co2_effects),
                (vname('light_interception'), self.light_interception),
                (vname('light_utilization'), self.light_utilization),
                (vname('phenology'), self.phenology),
                (vname('water_stress'), self.water_stress),
                (vname('heat_stress'), self.heat_stress),
                (vname('evapotranspiration_approach'), self.evapotranspiration_approach),
                (vname('rooting_depth_differences'), self.rooting_depth_differences),
                (vname('root_distribution'), self.root_distribution),
                (vname('permafrost'), self.permafrost),
                (vname('closed_energy_balance'), self.closed_energy_balance),
                (vname('soil_moisture_surface_temperature_coupling'), self.soil_moisture_surface_temperature_coupling),
                (vname('latent_heat'), self.latent_heat),
                (vname('sensible_heat'), self.sensible_heat),
            ]),
            ('Causes of mortality in vegetation models', [
                (vname('mortality_age'), self.mortality_age),
                (vname('mortality_fire'), self.mortality_fire),
                (vname('mortality_drought'), self.mortality_drought),
                (vname('mortality_insects'), self.mortality_insects),
                (vname('mortality_storm'), self.mortality_storm),
                (vname('mortality_stochastic_random_disturbance'), self.mortality_stochastic_random_disturbance),
                (vname('mortality_other'), self.mortality_other),
                (vname('mortality_remarks'), self.mortality_remarks),
            ]),
            ('NBP components', [
                (vname('nbp_fire'), self.nbp_fire),
                (vname('nbp_landuse_change'), self.nbp_landuse_change),
                (vname('nbp_harvest'), self.nbp_harvest),
                (vname('nbp_other'), self.nbp_other),
                (vname('nbp_comments'), self.nbp_comments),
            ]),
            ('Plant Functional Types (PFTs)', [
                (vname('list_of_pfts'), self.list_of_pfts),
                (vname('pfts_comments'), self.pfts_comments),
            ])
        ]

    class Meta:
        abstract = True
class Biomes(BiomesForests):
    class Meta:
        verbose_name_plural = 'Biomes'
        verbose_name = 'Biomes'
class Forests(BiomesForests):
    class Meta:
        verbose_name_plural = 'Forests'
        verbose_name = 'Forests'


class Energy(Sector):
    # Model & Method Characteristics
    model_type = models.TextField(null=True, blank=True, verbose_name='Model type')
    temporal_extent = models.TextField(null=True, blank=True, verbose_name='Temporal extent')
    temporal_resolution = models.TextField(null=True, blank=True, verbose_name='Temporal resolution')
    data_format_for_input = models.TextField(null=True, blank=True, verbose_name='Data format for input')
    # Impact Types
    impact_types_energy_demand = models.TextField(null=True, blank=True, verbose_name='Energy demand (heating & cooling)')
    impact_types_temperature_effects_on_thermal_power = models.TextField(null=True, blank=True, verbose_name='Temperature effects on thermal power')
    impact_types_weather_effects_on_renewables = models.TextField(null=True, blank=True, verbose_name='Weather effects on renewables')
    impact_types_water_scarcity_impacts = models.TextField(null=True, blank=True, verbose_name='Water scarcity impacts')
    impact_types_other = models.TextField(null=True, blank=True, verbose_name='Other (agriculture, infrastructure, adaptation)')
    # Output
    output_energy_demand = models.TextField(null=True, blank=True, verbose_name='Energy demand (heating & cooling)')
    output_energy_supply = models.TextField(null=True, blank=True, verbose_name='Energy supply')
    output_water_scarcity = models.TextField(null=True, blank=True, verbose_name='Water scarcity')
    output_economics = models.TextField(null=True, blank=True, verbose_name='Economics')
    output_other = models.TextField(null=True, blank=True, verbose_name='Other (agriculture, infrastructure, adaptation)')
    # Further Information
    variables_not_directly_from_GCMs = models.TextField(null=True, blank=True, verbose_name='Variables not directly from GCMs')
    response_function_of_energy_demand_to_HDD_CDD = models.TextField(null=True, blank=True, verbose_name='Response function of energy demand to HDD/CDD')
    factor_definition_and_calculation = models.TextField(null=True, blank=True, verbose_name='Definition and calculation of variable potential and load factor')
    biomass_types = models.TextField(null=True, blank=True, verbose_name='Biomass types')
    maximum_potential_assumption = models.TextField(null=True, blank=True, verbose_name='Maximum potential assumption')
    bioenergy_supply_costs = models.TextField(null=True, blank=True, verbose_name='Bioenergy supply costs')
    socioeconomic_input = models.TextField(null=True, blank=True, verbose_name='Socio-economic input')

    def values_to_tuples(self) -> list:
        vname = self._get_verbose_field_name
        return [
            ('Model & method characteristics', [
                (vname('model_type'), self.model_type),
                (vname('temporal_extent'), self.temporal_extent),
                (vname('temporal_resolution'), self.temporal_resolution),
                (vname('data_format_for_input'), self.data_format_for_input),
            ]),
            ('Impact Types', [

                (vname('impact_types_energy_demand'), self.impact_types_energy_demand),
                (vname('impact_types_temperature_effects_on_thermal_power'), self.impact_types_temperature_effects_on_thermal_power),
                (vname('impact_types_weather_effects_on_renewables'), self.impact_types_weather_effects_on_renewables),
                (vname('impact_types_water_scarcity_impacts'), self.impact_types_water_scarcity_impacts),
                (vname('impact_types_other'), self.impact_types_other),
            ]),
            ('Output', [
                (vname('output_energy_demand'), self.output_energy_demand),
                (vname('output_energy_supply'), self.output_energy_supply),
                (vname('output_water_scarcity'), self.output_water_scarcity),
                (vname('output_economics'), self.output_economics),
                (vname('output_other'), self.output_other),
            ]),
            ('Further Information', [
                (vname('variables_not_directly_from_GCMs'), self.variables_not_directly_from_GCMs),
                (vname('response_function_of_energy_demand_to_HDD_CDD'), self.response_function_of_energy_demand_to_HDD_CDD),
                (vname('factor_definition_and_calculation'), self.factor_definition_and_calculation),
                (vname('biomass_types'), self.biomass_types),
                (vname('maximum_potential_assumption'), self.maximum_potential_assumption),
                (vname('bioenergy_supply_costs'), self.bioenergy_supply_costs),
                (vname('socioeconomic_input'), self.socioeconomic_input),
            ])
        ]


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

    def values_to_tuples(self) -> list:
        vname = self._get_verbose_field_name
        return [
            (self._meta.verbose_name, [
                (vname('defining_features'), self.defining_features),
                (vname('spatial_scale'), self.spatial_scale),
                (vname('spatial_resolution'), self.spatial_resolution),
                (vname('temporal_scale'), self.temporal_scale),
                (vname('temporal_resolution'), self.temporal_resolution),
                (vname('taxonomic_scope'), self.taxonomic_scope),
                (vname('vertical_resolution'), self.vertical_resolution),
                (vname('spatial_dispersal_included'), self.spatial_dispersal_included),
                (vname('fishbase_used_for_mass_length_conversion'), self.fishbase_used_for_mass_length_conversion),
            ])
        ]

    class Meta:
        abstract = True
class MarineEcosystemsGlobal(MarineEcosystems):
    class Meta:
        verbose_name = 'Marine Ecosystems and Fisheries (global)'
        verbose_name_plural = 'Marine Ecosystems and Fisheries (global)'
class MarineEcosystemsRegional(MarineEcosystems):
    class Meta:
        verbose_name = 'Marine Ecosystems and Fisheries (regional)'
        verbose_name_plural = 'Marine Ecosystems and Fisheries (regional)'


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

    def values_to_tuples(self) -> list:
        vname = self._get_verbose_field_name
        return [
            (self._meta.verbose_name, [
                (vname('technological_progress'), self.technological_progress),
                (vname('soil_layers'), self.soil_layers),
                (vname('water_use'), self.water_use),
                (vname('water_sectors'), self.water_sectors),
                (vname('routing'), self.routing),
                (vname('routing_data'), self.routing_data),
                (vname('land_use'), self.land_use),
                (vname('dams_reservoirs'), self.dams_reservoirs),
                (vname('calibration'), self.calibration),
                (vname('calibration_years'), self.calibration_years),
                (vname('calibration_dataset'), self.calibration_dataset),
                (vname('calibration_catchments'), self.calibration_catchments),
                (vname('vegetation'), self.vegetation),
                (vname('vegetation_representation'), self.vegetation_representation),
                (vname('methods_evapotraspiration'), self.methods_evapotraspiration),
                (vname('methods_snowmelt'), self.methods_snowmelt),
            ])
        ]

    class Meta:
        abstract = True
class WaterGlobal(Water):
    class Meta:
        verbose_name='Water (global)'
        verbose_name_plural = 'Water (global)'
class WaterRegional(Water):
    class Meta:
        verbose_name = 'Water (regional)'
        verbose_name_plural = 'Water (regional)'


class Biodiversity(Sector): pass
class Health(Sector): pass
class CoastalInfrastructure(Sector):
    class Meta:
        verbose_name = 'Coastal Infrastructure'
        verbose_name_plural = 'Coastal Infrastructure'
class Permafrost(Sector): pass
class ComputableGeneralEquilibriumModelling(Sector):
    class Meta:
        verbose_name = verbose_name_plural = 'Computable General Equilibrium Modelling'
class AgroEconomicModelling(Sector):
    class Meta:
        verbose_name = verbose_name_plural = 'Agro-Economic Modelling'


class OutputData(models.Model):
    sector = models.CharField(max_length=500, choices=ImpactModel.SECTOR_CHOICES)
    model = models.ForeignKey(ImpactModel)
    scenarios = models.ManyToManyField(Scenario)
    drivers = models.ManyToManyField(InputData)
    date = models.DateField()

    def __str__(self):
        return "%s : %s" % (self.sector, self.model.name)

    class Meta:
        verbose_name = verbose_name_plural = 'Output data'
        ordering = ('name', )


SECTOR_MAPPING = {
    'Agriculture': Agriculture,
    'Energy': Energy,
    'Water (global)': WaterGlobal,
    'Water (regional)': WaterRegional,
    'Biomes': Biomes,
    'Forests': Forests,
    'Marine Ecosystems and Fisheries (global)': MarineEcosystemsGlobal,
    'Marine Ecosystems and Fisheries (regional)': MarineEcosystemsRegional,
    'Biodiversity': Biodiversity,
    'Health': Health,
    'Coastal Infrastructure': CoastalInfrastructure,
    'Permafrost': Permafrost,
    'Computable General Equilibrium Modelling': ComputableGeneralEquilibriumModelling,
    'Agro-Economic Modelling': AgroEconomicModelling,
}
