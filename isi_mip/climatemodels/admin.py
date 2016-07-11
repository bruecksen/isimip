from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.core import urlresolvers
from django.core.urlresolvers import NoReverseMatch

from isi_mip.sciencepaper.models import Author
from .models import *


class HideAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class HideSectorAdmin(HideAdmin):
    readonly_fields = ('impact_model',)


class ContactPersonAdmin(admin.TabularInline):
    model = ContactPerson
    extra = 1


class ImpactModelAdmin(admin.ModelAdmin):
    def sector_link(self, obj):
        try:
            adminurl = "admin:%s_change" % obj.fk_sector._meta.db_table
            link = urlresolvers.reverse(adminurl, args=[obj.fk_sector.id])
            return '<a href="%s">%s</a>' % (link, obj.fk_sector._meta.verbose_name)
        except NoReverseMatch:
            return '<span style="color:#666;">{} has no specific attributes.</span>'.format(obj.fk_sector._meta.verbose_name)
        except KeyError:
            return '<span style="color:#666;">will be shown, once the model is saved.</span>'
    sector_link.allow_tags = True
    sector_link.short_description = 'Sector settings'
    readonly_fields = ('sector_link',)
    list_display = ('name', 'sector', 'public', )
    list_filter = ('public', 'sector' )
    inlines = [ContactPersonAdmin]

    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'sector', 'sector_link', 'region', 'simulation_round',
                       'version',
                       'main_reference_paper', 'other_references', 'short_description']}
         ),
        ('Technical Information', {
            'fields': [
                # resolution
                'spatial_aggregation', 'spatial_resolution', 'spatial_resolution_info', 'temporal_resolution_climate',
                'temporal_resolution_co2', 'temporal_resolution_land', 'temporal_resolution_soil',
                'temporal_resolution_info',
                # input data
                'climate_data_sets', 'climate_variables', 'climate_variables_info',
                'socioeconomic_input_variables', 'soil_dataset', 'additional_input_data_sets',
                # more
                'exceptions_to_protocol', 'spin_up', 'spin_up_design',
                'natural_vegetation_partition', 'natural_vegetation_dynamics', 'natural_vegetation_cover_dataset',
                'management', 'extreme_events',
                'anything_else', 'owner', 'public',
            ],
        }),
    ]


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


admin.site.register(ImpactModel, ImpactModelAdmin)
admin.site.register(InputData)
admin.site.register(OutputData)

admin.site.register(Agriculture, AgricultureAdmin)
admin.site.register(Energy, HideSectorAdmin)
admin.site.register(WaterGlobal, HideSectorAdmin)
admin.site.register(WaterRegional, HideSectorAdmin)
admin.site.register(Biomes, HideSectorAdmin)
admin.site.register(Forests, HideSectorAdmin)
admin.site.register(MarineEcosystemsGlobal, HideSectorAdmin)
admin.site.register(MarineEcosystemsRegional, HideSectorAdmin)
admin.site.register(Biodiversity, HideSectorAdmin)
# admin.site.register(Health, HideSectorAdmin)
# admin.site.register(CoastalInfrastructure, HideSectorAdmin)
# admin.site.register(Permafrost, HideSectorAdmin)
# admin.site.register(ComputableGeneralEquilibriumModelling, HideSectorAdmin)
# admin.site.register(AgroEconomicModelling, HideSectorAdmin)

admin.site.register(ClimateDataType)
admin.site.register(ClimateVariable)
admin.site.register(InputPhase)
admin.site.register(ReferencePaper)
admin.site.register(Author, HideAdmin)
admin.site.register(Region)
admin.site.register(Scenario)
admin.site.register(SocioEconomicInputVariables)
admin.site.register(ContactPerson)
admin.site.register(SimulationRound)
admin.site.register(SpatialAggregation)