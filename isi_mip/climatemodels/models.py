from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from isi_mip.choiceorotherfield.models import ChoiceOrOtherField


class ReferencePaper(models.Model):
    name = models.CharField(max_length=500)
    climate_model = models.ForeignKey('General', null=True, blank=True)

    def __str__(self):
        return self.name

class ClimateDataSet(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class ClimateVariable(models.Model):
    name = models.CharField(max_length=500)
    abbrevation = models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return "%s (%s)" % (self.name, self.abbrevation)


class SocioEconomicInputVariables(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class General(models.Model):
    name = models.CharField(
        max_length=500
    )
    region = models.CharField(max_length=500)
    contact_person = models.ForeignKey(User,null=True,blank=True)
    version = models.CharField(max_length=500,null=True,blank=True)
    main_reference_paper = models.ForeignKey(ReferencePaper,null=True,blank=True)
    short_description = models.TextField(null=True,blank=True)

    # technical information
    RESOLUTION_CHOICES = (
        ('0.5°x0.5°', '0.5°x0.5°'),
    )
    resolution = ChoiceOrOtherField(
        max_length=500,
        choices=RESOLUTION_CHOICES,
        blank=True, null=True
    )
    TEMPORAL_RESOLUTION_CLIMATE_CHOICES = (
        ('daily','daily'), ('monthly','monthly'), ('annual','annual'),
    )
    temporal_resolution_climate = ChoiceOrOtherField(
        max_length=500,
        choices=TEMPORAL_RESOLUTION_CLIMATE_CHOICES,
        blank=True, null=True
    )
    temporal_resolution_co2 = ChoiceOrOtherField(
        max_length=500,
        choices=(('annual','annual'),),
        blank=True, null=True
    )
    temporal_resolution_land = ChoiceOrOtherField(
        max_length=500,
        choices=(('annual','annual'),),
        blank=True, null=True
    )
    temporal_resolution_soil = ChoiceOrOtherField(
        max_length=500,
        choices=(('annual','annual'),),
        blank=True, null=True
    )

    # input data
    climate_data_sets = models.ManyToManyField(ClimateDataSet, blank=True)
    climate_variables = models.ManyToManyField(ClimateVariable, blank=True)
    socioeconomic_input_variables = models.ManyToManyField(SocioEconomicInputVariables, blank=True)
    soil_dataset = models.TextField(
        null=True, blank=True,
        help_text= 'Soil dataset'
    )
    additional_input_data_sets = models.TextField(
        null=True, blank=True,
        help_text= 'Additional input data sets'
    )

    # other
    exceptions_to_protocol = models.TextField(
        null=True, blank=True,
        help_text= 'Did you have to overrule any settings prescribed by the protocol in order to get your model running?'
    )
    spin_up = models.NullBooleanField(
        help_text='Did you spin-up your model?'
    )
    spin_up_design = models.TextField(
        null=True, blank=True,
        help_text= 'Spin-up design'
    )
    natural_vegetation_partition = models.TextField(
        null=True, blank=True,
        help_text= 'How are areas covered by different types of natural vegetation partitioned?'
    )
    natural_vegetation_simulation = models.TextField(
        null=True, blank=True,
        help_text= 'Do your simulate your own (dynamic) natural vegetation? If so, please describe'
    )
    natural_vegetation_cover_dataset = models.TextField(
        null=True, blank=True,
        help_text= 'If you prescribe natural vegetation cover, which dataset do you use?'
    )
    management = models.TextField(
        null=True, blank=True,
        help_text= 'What specific management and autonomous adaptation measures did you apply?'
    )
    extreme_events = models.TextField(
        null=True, blank=True,
        help_text= 'Key challenges for model in reproducing impacts of extreme events'
    )
    anything_else = models.TextField(
        null=True, blank=True,
        help_text= 'Anything else necessary to reproduce and/or understand the simulation output'
    )
    comments = models.TextField(
        null=True, blank=True,
        help_text= 'Additional comments'
    )










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


class Sector(models.Model):
    general = models.OneToOneField(General)

    subsectors = ['biomes', 'agriculture', 'water', 'energy',
                  'agroeconomicmodelling', 'permafrost',
                  'coastalinfrastructure', 'health']

    class Meta:
        abstract = True


class Biomes(Sector):
    pass


class Agriculture(Sector):
    pass


class Water(Sector):
    technological_progress = models.TextField(
        null=True, blank=True,
        help_text=('Does your model account for GDP changes and technological progress? If so, how?'),
    )
    soil = models.TextField(
        null=True, blank=True,
        help_text=('How many soil layers are there?'),
    )
    water_use = models.TextField(
        null=True, blank=True,
        help_text=('What types of water use can your model include?'),
    )
    water_sectors = models.TextField(
        null=True, blank=True,
        help_text=('For the global water model varsoc and pressoc runs, which water sectors did you include?'),
    )
    routing = models.TextField(
        null=True, blank=True,
        help_text=('How do you route runoff in your model?'),
    )
    routing_data = models.TextField(
        null=True, blank=True,
        help_text=('What routing data do you use?'),
    )
    land_use = models.TextField(
        null=True, blank=True,
        help_text=('What effects of land-use change does your model include?'),
    )
    dams_reservoirs = models.TextField(
        null=True, blank=True,
        help_text=('How are dams and reservoirs implemented?'),
    )
    calibration = models.NullBooleanField(help_text='Was the model calibrated?')

    calibration_years = models.TextField(
        null=True, blank=True,
        help_text=('Which years were used for calibration?'),
    )
    calibration_dataset = models.TextField(
        null=True, blank=True,
        help_text=('Which dataset was used for calibration?'),
    )
    calibration_catchments = models.TextField(
        null=True, blank=True,
        help_text=('For approximately how many catchments was the calibration carried out?'),
    )
    vegetation = models.NullBooleanField(help_text='Do you account for CO2 fertilisation?')
    vegetation_presentation = models.TextField(
        null=True, blank=True,
        help_text=('How is vegetation represented?'),
    )
    methods_evapotraspiration = models.TextField(
        null=True, blank=True,
        help_text=('Potential evapotraspiration'),
    )
    methods_snowmelt = models.TextField(
        null=True, blank=True,
        help_text=('Snow melt'),
    )

    def __str__(self):
        return 'Water'





class Energy(Sector):
    pass


class AgroEconomicModelling(Sector):
    pass


class Permafrost(Sector):
    pass


class CoastalInfrastructure(Sector):
    pass


class Health(Sector):
    pass
