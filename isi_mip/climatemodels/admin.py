from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.core import urlresolvers
from django.core.urlresolvers import NoReverseMatch
from django.forms import CheckboxSelectMultiple

from isi_mip.sciencepaper.models import Author
from .models import *


class HideAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class SimulationRoundAdmin(admin.ModelAdmin):
    model = SimulationRound
    prepopulated_fields = {'slug': ('name',), }
    list_display = ('name', 'order')


class HideSectorAdmin(HideAdmin):
    readonly_fields = ('impact_model',)


class ContactPersonAdmin(admin.TabularInline):
    model = ContactPerson
    extra = 1


class BaseImpactModelAdmin(admin.ModelAdmin):
    model = BaseImpactModel
    inlines = [ContactPersonAdmin, ]
    list_display = ('name', 'sector')
    list_filter = ('sector',)


class TechnicalInformationAdmin(admin.StackedInline):
    model = TechnicalInformation


class InputDataInformationAdmin(admin.StackedInline):
    model = InputDataInformation


class OtherInformationAdmin(admin.StackedInline):
    model = OtherInformation


class ImpactModelAdmin(admin.ModelAdmin):
    inlines = [TechnicalInformationAdmin, InputDataInformationAdmin, OtherInformationAdmin]
    model = ImpactModel

    def get_name(self, obj):
        return obj.base_model.name
    get_name.admin_order_field = 'base_model__name'
    get_name.short_description = 'Name'

    def get_sector(self, obj):
        return obj.base_model.sector
    get_sector.admin_order_field = 'sector__name'
    get_sector.short_description = 'Sector'

    def sector_link(self, obj):
        try:
            adminurl = "admin:%s_%s_change" % (obj.fk_sector._meta.app_label, obj.fk_sector._meta.model_name)
            link = urlresolvers.reverse(adminurl, args=[obj.fk_sector.id])
            return '<a href="%s">%s</a>' % (link, obj.fk_sector)
        except NoReverseMatch:
            return '<span style="color:#666;">{} has no specific attributes.</span>'.format(obj.fk_sector._meta.verbose_name)
        except KeyError:
            return '<span style="color:#666;">will be shown, once the model is saved.</span>'
    sector_link.allow_tags = True
    sector_link.short_description = 'Sector settings'
    readonly_fields = ('sector_link',)
    list_display = ('get_name', 'simulation_round', 'get_sector', 'public')
    list_filter = ('public', 'base_model__sector',)


class AgricultureAdmin(HideSectorAdmin):
    fieldsets = [
        ('Key input and management', {
            'fields': [
                'crops', 'land_coverage', 'planting_date_decision',
                'planting_density', 'crop_cultivars', 'fertilizer_application',
                'irrigation', 'crop_residue', 'initial_soil_water',
                'initial_soil_nitrate_and_ammonia',
                'initial_soil_C_and_OM', 'initial_crop_residue'
            ]}
         ),
        ('Key model processes', {
            'fields': [
                'lead_area_development', 'light_interception', 'light_utilization', 'yield_formation',
                'crop_phenology', 'root_distribution_over_depth', 'stresses_involved', 'type_of_water_stress',
                'type_of_heat_stress', 'water_dynamics', 'evapo_transpiration', 'soil_CN_modeling',
                'co2_effects',
            ],
        }),
        ('Methods for model calibration and validation', {
            'fields': [
                'parameters_number_and_description', 'calibrated_values', 'output_variable_and_dataset',
                'spatial_scale_of_calibration_validation', 'temporal_scale_of_calibration_validation',
                'criteria_for_evaluation']
        })
    ]


class DataTypeAdmin(admin.ModelAdmin):
    model = DataType
    list_display = ('name', 'is_climate_data_type')
    list_filter = ('is_climate_data_type',)


class SectorAdmin(admin.ModelAdmin):
    model = Sector
    list_display = ('name', 'class_name')
    prepopulated_fields = {'slug': ('name',), }


class SectorInformationFieldAdmin(admin.StackedInline):
    model = SectorInformationField
    prepopulated_fields = {'identifier': ('name',), }


class SectorInformationGroupAdmin(admin.ModelAdmin):
    model = SectorInformationGroup
    inlines = [SectorInformationFieldAdmin]
    prepopulated_fields = {'identifier': ('name',), }

    def get_sector(self, obj):
        return obj.sector.name
    get_sector.admin_order_field = 'sector__name'
    get_sector.short_description = 'Sector'
    list_display = ('get_sector', 'name', 'order')
    list_filter = ('sector__name', )


class InputDataAdmin(admin.ModelAdmin):
    model = InputData
    list_display = ('name', 'data_type', )
    list_filter = ('data_type', )
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


class ClimateVariableAdmin(admin.ModelAdmin):
    model = ClimateVariable

    def get_type(self, obj):
        return ','.join(set([input_data.data_type.name for input_data in obj.inputdata_set.all().distinct()]))
    get_type.admin_order_field = 'sector__name'
    get_type.short_description = 'Data type'
    list_display = ('name', 'abbreviation', 'get_type')
    list_filter = ('inputdata__data_type__name',)


admin.site.register(BaseImpactModel, BaseImpactModelAdmin)
admin.site.register(ImpactModel, ImpactModelAdmin)
admin.site.register(InputData, InputDataAdmin)
admin.site.register(OutputData)
admin.site.register(Sector, SectorAdmin)
admin.site.register(Agriculture, AgricultureAdmin)
admin.site.register(Energy, HideSectorAdmin)
admin.site.register(WaterGlobal, HideSectorAdmin)
admin.site.register(WaterRegional, HideSectorAdmin)
admin.site.register(Biomes, HideSectorAdmin)
admin.site.register(Forests, HideSectorAdmin)
admin.site.register(MarineEcosystemsGlobal, HideSectorAdmin)
admin.site.register(MarineEcosystemsRegional, HideSectorAdmin)
admin.site.register(Biodiversity, HideSectorAdmin)
admin.site.register(GenericSector, HideSectorAdmin)

admin.site.register(SectorInformationGroup, SectorInformationGroupAdmin)

admin.site.register(DataType, DataTypeAdmin)
admin.site.register(ClimateVariable, ClimateVariableAdmin)
admin.site.register(ReferencePaper)
admin.site.register(Author, HideAdmin)
admin.site.register(Region)
admin.site.register(Scenario)
admin.site.register(SocioEconomicInputVariables)
admin.site.register(ContactPerson)
admin.site.register(SimulationRound, SimulationRoundAdmin)
admin.site.register(SpatialAggregation)