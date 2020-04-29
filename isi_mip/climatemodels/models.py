import os

from django.core.validators import FileExtensionValidator
from django.apps import apps
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.text import slugify
from django.template.defaultfilters import filesizeformat

from wagtail.search import index

from isi_mip.choiceorotherfield.models import ChoiceOrOtherField
from isi_mip.sciencepaper.models import Paper


def generate_helptext(help_text, value):
    return "<abbr title='{}'>{}</abbr>".format(help_text, value)


class Region(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )


class SimulationRound(models.Model):
    name = models.CharField(max_length=500, unique=True)
    slug = models.SlugField()
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


class DataType(models.Model):
    name = models.CharField(max_length=500, unique=True)
    is_climate_data_type = models.BooleanField(default=False)

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
    base_impact_model = models.ForeignKey('BaseImpactModel', null=True, blank=True)

    def __str__(self):
        return "%s%s %s" % (self.name, self.institute and " (%s)" % self.institute or "", self.email)

    def pretty(self):
        return "{0.name} (<a href='mailto:{0.email}'>{0.email}</a>), {0.institute}".format(self)

    class Meta:
        ordering = ('name',)


class InputData(models.Model):
    PROTOCOL_DATA = 'P'
    SECONDARY_DATA = 'S'
    PROTOCOL_RELATION_CHOICES = (
        (PROTOCOL_DATA, 'Protocol'),
        (SECONDARY_DATA, 'Secondary'),
    )
    name = models.CharField(max_length=500, unique=True)
    data_type = models.ForeignKey(DataType, null=True, blank=True, on_delete=models.SET_NULL)
    protocol_relation = models.CharField(max_length=1, choices=PROTOCOL_RELATION_CHOICES, default=PROTOCOL_DATA)
    scenario = models.ManyToManyField(Scenario, blank=True, related_name='scenarios')
    variables = models.ManyToManyField(ClimateVariable, blank=True, help_text="The variables are filtered based on the data type. To see variables of a different data type, please change and save data type first.")
    simulation_round = models.ManyToManyField(SimulationRound, blank=True, related_name='simulationrounds')
    description = models.TextField(null=True, blank=True, default='')
    specification = models.TextField(null=True, blank=True, default='')
    data_source = models.TextField(null=True, blank=True, default='')
    caveats = models.TextField(null=True, blank=True)
    download_instructions = models.TextField(null=True, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s (%s)' % (self.name, ", ".join(self.simulation_round.values_list('name', flat=True)))

    class Meta:
        verbose_name_plural = 'Input data'
        ordering = ('-created', 'name',)


class Sector(models.Model):
    name = models.CharField(max_length=500, unique=True)
    slug = models.SlugField()
    drkz_folder_name = models.CharField(max_length=500, verbose_name="DKRZ folder name")
    SECTOR_MAPPING = (
        ('GenericSector', 'Generic Sector'),
        ('Agriculture', 'Agriculture'),
        ('Energy', 'Energy'),
        ('WaterGlobal', 'Water (global)'),
        ('WaterRegional', 'Water (regional)'),
        ('Biomes', 'Biomes'),
        ('Forests', 'Forests'),
        ('MarineEcosystemsGlobal', 'Marine Ecosystems and Fisheries (global)'),
        ('MarineEcosystemsRegional', 'Marine Ecosystems and Fisheries (regional)'),
        ('Biodiversity', 'Biodiversity'),
        ('Health', 'Health'),
        ('CoastalInfrastructure', 'Coastal Infrastructure',),
        ('Permafrost', 'Permafrost'),
        ('ComputableGeneralEquilibriumModelling', 'Computable General Equilibrium Modelling'),
        ('AgroEconomicModelling', 'Agro-Economic Modelling'),
    )
    class_name = models.CharField(max_length=500, choices=SECTOR_MAPPING, default='GenericSector')
    has_sector_specific_values = models.BooleanField(default=True)

    @property
    def model(self):
        return apps.get_model(app_label='climatemodels', model_name=self.class_name)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Sectors'
        ordering = ('name',)


class SectorInformationGroup(models.Model):
    sector = models.ForeignKey(Sector)
    name = models.CharField(max_length=500)
    identifier = models.SlugField()
    description = models.TextField(blank=True)
    order = models.SmallIntegerField(default=0)

    def __str__(self):
        return '%s (%s)' % (self.name, self.sector.name)

    class Meta:
        verbose_name_plural = 'Sector information groups'
        ordering = ('order', 'name')
        unique_together = ('sector', 'name')


class SectorInformationField(models.Model):
    information_group = models.ForeignKey(SectorInformationGroup, related_name='fields')
    name = models.CharField(max_length=500)
    identifier = models.SlugField()
    help_text = models.CharField(max_length=500, blank=True)
    order = models.SmallIntegerField(default=0)

    def __str__(self):
        return '%s' % (self.name, )

    class Meta:
        verbose_name_plural = 'Sector information fields'
        ordering = ('order', 'name')
        unique_together = ('name', 'information_group')

    @property
    def unique_identifier(self):
        return '%s-%s' % (self.information_group.identifier, self.identifier)


class BaseImpactModel(index.Indexed, models.Model):
    name = models.CharField(max_length=500)
    drkz_folder_name = models.CharField(max_length=500, verbose_name="DKRZ folder name")
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
    sector = models.ForeignKey(Sector, help_text='The sector to which this information pertains. Some models may have further entries for other sectors.')
    region = models.ManyToManyField(Region, help_text="Region for which model produces results")
    short_description = models.TextField(
        null=True, blank=True, default='', verbose_name="Short model description (all rounds)",
        help_text="This short description should assist other researchers in getting an understanding of your model, including the main differences between model versions used for different ISIMIP simulation rounds.")

    search_fields = [
        index.SearchField('name', partial_match=True, boost=10),
        index.RelatedFields('sector', [
            index.SearchField('name'),
        ]),
        index.FilterField('public'),
        index.SearchField('get_related_contact_persons'),
        index.SearchField('short_description'),
    ]

    class Meta:
        ordering = ('name', 'sector')

    def __str__(self):
        return "%s (%s)" % (self.name, self.sector)

    def relative_url(self, site, request):
        # hard coded url, since no better solution at the moment
        # https://groups.google.com/forum/#!topic/wagtail/51FD2E4Odmc
        return "/impactmodels/details/%s/" % self.pk

    def get_missing_simulation_rounds(self):
        return SimulationRound.objects.exclude(id__in=self.impact_model.all().values_list('simulation_round', flat=True))

    def public(self):
        return self.impact_model.filter(public=True).exists()

    def get_related_contact_persons(self):
        return '\n'.join(['%s %s %s' % (owner.name, owner.email, owner.institute) for owner in self.impact_model_owner.all()])

    def can_duplicate_from(self):
        return self.impact_model.order_by('simulation_round').first()

    def _get_verbose_field_name(self, field):
        fieldmeta = self._meta.get_field(field)
        ret = fieldmeta.verbose_name.title()
        if fieldmeta.help_text:
            ret = generate_helptext(fieldmeta.help_text, ret)
        return ret

    def values_to_tuples(self):
        vname = self._get_verbose_field_name
        cpers = "<ul>%s</ul>" % "".join(["<li>%s</li>" % x.pretty() for x in self.impact_model_owner.all()])
        return [
            ('Common information', [
                (vname('sector'), self.sector),
                (vname('region'), ', '.join([x.name for x in self.region.all()])),
                ('Contact Person', cpers),
            ])]

    def save(self, *args, **kwargs):
        is_creation = self.pk is None
        super().save(*args, **kwargs)
        if not is_creation:
            # make sure if sector changes that sector specific objects exists for every impact model
            for impact_model in ImpactModel.objects.filter(base_model=self):
                if not hasattr(impact_model, impact_model.fk_sector_name):
                    self.sector.model.objects.get_or_create(impact_model=impact_model)


class ImpactModel(models.Model):
    base_model = models.ForeignKey(BaseImpactModel, null=True, blank=True, related_name='impact_model', on_delete=models.CASCADE)
    simulation_round = models.ForeignKey(
        SimulationRound, blank=True, null=True, on_delete=models.SET_NULL,
        help_text="The ISIMIP simulation round for which these model details are relevant"
    )
    version = models.CharField(max_length=500, null=True, blank=True, verbose_name='Model version',
                               help_text='The model version with which these simulations were run. If possible provide the git hash for later reproducibility. Indicate if the model version used for ISIMIP2b/3b can be evaluated against the ISIMIP2a/3a runs with observed forcings.')
    main_reference_paper = models.ForeignKey(
        ReferencePaper, null=True, blank=True, related_name='main_ref', verbose_name='Reference paper: main reference',
        help_text="The single paper that should be cited when referring to simulation output from this model",
        on_delete=models.SET_NULL)
    other_references = models.ManyToManyField(ReferencePaper, blank=True, verbose_name='Reference paper: other references',
                                              help_text='Other papers describing aspects of this model')
    responsible_person = models.CharField(max_length=500, null=True, blank=True, verbose_name='Person responsible for model simulations in this simulation round',
                               help_text='Contact information for person responsible for model simulations in this simulation round, if not the model contact person')
    simulation_round_specific_description = models.TextField(
        null=True, blank=True, default='', verbose_name="Simulation round specific description",
        help_text="")

    public = models.BooleanField(default=False)

    class Meta:
        unique_together = ('base_model', 'simulation_round')
        ordering = ('base_model', 'simulation_round')

    def __str__(self):
        return "%s (%s, %s)" % (self.base_model and self.base_model.name or self.id, self.base_model and self.base_model.sector or '', self.simulation_round)

    @property
    def fk_sector_name(self):
        return self.base_model.sector.class_name.lower()

    @property
    def fk_sector(self):
        return getattr(self, self.fk_sector_name)

    def save(self, *args, **kwargs):
        is_duplication = kwargs.pop('is_duplication', False)
        is_creation = self.pk is None
        super().save(*args, **kwargs)
        if not is_duplication and is_creation:
            # if model gets duplicated we handle related instances in the duplicate method
            self.base_model.sector.model.objects.get_or_create(impact_model=self)
            TechnicalInformation.objects.get_or_create(impact_model=self)
            InputDataInformation.objects.get_or_create(impact_model=self)
            OtherInformation.objects.get_or_create(impact_model=self)

        # make all owners involved in the duplicated model
        if is_creation and self.base_model:
            for owner in self.base_model.impact_model_owner.all():
                owner.involved.add(self)
        # make sure if sector changes that sector specific objects exists for the impact model
        if not is_duplication and not hasattr(self, self.fk_sector_name):
            self.base_model.sector.model.objects.get_or_create(impact_model=self)

    def duplicate(self, simulation_round):
        # save old references
        old_technical_information = self.technicalinformation
        old_input_data = self.inputdatainformation
        old_other = self.otherinformation
        old_sector = self.fk_sector
        # Impact model
        duplicate = ImpactModel(
            base_model=self.base_model,
            simulation_round=simulation_round,
            version=self.version,
            main_reference_paper=self.main_reference_paper,
            responsible_person=self.responsible_person,
            simulation_round_specific_description=self.simulation_round_specific_description,
            public=True,

        )
        duplicate.save(is_duplication=True)
        duplicate.other_references.set(self.other_references.all())
        # Technical information
        old_technical_information.pk = None
        old_technical_information.impact_model = duplicate
        old_technical_information.save()
        # Input Data
        old_climate_variables = old_input_data.climate_variables.filter(inputdata__simulation_round=simulation_round)
        old_simulated_atmospheric_climate_data_sets = old_input_data.simulated_atmospheric_climate_data_sets.filter(simulation_round=simulation_round)
        old_observed_atmospheric_climate_data_sets = old_input_data.observed_atmospheric_climate_data_sets.filter(simulation_round=simulation_round)
        old_simulated_ocean_climate_data_sets = old_input_data.simulated_ocean_climate_data_sets.filter(simulation_round=simulation_round)
        old_observed_ocean_climate_data_sets = old_input_data.observed_ocean_climate_data_sets.filter(simulation_round=simulation_round)
        old_emissions_data_sets = old_input_data.emissions_data_sets.filter(simulation_round=simulation_round)
        old_socio_economic_data_sets = old_input_data.socio_economic_data_sets.filter(simulation_round=simulation_round)
        old_land_use_data_sets = old_input_data.land_use_data_sets.filter(simulation_round=simulation_round)
        old_other_human_influences_data_sets = old_input_data.other_human_influences_data_sets.filter(simulation_round=simulation_round)
        old_other_data_sets = old_input_data.other_data_sets.filter(simulation_round=simulation_round)
        old_input_data.pk = None
        old_input_data.impact_model = duplicate
        old_input_data.save()
        old_input_data.climate_variables.set(old_climate_variables)
        old_input_data.simulated_atmospheric_climate_data_sets.set(old_simulated_atmospheric_climate_data_sets)
        old_input_data.observed_atmospheric_climate_data_sets.set(old_observed_atmospheric_climate_data_sets)
        old_input_data.simulated_ocean_climate_data_sets.set(old_simulated_ocean_climate_data_sets)
        old_input_data.observed_ocean_climate_data_sets.set(old_observed_ocean_climate_data_sets)
        old_input_data.emissions_data_sets.set(old_emissions_data_sets)
        old_input_data.socio_economic_data_sets.set(old_socio_economic_data_sets)
        old_input_data.land_use_data_sets.set(old_land_use_data_sets)
        old_input_data.other_human_influences_data_sets.set(old_other_human_influences_data_sets)
        old_input_data.other_data_sets.set(old_other_data_sets)
        # OtherInformation
        old_other.pk = None
        old_other.impact_model = duplicate
        old_other.save()
        # Sector
        old_sector.pk = None
        old_sector.impact_model = duplicate
        old_sector.save()
        return duplicate

    def _get_verbose_field_name(self, field):
        fieldmeta = self._meta.get_field(field)
        ret = fieldmeta.verbose_name.title()
        if fieldmeta.help_text:
            ret = generate_helptext(fieldmeta.help_text, ret)
        return ret

    def values_to_tuples(self):
        vname = self._get_verbose_field_name
        bvname = self.base_model._get_verbose_field_name
        if self.other_references.exists():
            other_references = "<ul>%s</ul>" % "".join(["<li>%s</li>" % x.entry_with_link() for x in self.other_references.all()])
        else:
            other_references = None
        model_output_license = ''
        if hasattr(self, 'confirmation'):
            model_output_license = self.confirmation.confirmed_license
        return [
            ('Basic information', [
                (vname('version'), self.version),
                ('Model output license', model_output_license),
                (vname('simulation_round_specific_description'), self.simulation_round_specific_description),
                (vname('main_reference_paper'),
                 self.main_reference_paper.entry_with_link() if self.main_reference_paper else None),
                (vname('other_references'), other_references),
                (vname('responsible_person'), self.responsible_person),
            ]),
            self.technicalinformation.values_to_tuples(),
            self.inputdatainformation.values_to_tuples(),
        ] + self.otherinformation.values_to_tuples()

    def can_confirm_data(self):
        return hasattr(self, 'confirmation') and not self.confirmation.is_confirmed


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

    def _get_verbose_field_name(self, field):
        fieldmeta = self._meta.get_field(field)
        ret = fieldmeta.verbose_name.title()
        if fieldmeta.help_text:
            ret = generate_helptext(fieldmeta.help_text, ret)
        return ret

    def values_to_tuples(self):
        vname = self._get_verbose_field_name
        return ('Resolution', [
                (vname('spatial_aggregation'), self.spatial_aggregation),
                (vname('spatial_resolution'), self.spatial_resolution),
                (vname('spatial_resolution_info'), self.spatial_resolution_info),
                (vname('temporal_resolution_climate'), self.temporal_resolution_climate),
                (vname('temporal_resolution_co2'), self.temporal_resolution_co2),
                (vname('temporal_resolution_land'), self.temporal_resolution_land),
                (vname('temporal_resolution_soil'), self.temporal_resolution_soil),
                (vname('temporal_resolution_info'), self.temporal_resolution_info),
                ])


class InputDataInformation(models.Model):
    impact_model = models.OneToOneField(
        ImpactModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    simulated_atmospheric_climate_data_sets = models.ManyToManyField(InputData, blank=True, verbose_name="Simulated atmospheric climate data sets used",
                                                                     help_text="The simulated atmospheric climate data sets used in this simulation round", related_name="simulated_atmospheric_climate_data_sets")
    observed_atmospheric_climate_data_sets = models.ManyToManyField(InputData, blank=True, verbose_name="Observed atmospheric climate data sets used",
                                                                    help_text="The observed atmospheric climate data sets used in this simulation round", related_name="observed_atmospheric_climate_data_sets")
    simulated_ocean_climate_data_sets = models.ManyToManyField(InputData, blank=True, verbose_name="Simulated ocean climate data sets used",
                                                               help_text="The observed ocean climate data sets used in this simulation round", related_name="simulated_ocean_climate_data_sets")
    observed_ocean_climate_data_sets = models.ManyToManyField(InputData, blank=True, verbose_name="Observed ocean climate data sets used",
                                                              help_text="The observed ocean climate data sets used in this simulation round", related_name="observed_ocean_climate_data_sets")
    emissions_data_sets = models.ManyToManyField(InputData, blank=True, verbose_name="Emissions data sets used",
                                                 help_text="The emissions data sets used in this simulation round", related_name="emissions_data_sets")
    socio_economic_data_sets = models.ManyToManyField(InputData, blank=True, verbose_name="Socio-economic data sets used",
                                                      help_text="The socio-economic data sets used in this simulation round", related_name="socio_economic_data_sets")
    land_use_data_sets = models.ManyToManyField(InputData, blank=True, verbose_name="Land use data sets used",
                                                help_text="The Land use data sets used in this simulation round", related_name="land_use_data_sets")
    other_human_influences_data_sets = models.ManyToManyField(InputData, blank=True, verbose_name="Other human influences data sets used",
                                                              help_text="The other human influences data sets used in this simulation round", related_name="other_human_influences_data_sets")
    other_data_sets = models.ManyToManyField(InputData, blank=True, verbose_name="Other data sets used",
                                             help_text="Other data sets used in this simulation round", related_name="other_data_sets")
    additional_input_data_sets = models.TextField(
        null=True, blank=True, verbose_name='Additional input data sets',
        help_text='Data sets used to drive the model that were not provided by ISIMIP'
    )
    climate_variables = models.ManyToManyField(
        ClimateVariable, blank=True, verbose_name='Climate variables',
        help_text="Which of the climate input variables provided was used by your model?")
    climate_variables_info = models.TextField(blank=True, verbose_name='Additional information about input variables',
                                              help_text='Including how variables were derived that were not included in the ISIMIP input data')

    def _get_verbose_field_name(self, field):
        fieldmeta = self._meta.get_field(field)
        ret = fieldmeta.verbose_name.title()
        if fieldmeta.help_text:
            ret = generate_helptext(fieldmeta.help_text, ret)
        return ret

    def values_to_tuples(self):
        vname = self._get_verbose_field_name
        return ('Input data sets used', [
                (vname('simulated_atmospheric_climate_data_sets'), ', '.join([x.name for x in self.simulated_atmospheric_climate_data_sets.all()])),
                (vname('observed_atmospheric_climate_data_sets'), ', '.join([x.name for x in self.observed_atmospheric_climate_data_sets.all()])),
                (vname('simulated_ocean_climate_data_sets'), ', '.join([x.name for x in self.simulated_ocean_climate_data_sets.all()])),
                (vname('observed_ocean_climate_data_sets'), ', '.join([x.name for x in self.observed_ocean_climate_data_sets.all()])),
                (vname('emissions_data_sets'), ', '.join([x.name for x in self.emissions_data_sets.all()])),
                (vname('socio_economic_data_sets'), ', '.join([x.name for x in self.socio_economic_data_sets.all()])),
                (vname('land_use_data_sets'), ', '.join([x.name for x in self.land_use_data_sets.all()])),
                (vname('other_human_influences_data_sets'), ', '.join([x.name for x in self.other_human_influences_data_sets.all()])),
                (vname('other_data_sets'), ', '.join([x.name for x in self.other_data_sets.all()])),
                (vname('climate_variables'), ', '.join([x.as_span() for x in self.climate_variables.all()])),
                (vname('climate_variables_info'), self.climate_variables_info),
                (vname('additional_input_data_sets'), self.additional_input_data_sets),
                ])


class OtherInformation(models.Model):
    impact_model = models.OneToOneField(
        ImpactModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    exceptions_to_protocol = models.TextField(
        null=True, blank=True, default='', verbose_name='Exceptions',
        help_text='Any settings prescribed by the ISIMIP protocol that were overruled when runing the model'
    )
    YES_NO = ((True, 'Yes'), (False, 'No'))
    spin_up = models.NullBooleanField(
        verbose_name='Was a spin-up performed?',
        help_text="'No' indicates the simulations were run starting in the first reporting year 1971",
        choices=YES_NO
    )
    spin_up_design = models.TextField(
        null=True, blank=True, default='', verbose_name='Spin-up design',
        help_text="Including the length of the spin up, the CO2 concentration used, and any deviations from the spin-up procedure defined in the protocol"
    )
    natural_vegetation_partition = models.TextField(
        null=True, blank=True, default='', help_text='How areas covered by different types of natural vegetation are partitioned'
    )
    natural_vegetation_dynamics = models.TextField(
        null=True, blank=True, default='',
        help_text='Description of how natural vegetation is simulated dynamically where relevant'
    )
    natural_vegetation_cover_dataset = models.TextField(
        null=True, blank=True, default='', help_text='Dataset used if natural vegetation cover is prescribed'
    )
    management = models.TextField(
        null=True, blank=True, default='',
        help_text='Specific management and autonomous adaptation measures applied. E.g. varying sowing dates in crop models, dbh-related harvesting in forest models.'
    )
    extreme_events = models.TextField(
        null=True, blank=True, default='', verbose_name='Key challenges',
        help_text='Key challenges for this model in reproducing impacts of extreme events'
    )
    anything_else = models.TextField(
        verbose_name='Additional comments',
        null=True, blank=True, default='', help_text='Anything else necessary to reproduce and/or understand the simulation output'
    )

    def _get_verbose_field_name(self, field):
        fieldmeta = self._meta.get_field(field)
        ret = fieldmeta.verbose_name.title()
        if fieldmeta.help_text:
            ret = generate_helptext(fieldmeta.help_text, ret)
        return ret

    def values_to_tuples(self):
        vname = self._get_verbose_field_name
        return [
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
            ('Extreme Events & Disturbances', [
                (vname('extreme_events'), self.extreme_events),
                (vname('anything_else'), self.anything_else),
            ])
        ]


class BaseSector(models.Model):
    impact_model = models.OneToOneField(ImpactModel)
    data = JSONField(blank=True, null=True, default=dict)

    class Meta:
        abstract = True

    def __str__(self):
        return '%s' % (self.impact_model)

    def _get_verbose_field_name(self, field):
        fieldmeta = self._meta.get_field(field)
        ret = fieldmeta.verbose_name.title()
        if fieldmeta.help_text:
            ret = generate_helptext(fieldmeta.help_text, ret)
        return ret

    def _get_verbose_field_name_question(self, field):
        fieldmeta = self._meta.get_field(field)
        ret = fieldmeta.verbose_name
        if fieldmeta.help_text:
            ret = generate_helptext(fieldmeta.help_text, ret)
        return ret

    def _get_generic_verbose_field_name(self, field):
        ret = field.name
        if field.help_text:
            ret = generate_helptext(field.help_text, ret)
        return ret

    def values_to_tuples(self):
        if not self.data:
            return []
        groups = []
        vname = self._get_generic_verbose_field_name
        for group in SectorInformationGroup.objects.filter(sector=self.impact_model.base_model.sector):
                fields = []
                for field in group.fields.all():
                    fields.append((vname(field), self.data.get(field.unique_identifier, '')))
                groups.append((group.name, fields))
        return groups


class GenericSector(BaseSector):
    def __str__(self):
        return '%s' % self.impact_model.base_model.sector

    class Meta:
        verbose_name = 'Generic sector'


class Agriculture(BaseSector):
    # Key input and Management, help_text="Provide a yes/no answer and a short description of how the process is included"
    crops = models.TextField(null=True, blank=True, default='', verbose_name='Crops')
    land_coverage = models.TextField(null=True, blank=True, default='', verbose_name='Land cover')
    planting_date_decision = models.TextField(null=True, blank=True, default='', verbose_name='Planting date decision')
    planting_density = models.TextField(null=True, blank=True, default='', verbose_name='Planting density')
    crop_cultivars = models.TextField(null=True, blank=True, default='', verbose_name='Crop cultivars')
    fertilizer_application = models.TextField(null=True, blank=True, default='', verbose_name='Fertilizer application')
    irrigation = models.TextField(null=True, blank=True, default='', verbose_name='Irrigation')
    crop_residue = models.TextField(null=True, blank=True, default='', verbose_name='Crop residue')
    initial_soil_water = models.TextField(null=True, blank=True, default='', verbose_name='Initial soil water')
    initial_soil_nitrate_and_ammonia = models.TextField(null=True, blank=True, default='', verbose_name='Initial soil nitrate and ammonia')
    initial_soil_C_and_OM = models.TextField(null=True, blank=True, default='', verbose_name='Initial soil C and OM')
    initial_crop_residue = models.TextField(null=True, blank=True, default='', verbose_name='Initial crop residue')
    # Key model processes, help_text="Please specify methods for model calibration and validation"
    lead_area_development = models.TextField(null=True, blank=True, default='', verbose_name='Leaf area development', help_text='Methods for model calibration and validation')
    light_interception = models.TextField(null=True, blank=True, default='', verbose_name='Light interception', help_text='Methods for model calibration and validation')
    light_utilization = models.TextField(null=True, blank=True, default='', verbose_name='Light utilization', help_text='Methods for model calibration and validation')
    yield_formation = models.TextField(null=True, blank=True, default='', verbose_name='Yield formation', help_text='Methods for model calibration and validation')
    crop_phenology = models.TextField(null=True, blank=True, default='', verbose_name='Crop phenology', help_text='Methods for model calibration and validation')
    root_distribution_over_depth = models.TextField(null=True, blank=True, default='', verbose_name='Root distribution over depth', help_text='Methods for model calibration and validation')
    stresses_involved = models.TextField(null=True, blank=True, default='', verbose_name='Stresses involved', help_text='Methods for model calibration and validation')
    type_of_water_stress = models.TextField(null=True, blank=True, default='', verbose_name='Type of water stress', help_text='Methods for model calibration and validation')
    type_of_heat_stress = models.TextField(null=True, blank=True, default='', verbose_name='Type of heat stress', help_text='Methods for model calibration and validation')
    water_dynamics = models.TextField(null=True, blank=True, default='', verbose_name='Water dynamics', help_text='Methods for model calibration and validation')
    evapo_transpiration = models.TextField(null=True, blank=True, default='', verbose_name='Evapo-transpiration', help_text='Methods for model calibration and validation')
    soil_CN_modeling = models.TextField(null=True, blank=True, default='', verbose_name='Soil CN modeling', help_text='Methods for model calibration and validation')
    co2_effects = models.TextField(null=True, blank=True, default='', verbose_name='CO2 Effects', help_text='Methods for model calibration and validation')
    # Methods for model calibration and validation , help_text="Please specify methods for model calibration and validation"
    parameters_number_and_description = models.TextField(null=True, blank=True, default='', verbose_name='Parameters, number and description')
    calibrated_values = models.TextField(null=True, blank=True, default='', verbose_name='Calibrated values')
    output_variable_and_dataset = models.TextField(null=True, blank=True, default='', verbose_name='Output variable and dataset for calibration validation')
    spatial_scale_of_calibration_validation = models.TextField(null=True, blank=True, default='', verbose_name='Spatial scale of calibration/validation')
    temporal_scale_of_calibration_validation = models.TextField(null=True, blank=True, default='', verbose_name='Temporal scale of calibration/validation')
    criteria_for_evaluation = models.TextField(null=True, blank=True, default='', verbose_name='Criteria for evaluation (validation)')

    def values_to_tuples(self):
        vname = self._get_verbose_field_name
        generic = super(Agriculture, self).values_to_tuples()
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
        ] + generic


class BiomesForests(BaseSector):
    # technological_progress = models.TextField(null=True, blank=True, default='')
    output = models.TextField(
        null=True, blank=True, default='', verbose_name='Output format',
        help_text='Is output (e.g. PFT cover) written out per grid-cell area or per land and water area within a grid cell, or land only?'
    )
    output_per_pft = models.TextField(
        null=True, blank=True, default='', verbose_name='Output per PFT?',
        help_text='Is output per PFT per unit area of that PFT, i.e. requiring weighting by the fractional coverage of each PFT to get the gridbox average?'
    )
    considerations = models.TextField(
        null=True, blank=True, default='',
        help_text='Things to consider, when calculating basic variables such as GPP, NPP, RA, RH from the model.'
    )
    # key model processes , help_text="Please provide yes/no and a short description how the process is included"
    dynamic_vegetation = models.TextField(null=True, blank=True, default='')
    nitrogen_limitation = models.TextField(null=True, blank=True, default='')
    co2_effects = models.TextField(null=True, blank=True, default='', verbose_name='CO2 effects')
    light_interception = models.TextField(null=True, blank=True, default='')
    light_utilization = models.TextField(null=True, blank=True, default='', help_text="photosynthesis, RUE-approach?")
    phenology = models.TextField(null=True, blank=True, default='')
    water_stress = models.TextField(null=True, blank=True, default='')
    heat_stress = models.TextField(null=True, blank=True, default='')
    evapotranspiration_approach = models.TextField(verbose_name='Evapo-transpiration approach', null=True, blank=True, default='')
    rooting_depth_differences = models.TextField(verbose_name='Differences in rooting depth', null=True, blank=True, default='',
                                                 help_text="Including how it changes")
    root_distribution = models.TextField(verbose_name='Root distribution over depth', null=True, blank=True, default='')
    permafrost = models.TextField(null=True, blank=True, default='')
    closed_energy_balance = models.TextField(null=True, blank=True, default='')
    soil_moisture_surface_temperature_coupling = models.TextField(
        null=True, blank=True, default='', verbose_name='Coupling/feedback between soil moisture and surface temperature')
    latent_heat = models.TextField(null=True, blank=True, default='')
    sensible_heat = models.TextField(null=True, blank=True, default='')
    # causes of mortality in vegetation models , help_text="Describe briefly how the process is described in this model and in which way it is climate dependent."
    mortality_age = models.TextField(verbose_name='Age/Senescence', null=True, blank=True, default='')
    mortality_fire = models.TextField(verbose_name='Fire', null=True, blank=True, default='')
    mortality_drought = models.TextField(verbose_name='Drought', null=True, blank=True, default='')
    mortality_insects = models.TextField(verbose_name='Insects', null=True, blank=True, default='')
    mortality_storm = models.TextField(verbose_name='Storm', null=True, blank=True, default='')
    mortality_stochastic_random_disturbance = models.TextField(verbose_name='Stochastic random disturbance', null=True, blank=True, default='')
    mortality_other = models.TextField(verbose_name='Other', null=True, blank=True, default='')
    mortality_remarks = models.TextField(verbose_name='Remarks', null=True, blank=True, default='')
    # NBP components , help_text="Indicate whether the model includes the processes, and how the model accounts for the fluxes, i.e.what is the fate of the biomass? E.g.directly to atmsphere or let it go to other pool"
    nbp_fire = models.TextField(null=True, blank=True, default='', verbose_name='Fire', help_text='Indicate whether the model includes fire, and how the model accounts for the fluxes, i.e. what is the fate of the biomass? E.g. directly to atmsphere or let it go to other pool')
    nbp_landuse_change = models.TextField(null=True, blank=True, default='', verbose_name='Land-use change',
                                          help_text="Indicate whether the model includes land-use change (e.g. deforestation harvest and otherland-use changes), and how the model accounts for the fluxes, i.e. what is the fate of the biomass? e.g. directly to atmsphere or let it go to other pool")
    nbp_harvest = models.TextField(
        null=True, blank=True, default='', verbose_name='Harvest',
        help_text="Indicate whether the model includes harvest, and how the model accounts for the fluxes, i.e. what is the fate of the biomass? E.g. directly to atmsphere or let it go to other pool. 1: crops, 2: harvest from forest management, 3: harvest from grassland management."
    )
    nbp_other = models.TextField(null=True, blank=True, default='', verbose_name='Other processes')
    nbp_comments = models.TextField(null=True, blank=True, default='', verbose_name='Comments')
    # Species / Plant Functional Types (PFTs)
    list_of_pfts = models.TextField(
        null=True, blank=True, default='', verbose_name='List of species / PFTs',
        help_text="Provide a list of PFTs using the folllowing format: [pft1_long_name] ([pft1_short_name]); [pft2_long_name] ([pft2_short_name]). Include long name in brackets if no short name is available."
    )
    pfts_comments = models.TextField(null=True, blank=True, default='', verbose_name='Comments')

    def values_to_tuples(self):
        vname = self._get_verbose_field_name
        generic = super(BiomesForests, self).values_to_tuples()
        return [
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
            ('Species / Plant Functional Types (PFTs)', [
                (vname('list_of_pfts'), self.list_of_pfts),
                (vname('pfts_comments'), self.pfts_comments),
            ]),
            ('Model output specifications', [
                (vname('output'), self.output),
                (vname('output_per_pft'), self.output_per_pft),
                (vname('considerations'), self.considerations),
            ]),
        ] + generic

    class Meta:
        abstract = True


class Biomes(BiomesForests):
    # key model processes
    compute_soil_carbon = models.TextField(null=True, blank=True, default='', verbose_name='How do you compute soil organic carbon during land use (do you mix the previous PFT SOC into agricultural SOC)?')
    seperate_soil_carbon = models.TextField(null=True, blank=True, default='', verbose_name='Do you separate soil organic carbon in pasture from natural grass?')
    harvest_npp_crops = models.TextField(null=True, blank=True, default='', verbose_name='Do you harvest NPP of crops? Do you including grazing? How does harvested NPP decay?')
    treat_biofuel_npp = models.TextField(null=True, blank=True, default='', verbose_name='How do you to treat biofuel NPP and biofuel harvest?')
    npp_litter_output = models.TextField(null=True, blank=True, default='', verbose_name='Does non-harvested crop NPP go to litter in your output?')
    # model setup
    simulate_bioenergy = models.TextField(null=True, blank=True, default='', verbose_name='How do you simulate bioenergy? I.e. What PFT do you simulate on bioenergy land?')
    transition_cropland = models.TextField(null=True, blank=True, default='', verbose_name='How do you simulate the transition from cropland to bioenergy?')
    simulate_pasture = models.TextField(null=True, blank=True, default='', verbose_name='How do you simulate pasture (which PFT)?')
    
    class Meta:
        verbose_name_plural = 'Biomes'
        verbose_name = 'Biomes'

    def values_to_tuples(self):
        vname = self._get_verbose_field_name
        generic = super(BiomesForests, self).values_to_tuples()
        return [
            ('Model set-up specifications', [
                (vname('simulate_bioenergy'), self.simulate_bioenergy),
                (vname('transition_cropland'), self.transition_cropland),
                (vname('simulate_pasture'), self.simulate_pasture),
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
                (vname('compute_soil_carbon'), self.compute_soil_carbon),
                (vname('seperate_soil_carbon'), self.seperate_soil_carbon),
                (vname('harvest_npp_crops'), self.harvest_npp_crops),
                (vname('treat_biofuel_npp'), self.treat_biofuel_npp),
                (vname('npp_litter_output'), self.npp_litter_output),
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
            ('Species / Plant Functional Types (PFTs)', [
                (vname('list_of_pfts'), self.list_of_pfts),
                (vname('pfts_comments'), self.pfts_comments),
            ]),
            ('Model output specifications', [
                (vname('output'), self.output),
                (vname('output_per_pft'), self.output_per_pft),
                (vname('considerations'), self.considerations),
            ]),
        ] + generic


class Forests(BiomesForests):
    # Forest Model Set-up Specifications
    initialize_model = models.TextField(null=True, blank=True, default='', verbose_name='How did you initialize your model, e.g. using Individual tree dbh and height or stand basal area? How do you initialize soil conditions?')
    data_profound_db = models.TextField(null=True, blank=True, default='', verbose_name='Which data from PROFOUND DB did you use for initialisation (name of variable, which year)? From stand data or from individual tree data?')
    management_implementation = models.TextField(null=True, blank=True, default='', verbose_name='How is management implemented? E.g. do you harvest biomass/basal area proportions or by tree numbers or dimensions (target dbh)?')
    harvesting_simulated = models.TextField(null=True, blank=True, default='', verbose_name='When is harvesting simulated by your model (start/middle/end of the year, i.e., before or after the growing season)?')
    regenerate = models.TextField(null=True, blank=True, default='', verbose_name='How do you regenerate? Do you plant seedlings one year after harvest or several years of gap and then plant larger saplings?')
    unmanaged_simulations = models.TextField(null=True, blank=True, default='', verbose_name='How are the unmanaged simulations designed? Is there some kind of regrowth/regeneration or are the existing trees just growing older and older?')
    noco2_scenario = models.TextField(null=True, blank=True, default='', verbose_name='How are models implementing the noco2 scenario? Please confirm that co2 is follwing the historical trend (based on PROFUND DB) until 2000 (for ISIMIPFT) or 2005 (for ISIMIP2b) and then fixed at 2000 or 2005 value respectively?')
    leap_years = models.TextField(null=True, blank=True, default='', verbose_name='Does your model consider leap-years or a 365 calendar only? Or any other calendar?')
    simulate_minor_tree = models.TextField(null=True, blank=True, default='', verbose_name='In hyytiälä and kroof, how did you simulate the "minor tree species"? e.g. in hyytiälä did you simulate only pine trees and removed the spruce trees or did you interpret spruce basal area as being pine basal area?')
    nitrogen_simulation = models.TextField(null=True, blank=True, default='', verbose_name='How did you simulate nitrogen deposition from 2005 onwards in the 2b picontrol run? Please confirm you kept them constant at 2005-levels?')
    soil_depth = models.TextField(null=True, blank=True, default='', verbose_name='What is the soil depth you assumed for each site and how many soil layers (including their depths) do you assume in each site? Please upload a list of the soil depth and soil layers your model assumes for each site as an attachment (Section 7).')
    stochastic_element = models.TextField(null=True, blank=True, default='', verbose_name='Is there any stochastic element in your model (e.g. in the management or mortality submodel) that will lead to slightly different results if the model is re-run, even though all drivers etc. remain the same?')
    minimum_diameter_tree = models.TextField(null=True, blank=True, default='', verbose_name='What is the minimum diameter at which a „tree is considered a tree“? and is there a similar threshold for the minimum harvestable diameter?')
    model_historically_calibrated = models.TextField(null=True, blank=True, default='', verbose_name='Has your model been "historically calibrated" to any of the sites you simulated? e.g. has the site been used for model testing during model development?')
    upload_parameter_list = models.TextField(null=True, blank=True, default='', verbose_name='Please upload a list of your parameters as an attachment (Section 7). The list should include species-specific parameters and other parameters not depending on initialization data including the following information: short name, long name, short explanation, unit, value, see here for an example (http://www.pik-potsdam.de/4c/web_4c/theory/parameter_table_0514.pdf)')
    # key model processes , help_text="Please provide yes/no and a short description how the process is included"
    assimilation = models.TextField(null=True, blank=True, default='', verbose_name='Assimilation')
    respiration = models.TextField(null=True, blank=True, default='', verbose_name='Respiration')
    carbon_allocation = models.TextField(null=True, blank=True, default='', verbose_name='Carbon allocation')
    regeneration_planting = models.TextField(null=True, blank=True, default='', verbose_name='Regeneration/planting')
    soil_water_balance = models.TextField(null=True, blank=True, default='', verbose_name='Soil water balance')
    carbon_nitrogen_balance = models.TextField(null=True, blank=True, default='', verbose_name='Carbon/Nitrogen balance')
    feedbacks_considered = models.TextField(null=True, blank=True, default='', verbose_name='Are feedbacks considered that reflect the influence of changing carbon state variables on the other system components and driving data (i.e. Growth (leaf area), light, temperature, water availability, nutrient availability)?')
    # Forest Model Output Specifications
    initial_state = models.TextField(null=True, blank=True, default='', verbose_name='Do you provide the initial state in your simulation outputs (i.e., at year 0; before the simulation starts)?')
    total_calculation = models.TextField(null=True, blank=True, default='', verbose_name='When you report a variable as "xxx-total" does it equal the (sum of) "xxx-species" value(s)? or are there confounding factors such as ground/herbaceous vegetation contributing to the "total" in your model?')
    output_dbh_class = models.TextField(null=True, blank=True, default='', verbose_name='Did you report any output per dbh-class? if yes, which variables?')


    class Meta:
        verbose_name_plural = 'Forests'
        verbose_name = 'Forests'

    def values_to_tuples(self):
        vname = self._get_verbose_field_name_question
        generic = super(BiomesForests, self).values_to_tuples()
        return [
            ('Model set-up specifications', [
                (vname('initialize_model'), self.initialize_model),
                (vname('data_profound_db'), self.data_profound_db),
                (vname('management_implementation'), self.management_implementation),
                (vname('harvesting_simulated'), self.harvesting_simulated),
                (vname('regenerate'), self.regenerate),
                (vname('unmanaged_simulations'), self.unmanaged_simulations),
                (vname('noco2_scenario'), self.noco2_scenario),
                (vname('leap_years'), self.leap_years),
                (vname('simulate_minor_tree'), self.simulate_minor_tree),
                (vname('nitrogen_simulation'), self.nitrogen_simulation),
                (vname('soil_depth'), self.soil_depth),
                (vname('stochastic_element'), self.stochastic_element),
                (vname('minimum_diameter_tree'), self.minimum_diameter_tree),
                (vname('model_historically_calibrated'), self.model_historically_calibrated),
                (vname('upload_parameter_list'), self.upload_parameter_list),
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
                (vname('assimilation'), self.assimilation),
                (vname('respiration'), self.respiration),
                (vname('carbon_allocation'), self.carbon_allocation),
                (vname('regeneration_planting'), self.regeneration_planting),
                (vname('soil_water_balance'), self.soil_water_balance),
                (vname('carbon_nitrogen_balance'), self.carbon_nitrogen_balance),
                (vname('feedbacks_considered'), self.feedbacks_considered),
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
            ('Species / Plant Functional Types (PFTs)', [
                (vname('list_of_pfts'), self.list_of_pfts),
                (vname('pfts_comments'), self.pfts_comments),
            ]),
            ('Model output specifications', [
                (vname('initial_state'), self.initial_state),
                (vname('output'), self.output),
                (vname('output_per_pft'), self.output_per_pft),
                (vname('total_calculation'), self.total_calculation),
                (vname('output_dbh_class'), self.output_dbh_class),
                (vname('considerations'), self.considerations),
            ]),
        ] + generic


class Energy(BaseSector):
    # Model & Method Characteristics
    model_type = models.TextField(null=True, blank=True, default='', verbose_name='Model type')
    temporal_extent = models.TextField(null=True, blank=True, default='', verbose_name='Temporal extent')
    temporal_resolution = models.TextField(null=True, blank=True, default='', verbose_name='Temporal resolution')
    data_format_for_input = models.TextField(null=True, blank=True, default='', verbose_name='Data format for input')
    # Impact Types
    impact_types_energy_demand = models.TextField(null=True, blank=True, default='', verbose_name='Energy demand (heating & cooling)')
    impact_types_temperature_effects_on_thermal_power = models.TextField(null=True, blank=True, default='', verbose_name='Temperature effects on thermal power')
    impact_types_weather_effects_on_renewables = models.TextField(null=True, blank=True, default='', verbose_name='Weather effects on renewables')
    impact_types_water_scarcity_impacts = models.TextField(null=True, blank=True, default='', verbose_name='Water scarcity impacts')
    impact_types_other = models.TextField(null=True, blank=True, default='', verbose_name='Other (agriculture, infrastructure, adaptation)')
    # Output
    output_energy_demand = models.TextField(null=True, blank=True, default='', verbose_name='Energy demand (heating & cooling)')
    output_energy_supply = models.TextField(null=True, blank=True, default='', verbose_name='Energy supply')
    output_water_scarcity = models.TextField(null=True, blank=True, default='', verbose_name='Water scarcity')
    output_economics = models.TextField(null=True, blank=True, default='', verbose_name='Economics')
    output_other = models.TextField(null=True, blank=True, default='', verbose_name='Other (agriculture, infrastructure, adaptation)')
    # Further Information
    variables_not_directly_from_GCMs = models.TextField(null=True, blank=True, default='', verbose_name='Variables not directly from GCMs', help_text='How are these calculated (including equations)?')
    response_function_of_energy_demand_to_HDD_CDD = models.TextField(null=True, blank=True, default='', verbose_name='Response function of energy demand to HDD/CDD', help_text='Including equations where appropriate')
    factor_definition_and_calculation = models.TextField(null=True, blank=True, default='', verbose_name='Definition and calculation of variable potential and load factor', help_text='Are these endogenous or exogenous to the model?')
    biomass_types = models.TextField(null=True, blank=True, default='', verbose_name='Biomass types', help_text='1st generation, 2nd generation, residues...')
    maximum_potential_assumption = models.TextField(null=True, blank=True, default='', verbose_name='Maximum potential assumption', help_text='Which information source is used?')
    bioenergy_supply_costs = models.TextField(null=True, blank=True, default='', verbose_name='Bioenergy supply costs', help_text='Include information on the functional forms and the data sources for deriving the supply curves')
    socioeconomic_input = models.TextField(null=True, blank=True, default='', verbose_name='Socio-economic input', help_text='Are SSP storylines implemented, or just GDP and population scenarios?')

    def values_to_tuples(self):
        vname = self._get_verbose_field_name
        generic = super(Energy, self).values_to_tuples()
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
        ] + generic


class MarineEcosystems(BaseSector):
    defining_features = models.TextField(null=True, blank=True, default='', verbose_name='Defining features')
    spatial_scale = models.TextField(null=True, blank=True, default='', verbose_name='Spatial scale')
    spatial_resolution = models.TextField(null=True, blank=True, default='', verbose_name='Spatial resolution')
    temporal_scale = models.TextField(null=True, blank=True, default='', verbose_name='Temporal scale')
    temporal_resolution = models.TextField(null=True, blank=True, default='', verbose_name='Temporal resolution')
    taxonomic_scope = models.TextField(null=True, blank=True, default='', verbose_name='Taxonomic scope')
    vertical_resolution = models.TextField(null=True, blank=True, default='', verbose_name='Vertical resolution')
    spatial_dispersal_included = models.TextField(null=True, blank=True, default='', verbose_name='Spatial dispersal included')
    fishbase_used_for_mass_length_conversion = models.TextField(
        null=True, blank=True, default='', verbose_name='Is FishBase used for mass-length conversion?')

    def values_to_tuples(self):
        vname = self._get_verbose_field_name
        generic = super(MarineEcosystems, self).values_to_tuples()
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
        ] + generic

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


class Water(BaseSector):
    technological_progress = models.TextField(
        null=True, blank=True, default='',
        help_text='Does the model account for GDP changes and technological progress? If so, how are these integrated into the runs?'
    )
    soil_layers = models.TextField(null=True, blank=True, default='',
                                   help_text='How many soil layers are used? Which qualities do they have?')
    water_use = models.TextField(null=True, blank=True, default='', verbose_name='Water-use types',
                                 help_text='Which types of water use are included in the model?')
    water_sectors = models.TextField(
        null=True, blank=True, default='', verbose_name='Water-use sectors',
        help_text='For the global-water-model varsoc and pressoc runs, which water sectors were included? E.g. irrigation, domestic, manufacturing, electricity, livestock.')
    routing = models.TextField(null=True, blank=True, default='', verbose_name='Runoff routing', help_text='How is runoff routed?')
    routing_data = models.TextField(null=True, blank=True, default='', help_text='Which routing data are used?')
    land_use = models.TextField(null=True, blank=True, default='', verbose_name='Land-use change effects',
                                help_text='Which land-use change effects are included?')
    dams_reservoirs = models.TextField(null=True, blank=True, default='', verbose_name='Dam and reservoir implementation',
                                       help_text='Describe how are dams and reservoirs are implemented')

    calibration = models.NullBooleanField(verbose_name='Was the model calibrated?', default=None)
    calibration_years = models.TextField(null=True, blank=True, default='', verbose_name='Which years were used for calibration?')
    calibration_dataset = models.TextField(null=True, blank=True, default='', verbose_name='Which dataset was used for calibration?',
                                           help_text='E.g. WFD, GSWP3')
    calibration_catchments = models.TextField(null=True, blank=True, default='',
                                              verbose_name='How many catchments were callibrated?')
    vegetation = models.NullBooleanField(verbose_name='Is CO2 fertilisation accounted for?', default=None)
    vegetation_representation = models.TextField(null=True, blank=True, default='', verbose_name='How is vegetation represented?')
    methods_evapotranspiration = models.TextField(null=True, blank=True, default='', verbose_name='Potential evapotranspiration')
    methods_snowmelt = models.TextField(null=True, blank=True, default='', verbose_name='Snow melt')

    def values_to_tuples(self):
        vname = self._get_verbose_field_name
        generic = super(Water, self).values_to_tuples()
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
        ] + generic

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


class Biodiversity(BaseSector):
    MODEL_ALGORITHM_CHOICES = (
        ('GAM', 'Generalised Additive Model (GAM)'),
        ('GBM', 'Generalized Boosted Models (GBM)'),
        ('RF', 'Random Forest (RF)'),
        ('MaxEnt', 'Maximum Entropy (MaxEnt)')
    )
    model_algorithm = models.CharField(null=True, blank=True, choices=MODEL_ALGORITHM_CHOICES, verbose_name='Model algorithm', max_length=255)
    explanatory_variables = models.TextField(null=True, blank=True, default='', verbose_name='Explanatory variables')
    RESPONSE_VARIABLE_CHOICES = (
        ('absence/presence of species', 'absence/presence of species'),
        ('species richness of taxon', 'species richness of taxon'),
    )
    response_variable = models.CharField(null=True, blank=True, choices=RESPONSE_VARIABLE_CHOICES, verbose_name='Response variable', max_length=255)
    additional_information_response_variable = models.TextField(null=True, blank=True, default='', verbose_name='Additional information about response variable')
    DISTRIBUTION_RESPONSE_CHOICES = (
        ('Binomial', 'Binomial'),
        ('Poisson', 'Poisson'),
    )
    distribution_response_variable = models.CharField(null=True, blank=True, choices=DISTRIBUTION_RESPONSE_CHOICES, verbose_name='Distribution of response variable', max_length=255)
    parameters = models.TextField(null=True, blank=True, default='', verbose_name='Parameters')
    additional_info_parameters = models.TextField(null=True, blank=True, default='', verbose_name='Additional Information about Parameters')
    SOFTWARE_FUNCTION_CHOICES = (
        ('gam()', 'gam()'),
        ('gbm()', 'gbm()'),
        ('randomForest()', 'randomForest()'),
        ('maxent()', 'maxent()')
    )
    software_function = models.CharField(null=True, blank=True, choices=SOFTWARE_FUNCTION_CHOICES, verbose_name='Software function', max_length=255)
    SOFTWARE_PACKAGE_CHOICES = (
        ('mgcv', 'mgcv'),
        ('gbm', 'gbm'),
        ('dismo', 'dismo'),
        ('randomForest', 'randomForest')
    )
    software_package = models.CharField(null=True, blank=True, choices=SOFTWARE_PACKAGE_CHOICES, verbose_name='Software package', max_length=255)
    software_program = models.TextField(null=True, blank=True, default='', verbose_name='Software program')
    MODEL_OUTPUT_CHOICES = (
        ('probability of occurrence', 'probability of occurrence'),
        ('relative probability of occurrence', 'relative probability of occurrence'),
        ('summed probability of occurrence', 'summed probability of occurrence'),
    )
    model_output = models.CharField(null=True, blank=True, choices=MODEL_OUTPUT_CHOICES, verbose_name='Model output', max_length=255)
    additional_info_model_output = models.TextField(null=True, blank=True, default='', verbose_name='Additional Information about Model output')

    class Meta:
        verbose_name = 'Biodiversity'
        verbose_name_plural = 'Biodiversity'

    def values_to_tuples(self):
        vname = self._get_verbose_field_name
        generic = super(Biodiversity, self).values_to_tuples()
        return [
            ('Model specifications', [
                (vname('model_algorithm'), self.model_algorithm),
                (vname('explanatory_variables'), self.explanatory_variables),
                (vname('response_variable'), self.response_variable),
                (vname('additional_information_response_variable'), self.additional_information_response_variable),
                (vname('distribution_response_variable'), self.distribution_response_variable),
                (vname('parameters'), self.parameters),
                (vname('additional_info_parameters'), self.additional_info_parameters),
                (vname('software_function'), self.software_function),
                (vname('software_package'), self.software_package),
                (vname('software_program'), self.software_program),
                (vname('model_output'), self.model_output),
                (vname('additional_info_model_output'), self.additional_info_model_output),
            ]),
        ] + generic


class Health(BaseSector):
    pass


class CoastalInfrastructure(BaseSector):
    class Meta:
        verbose_name = 'Coastal Infrastructure'
        verbose_name_plural = 'Coastal Infrastructure'


class Permafrost(BaseSector):
    pass


class ComputableGeneralEquilibriumModelling(BaseSector):
    class Meta:
        verbose_name = verbose_name_plural = 'Computable General Equilibrium Modelling'


class AgroEconomicModelling(BaseSector):
    class Meta:
        verbose_name = verbose_name_plural = 'Agro-Economic Modelling'


class OutputData(models.Model):
    model = models.ForeignKey(ImpactModel, null=True, blank=True, on_delete=models.CASCADE)
    scenarios = models.ManyToManyField(Scenario, blank=True)
    experiments = models.CharField(max_length=500, null=True, blank=True)
    drivers = models.ManyToManyField(InputData)
    date = models.DateField()

    class Meta:
        verbose_name = verbose_name_plural = 'Output data'
        verbose_name = verbose_name_plural = 'Output data'

    def duplicate(self):
        duplicate = OutputData(
            model=self.model,
            experiments=self.experiments,
            date=self.date
        )
        duplicate.save()
        duplicate.scenarios.set(self.scenarios.all())
        duplicate.drivers.set(self.drivers.all())
        return duplicate
    
    def __str__(self):
        if self.model:
            return "%s : %s" % (self.model.base_model.sector, self.model.base_model.name)
        return "%s" % self.pk


def impact_model_path(instance, filename):
    return 'impact_model_attachments/{0}-{1}'.format(instance.impact_model.id, filename)


class Attachment(models.Model):
    impact_model = models.OneToOneField(ImpactModel)
    attachment1 = models.FileField(null=True, blank=True, verbose_name="Attachment", upload_to=impact_model_path, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'txt', 'csv'])])
    attachment1_description = models.TextField(null=True, blank=True, verbose_name="Description")
    attachment2 = models.FileField(null=True, blank=True, verbose_name="Attachment", upload_to=impact_model_path, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'txt', 'csv'])])
    attachment2_description = models.TextField(null=True, blank=True, verbose_name="Description")
    attachment3 = models.FileField(null=True, blank=True, verbose_name="Attachment", upload_to=impact_model_path, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'txt', 'csv'])])
    attachment3_description = models.TextField(null=True, blank=True, verbose_name="Description")
    attachment4 = models.FileField(null=True, blank=True, verbose_name="Attachment", upload_to=impact_model_path, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'txt', 'csv'])])
    attachment4_description = models.TextField(null=True, blank=True, verbose_name="Description")
    attachment5 = models.FileField(null=True, blank=True, verbose_name="Attachment", upload_to=impact_model_path, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'txt', 'csv'])])
    attachment5_description = models.TextField(null=True, blank=True, verbose_name="Description")

    def _get_verbose_field_name(self, field):
        fieldmeta = self._meta.get_field(field)
        ret = fieldmeta.verbose_name.title()
        if fieldmeta.help_text:
            ret = generate_helptext(fieldmeta.help_text, ret)
        return ret

    def values_to_tuples(self):
        vname = self._get_verbose_field_name
        tuples = []
        if self.attachment1:
            tuples.append(('', '<a href="%s" target="_blank"><i class="fa fa-download"></i> %s (%s)</a> %s' % (self.attachment1.url, os.path.basename(self.attachment1.name), filesizeformat(self.attachment1.size), self.attachment1_description or '')))
        if self.attachment2:
            tuples.append(('', '<a href="%s" target="_blank"><i class="fa fa-download"></i> %s (%s)</a> %s' % (self.attachment2.url, os.path.basename(self.attachment2.name), filesizeformat(self.attachment2.size), self.attachment2_description or '')))
        if self.attachment3:
            tuples.append(('', '<a href="%s" target="_blank"><i class="fa fa-download"></i> %s (%s)</a> %s' % (self.attachment3.url, os.path.basename(self.attachment3.name), filesizeformat(self.attachment3.size), self.attachment3_description or '')))
        if self.attachment4:
            tuples.append(('', '<a href="%s" target="_blank"><i class="fa fa-download"></i> %s (%s)</a> %s' % (self.attachment4.url, os.path.basename(self.attachment4.name), filesizeformat(self.attachment4.size), self.attachment4_description or '')))
        if self.attachment5:
            tuples.append(('', '<a href="%s" target="_blank"><i class="fa fa-download"></i> %s (%s)</a> %s' % (self.attachment5.url, os.path.basename(self.attachment5.name), filesizeformat(self.attachment5.size), self.attachment5_description or '')))
        return [('Attachments', tuples )]


class DataPublicationConfirmation(models.Model):
    impact_model = models.OneToOneField(ImpactModel, on_delete=models.PROTECT, related_name='confirmation')
    created = models.DateTimeField(auto_now_add=True)
    email_text = models.TextField(help_text="Please insert information on the experiments that are to be published here (required).")

    is_confirmed = models.BooleanField(default=False)
    confirmed_date = models.DateTimeField(null=True, blank=True)
    confirmed_by = models.ForeignKey(User, null=True, blank=True)
    confirmed_license = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = "Data publication confirmation"
        verbose_name_plural = "Data publication confirmations"
