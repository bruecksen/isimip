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


class SimulationRound(models.Model):
    name = models.CharField(max_length=500, unique=True)
    order = models.SmallIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-order',)


class ReferencePaper(Paper):
    def __str__(self):
        # if self.doi:
        #     return "%s (<a target='_blank' href='http://dx.doi.org/%s'>%s</a>)" % (self.title, self.doi, self.doi)
        return self.title

    def title_with_link(self):
        if self.doi:
            return "<a target='_blank' href='http://dx.doi.org/{0.doi}'>{0.title}</a>".format(self)
        return self.title

    def entry_with_link(self):
        author = "{} et al. ".format(self.lead_author) if self.lead_author else ''
        title = "<a target='_blank' href='http://dx.doi.org/{0.doi}'>{0.title}</a>. ".format(self) if self.doi else self.title
        journal = "{0.journal_name},{0.journal_volume},{0.journal_pages},".format(self) if self.journal_name else ''
        year = self.first_published.year if self.first_published else ''
        return "{}{}{}{}".format(author, title, journal, year)


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

    def pretty(self):
        return "{0.name} (<a href='mailto:{0.email}'>{0.email}</a>) {0.institute}".format(self)

    class Meta:
        ordering = ('name',)


class InputData(models.Model):
    name = models.CharField(max_length=500, unique=True)
    data_type = models.ForeignKey(ClimateDataType, null=True, blank=True, on_delete=models.SET_NULL)
    scenario = models.ForeignKey(Scenario, null=True, blank=True, on_delete=models.SET_NULL)
    variables = models.ManyToManyField(ClimateVariable, blank=True)
    simulation_round = models.ForeignKey(SimulationRound, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(null=True, blank=True)
    caveats = models.TextField(null=True, blank=True)
    download_instructions = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Input data'
        ordering = ('name',)


class BaseImpactModel(models.Model):
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
    sector = models.CharField(max_length=500, choices=SECTOR_CHOICES, help_text='The sector to which this information pertains. Some models may have further entries for other sectors.')
    region = models.ManyToManyField(Region, help_text="Region for which model produces results")
    short_description = models.TextField(
        null=True, blank=True, verbose_name="Short model description",
        help_text="This short description should assist other researchers in briefly describing the model in a paper.")
    owners = models.ManyToManyField(User)

    def __str__(self):
        return "%s (%s)" % (self.name, self.sector)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SECTOR_MAPPING[self.sector].objects.get_or_create(impact_model=self)

    @property
    def fk_sector_name(self):
        sector = SECTOR_MAPPING[self.sector]
        sectorname = sector._meta.label_lower.rsplit('.')[-1]
        return sectorname

    @property
    def fk_sector(self):
        return getattr(self, self.fk_sector_name)


class ImpactModel(models.Model):
    base_model = models.ForeignKey(BaseImpactModel, null=True, blank=True, related_name='base_model', on_delete=models.SET_NULL)
    simulation_round = models.ForeignKey(
        SimulationRound, blank=True, null=True, on_delete=models.SET_NULL,
        help_text="The ISIMIP simulation round for which these model details are relevant"
    )
    version = models.CharField(max_length=500, null=True, blank=True, verbose_name='Model version',
                               help_text='The model version with which the simulations were run')
    main_reference_paper = models.ForeignKey(
        ReferencePaper, null=True, blank=True, related_name='main_ref', verbose_name='Reference paper: main reference',
        help_text="The single paper that should be cited when referring to simulation output from this model",
        on_delete=models.SET_NULL)
    other_references = models.ManyToManyField(ReferencePaper, blank=True, verbose_name='Reference paper: other references',
                                              help_text='Other papers describing aspects of this model')
    public = models.BooleanField(default=True)

    class Meta:
        unique_together = ('base_model', 'simulation_round')
        ordering = ('base_model', 'simulation_round')

    def __str__(self):
        return "%s #%s (%s)" % (self.base_model.name, self.simulation_round, self.base_model.sector)

    def _get_verbose_field_name(self, field: str) -> str:
        fieldmeta = self._meta.get_field(field)
        ret = fieldmeta.verbose_name.title()
        if fieldmeta.help_text:
            ret = "<abbr title='{}'>{}</abbr>".format(fieldmeta.help_text, ret)
        return ret

    def values_to_tuples(self) -> list:
        vname = self._get_verbose_field_name
        cpers = "<ul>%s</ul>" % "".join(["<li>%s</li>" % x.pretty() for x in self.contactperson_set.all()])
        other_references = "<ul>%s</ul>" % "".join(["<li>%s</li>" % x.entry_with_link() for x in self.other_references.all()])
        return [
            ('Basic information', [
                (vname('sector'), self.sector),
                (vname('region'), ', '.join([x.name for x in self.region.all()])),
                ('Contact Person', cpers),
                (vname('simulation_round'), ', '.join([x.name for x in self.simulation_round.all()])),
                (vname('version'), self.version),
                (vname('main_reference_paper'),
                 self.main_reference_paper.entry_with_link() if self.main_reference_paper else None),
                (vname('other_references'), other_references),
                # (vname('short_description'), self.short_description),
            ]),
            ('Resolution', [
                (vname('spatial_aggregation'), self.spatial_aggregation),
                (vname('spatial_resolution'), self.spatial_resolution),
                (vname('spatial_resolution_info'), self.spatial_resolution_info),
                (vname('temporal_resolution_climate'), self.temporal_resolution_climate),
                (vname('temporal_resolution_co2'), self.temporal_resolution_co2),
                (vname('temporal_resolution_land'), self.temporal_resolution_land),
                (vname('temporal_resolution_soil'), self.temporal_resolution_soil),
                (vname('temporal_resolution_info'), self.temporal_resolution_info),
            ]),
            ('Input Data', [
                (vname('climate_data_sets'), ', '.join([x.name for x in self.climate_data_sets.all()])),
                (vname('climate_variables'), ', '.join([x.as_span() for x in self.climate_variables.all()])),
                (vname('climate_variables_info'), self.climate_variables_info),
                (vname('socioeconomic_input_variables'),
                 ', '.join([x.name for x in self.socioeconomic_input_variables.all()])),
                (vname('soil_dataset'), self.soil_dataset),
                (vname('additional_input_data_sets'), self.additional_input_data_sets),
            ]),
            ('Exceptions to Protocol', [
                (vname('exceptions_to_protocol'), self.exceptions_to_protocol),
            ]),
            ('Spin-up', [
                (vname('spin_up'), 'Yes' if self.spin_up is True else 'No' if self.spin_up is False else ''),
                (vname('spin_up_design'), self.spin_up_design if self.spin_up else ''),
            ]),
            ('Natural Vegetation', [
                (vname('natural_vegetation_partition'), self.natural_vegetation_partition),
                (vname('natural_vegetation_dynamics'), self.natural_vegetation_dynamics),
                (vname('natural_vegetation_cover_dataset'), self.natural_vegetation_cover_dataset),
            ]),
            ('Management & Adaptation Measures', [
                (vname('management'), self.management),
            ]),
            ('Extreme Events', [
                (vname('extreme_events'), self.extreme_events),
                (vname('anything_else'), self.anything_else),
            ])
        ]


class TechnicalInformation(models.Model):
    impact_model = models.OneToOneField(
        ImpactModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    spatial_aggregation = models.ForeignKey(SpatialAggregation, null=True, blank=True, on_delete=models.SET_NULL)
    spatial_resolution = ChoiceOrOtherField(
        max_length=500, choices=(('0.5°x0.5°', '0.5°x0.5°'),), blank=True, null=True, verbose_name='Spatial Resolution',
        help_text="The spatial resolution at which the ISIMIP simulations were run, if on a regular grid. Data was provided on a 0.5°x0.5° grid")
    spatial_resolution_info = models.TextField(blank=True, verbose_name='Additional spatial aggregation & resolution information',
                                               help_text='Anything else necessary to understand the spatial aggregation and resolution at which the model operates')
    TEMPORAL_RESOLUTION_CLIMATE_CHOICES = (('daily', 'daily'), ('monthly', 'monthly'), ('annual', 'annual'),)
    temporal_resolution_climate = ChoiceOrOtherField(
        max_length=500, choices=TEMPORAL_RESOLUTION_CLIMATE_CHOICES, blank=True, null=True, verbose_name='Temporal resolution of input data: climate variables',
        help_text="ISIMIP data was provided in daily time steps")
    temporal_resolution_co2 = ChoiceOrOtherField(
        max_length=500, choices=(('annual', 'annual'),), blank=True, null=True, verbose_name='Temporal resolution of input data: CO2',
        help_text="ISIMIP data was provided in annual time steps")
    temporal_resolution_land = ChoiceOrOtherField(
        max_length=500, choices=(('annual', 'annual'),), blank=True, null=True, verbose_name='Temporal resolution of input data: land use/land cover',
        help_text="ISIMIP data was provided in annual time steps")
    temporal_resolution_soil = ChoiceOrOtherField(
        max_length=500, choices=(('constant', 'constant'),), blank=True, null=True, verbose_name='Temporal resolution of input data: soil', help_text="ISIMIP data was fixed over time")
    temporal_resolution_info = models.TextField(
        verbose_name='Additional temporal resolution information', blank=True,
        help_text='Anything else necessary to understand the temporal resolution at which the model operates')


class InputDataInformation(models.Model):
    impact_model = models.OneToOneField(
        ImpactModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    climate_data_sets = models.ManyToManyField(InputData, blank=True, verbose_name="Climate data sets used",
                                               help_text="The climate-input data sets used in this simulation round")
    climate_variables = models.ManyToManyField(
        ClimateVariable, blank=True, verbose_name='Climate variables',
        help_text="Including variables that were derived from those provided in the ISIMIP input data set")
    climate_variables_info = models.TextField(blank=True, verbose_name='Additional climate variables information',
                                              help_text='Including how variables were derived that were not included in the ISIMIP input data')
    socioeconomic_input_variables = models.ManyToManyField(
        SocioEconomicInputVariables, blank=True, verbose_name="Socio-economic input variables",
        help_text="Including resolution where relevant")
    soil_dataset = models.TextField(null=True, blank=True, verbose_name='Soil dataset',
                                    help_text="HWSD or GSWP3 were provided")
    additional_input_data_sets = models.TextField(
        null=True, blank=True, verbose_name='Additional input data sets',
        help_text='Data sets used to drive the model that were not provided by ISIMIP'
    )


class OtherInformation(models.Model):
    impact_model = models.OneToOneField(
        ImpactModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    exceptions_to_protocol = models.TextField(
        null=True, blank=True, verbose_name='Exceptions',
        help_text='Any settings prescribed by the ISIMIP protocol that were overruled when runing the model'
    )
    NA_YES_NO = ((None, '---------'), (True, 'Yes'), (False, 'No'))
    spin_up = models.NullBooleanField(
        verbose_name='Was a spin-up performed?',
        help_text="'No' indicates the simulations were run starting in the first reporting year 1971",
        choices=NA_YES_NO
    )
    spin_up_design = models.TextField(
        null=True, blank=True, verbose_name='Spin-up design',
        help_text="Including the length of the spin up, the CO2 concentration used, and any deviations from the spin-up procedure defined in the protocol"
    )
    natural_vegetation_partition = models.TextField(
        null=True, blank=True, help_text='How areas covered by different types of natural vegetation are partitioned'
    )
    natural_vegetation_dynamics = models.TextField(
        null=True, blank=True,
        help_text='Description of how natural vegetation is simulated dynamically where relevant'
    )
    natural_vegetation_cover_dataset = models.TextField(
        null=True, blank=True, help_text='Dataset used if natural vegetation cover is prescribed'
    )
    management = models.TextField(
        null=True, blank=True,
        help_text='Specific management and autonomous adaptation measures applied. E.g. varying sowing dates in crop models, dbh-related harvesting in forest models.'
    )
    extreme_events = models.TextField(
        null=True, blank=True, verbose_name='Key challenges',
        help_text='Key challenges for this model in reproducing impacts of extreme events'
    )
    anything_else = models.TextField(verbose_name='Additional comments',
        null=True, blank=True, help_text='Anything else necessary to reproduce and/or understand the simulation output'
    )



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
        return self._meta.get_field(field).verbose_name.title()

    def values_to_tuples(self) -> list:
        return []


class Agriculture(Sector):
    # Key input and Management, help_text="Provide a yes/no answer and a short description of how the process is included"
    crops = models.TextField(null=True, blank=True, verbose_name='Crops')
    land_coverage = models.TextField(null=True, blank=True, verbose_name='Land cover')
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
    lead_area_development = models.TextField(null=True, blank=True, verbose_name='Lead area development', help_text='Methods for model calibration and validation')
    light_interception = models.TextField(null=True, blank=True, verbose_name='Light interception', help_text='Methods for model calibration and validation')
    light_utilization = models.TextField(null=True, blank=True, verbose_name='Light utilization', help_text='Methods for model calibration and validation')
    yield_formation = models.TextField(null=True, blank=True, verbose_name='Yield formation', help_text='Methods for model calibration and validation')
    crop_phenology = models.TextField(null=True, blank=True, verbose_name='Crop phenology', help_text='Methods for model calibration and validation')
    root_distribution_over_depth = models.TextField(null=True, blank=True, verbose_name='Root distribution over depth', help_text='Methods for model calibration and validation')
    stresses_involved = models.TextField(null=True, blank=True, verbose_name='Stresses involved', help_text='Methods for model calibration and validation')
    type_of_water_stress = models.TextField(null=True, blank=True, verbose_name='Type of water stress', help_text='Methods for model calibration and validation')
    type_of_heat_stress = models.TextField(null=True, blank=True, verbose_name='Type of heat stress', help_text='Methods for model calibration and validation')
    water_dynamics = models.TextField(null=True, blank=True, verbose_name='Water dynamics', help_text='Methods for model calibration and validation')
    evapo_transpiration = models.TextField(null=True, blank=True, verbose_name='Evapo-transpiration', help_text='Methods for model calibration and validation')
    soil_CN_modeling = models.TextField(null=True, blank=True, verbose_name='Soil CN modeling', help_text='Methods for model calibration and validation')
    co2_effects = models.TextField(null=True, blank=True, verbose_name='CO2 Effects', help_text='Methods for model calibration and validation')
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
        null=True, blank=True, verbose_name='Output per PFT?',
        help_text='Is output per PFT per unit area of that PFT, i.e. requiring weighting by the fractional coverage of each PFT to get the gridbox average?'
    )
    considerations = models.TextField(
        null=True, blank=True,
        help_text='Things to consider, when calculating basic variables such as GPP, NPP, RA, RH from the model.'
    )
    # key model processes , help_text="Please provide yes/no and a short description how the process is included"
    dynamic_vegetation = models.TextField(null=True, blank=True)
    nitrogen_limitation = models.TextField(null=True, blank=True)
    co2_effects = models.TextField(null=True, blank=True, verbose_name='CO2 effects')
    light_interception = models.TextField(null=True, blank=True)
    light_utilization = models.TextField(null=True, blank=True, help_text="photosynthesis, RUE-approach?")
    phenology = models.TextField(null=True, blank=True)
    water_stress = models.TextField(null=True, blank=True)
    heat_stress = models.TextField(null=True, blank=True)
    evapotranspiration_approach = models.TextField(verbose_name='Evapo-transpiration approach', null=True, blank=True)
    rooting_depth_differences = models.TextField(verbose_name='Differences in rooting depth', null=True, blank=True,
                                                 help_text="Including how it changes")
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
    nbp_fire = models.TextField(null=True, blank=True, verbose_name='Fire', help_text='Indicate whether the model includes fire, and how the model accounts for the fluxes, i.e. what is the fate of the biomass? E.g. directly to atmsphere or let it go to other pool')
    nbp_landuse_change = models.TextField(null=True, blank=True, verbose_name='Land-use change',
                                          help_text="Indicate whether the model includes land-use change (e.g. deforestation harvest and otherland-use changes), and how the model accounts for the fluxes, i.e. what is the fate of the biomass? e.g. directly to atmsphere or let it go to other pool")
    nbp_harvest = models.TextField(
        null=True, blank=True, verbose_name='Harvest',
        help_text="Indicate whether the model includes harvest, and how the model accounts for the fluxes, i.e. what is the fate of the biomass? E.g. directly to atmsphere or let it go to other pool. 1: crops, 2: harvest from forest management, 3: harvest from grassland management."
    )
    nbp_other = models.TextField(null=True, blank=True, verbose_name='Other processes')
    nbp_comments = models.TextField(null=True, blank=True, verbose_name='Comments')
    # Plant Functional Types (PFTs)
    list_of_pfts = models.TextField(
        null=True, blank=True, verbose_name='List of PFTs',
        help_text="Provide a list of PFTs using the folllowing format: [pft1_long_name] ([pft1_short_name]); [pft2_long_name] ([pft2_short_name]). Include long name in brackets if no short name is available."
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
    variables_not_directly_from_GCMs = models.TextField(null=True, blank=True, verbose_name='Variables not directly from GCMs', help_text='How are these calculated (including equations)?')
    response_function_of_energy_demand_to_HDD_CDD = models.TextField(null=True, blank=True, verbose_name='Response function of energy demand to HDD/CDD', help_text='Including equations where appropriate')
    factor_definition_and_calculation = models.TextField(null=True, blank=True, verbose_name='Definition and calculation of variable potential and load factor', help_text='Are these endogenous or exogenous to the model?')
    biomass_types = models.TextField(null=True, blank=True, verbose_name='Biomass types', help_text='1st generation, 2nd generation, residues...')
    maximum_potential_assumption = models.TextField(null=True, blank=True, verbose_name='Maximum potential assumption', help_text='Which information source is used?')
    bioenergy_supply_costs = models.TextField(null=True, blank=True, verbose_name='Bioenergy supply costs', help_text='Include information on the functional forms and the data sources for deriving the supply curves')
    socioeconomic_input = models.TextField(null=True, blank=True, verbose_name='Socio-economic input', help_text='Are SSP storylines implemented, or just GDP and population scenarios?')

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
            ('Information specific to marine ecosystems & fisheries', [
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
                                 help_text='Which types of water use are included in the model?')
    water_sectors = models.TextField(
        null=True, blank=True, verbose_name='Water-use sectors',
        help_text='For the global-water-model varsoc and pressoc runs, which water sectors were included? E.g. irrigation, domestic, manufacturing, electricity, livestock.')
    routing = models.TextField(null=True, blank=True, verbose_name='Runoff routing', help_text='How is runoff routed?')
    routing_data = models.TextField(null=True, blank=True, help_text='Which routing data are used?')
    land_use = models.TextField(null=True, blank=True, verbose_name='Land-use change effects',
                                help_text='Which land-use change effects are included?')
    dams_reservoirs = models.TextField(null=True, blank=True, verbose_name='Dam and reservoir implementation',
                                       help_text='Describe how are dams and reservoirs are implemented')

    calibration = models.NullBooleanField(verbose_name='Was the model calibrated?', default=None)
    calibration_years = models.TextField(null=True, blank=True, verbose_name='Which years were used for calibration?')
    calibration_dataset = models.TextField(null=True, blank=True, verbose_name='Which dataset was used for calibration?',
                                           help_text='E.g. WFD, GSWP3')
    calibration_catchments = models.TextField(null=True, blank=True,
                                              verbose_name='How many catchments were callibrated?')
    vegetation = models.NullBooleanField(verbose_name='Is CO2 fertilisation accounted for?', default=None)
    vegetation_representation = models.TextField(null=True, blank=True, verbose_name='How is vegetation represented?')
    methods_evapotranspiration = models.TextField(null=True, blank=True, verbose_name='Potential evapotranspiration')
    methods_snowmelt = models.TextField(null=True, blank=True, verbose_name='Snow melt')

    def values_to_tuples(self) -> list:
        vname = self._get_verbose_field_name
        return [
            ('Technological Progress', [
                (vname('technological_progress'), self.technological_progress),
                ]),
            ('Soil', [
                (vname('soil_layers'), self.soil_layers),
            ]),
            ('Water Use', [
                (vname('water_use'), self.water_use),
                (vname('water_sectors'), self.water_sectors),
            ]),
            ('Routing', [
                (vname('routing'), self.routing),
                (vname('routing_data'), self.routing_data),
            ]),
            ('Land Use', [
                (vname('land_use'), self.land_use),
            ]),
            ('Dams & Reservoirs', [
                (vname('dams_reservoirs'), self.dams_reservoirs),
            ]),
            ('Calibration', [
                (vname('calibration'), self.calibration),
                (vname('calibration_years'), self.calibration_years),
                (vname('calibration_dataset'), self.calibration_dataset),
                (vname('calibration_catchments'), self.calibration_catchments),
            ]),
            ('Vegetation', [
                (vname('vegetation'), self.vegetation),
                (vname('vegetation_representation'), self.vegetation_representation),
            ]),
            ('Methods', [
                (vname('methods_evapotranspiration'), self.methods_evapotranspiration),
                (vname('methods_snowmelt'), self.methods_snowmelt),
            ])
        ]

    class Meta:
        abstract = True


class WaterGlobal(Water):
    class Meta:
        verbose_name = 'Water (global)'
        verbose_name_plural = 'Water (global)'


class WaterRegional(Water):
    class Meta:
        verbose_name = 'Water (regional)'
        verbose_name_plural = 'Water (regional)'


class Biodiversity(Sector):
    pass


class Health(Sector):
    pass


class CoastalInfrastructure(Sector):
    class Meta:
        verbose_name = 'Coastal Infrastructure'
        verbose_name_plural = 'Coastal Infrastructure'


class Permafrost(Sector):
    pass


class ComputableGeneralEquilibriumModelling(Sector):
    class Meta:
        verbose_name = verbose_name_plural = 'Computable General Equilibrium Modelling'


class AgroEconomicModelling(Sector):
    class Meta:
        verbose_name = verbose_name_plural = 'Agro-Economic Modelling'


class OutputData(models.Model):
    sector = models.CharField(max_length=500, choices=BaseImpactModel.SECTOR_CHOICES)
    model = models.ForeignKey(ImpactModel, null=True, blank=True, on_delete=models.SET_NULL)
    scenarios = models.ManyToManyField(Scenario)
    drivers = models.ManyToManyField(InputData)
    date = models.DateField()

    def __str__(self):
        if self.model:
            return "%s : %s" % (self.sector, self.model.name)
        return self.sector

    class Meta:
        verbose_name = verbose_name_plural = 'Output data'


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
