from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.core import urlresolvers

from .models import *


class HideAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class HideSectorAdmin(HideAdmin):
    # readonly_fields = ('impact_model',)
    pass


class ContactPersonAdmin(admin.TabularInline):
    model = ContactPerson
    extra = 1


class ImpactModelAdmin(admin.ModelAdmin):
    def sector_link(self, obj):
        try:
            adminurl = "admin:%s_change" % obj.fk_sector._meta.db_table
            link = urlresolvers.reverse(adminurl, args=[obj.fk_sector.id])
            return '<a href="%s">%s</a>' % (link, obj.fk_sector)
        except:
            return

    sector_link.allow_tags = True
    sector_link.short_description = 'Sector link'
    #
    # def trenner(self, obj):
    #     return '<hl />'
    #
    # trenner.allow_tags = True
    # trenner.short_description = 'trennerli'
    readonly_fields = ('sector_link',)

    inlines = [ContactPersonAdmin]

    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'sector', 'sector_link', 'region', 'version',
                       'main_reference_paper', 'additional_papers', 'short_description']}
         ),
        ('Technical Information', {
            'fields': [
                # resolution
                'resolution', 'temporal_resolution_climate', 'temporal_resolution_co2',
                'temporal_resolution_land', 'temporal_resolution_soil',
                # input data
                'climate_data_sets', 'climate_variables',
                'socioeconomic_input_variables', 'soil_dataset', 'additional_input_data_sets',
                # more
                'exceptions_to_protocol', 'spin_up', 'spin_up_design',
                'natural_vegetation_partition', 'natural_vegetation_simulation', 'natural_vegetation_cover_dataset',
                'management', 'extreme_events',
                'anything_else', 'comments'
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
admin.site.register(Water, HideSectorAdmin)
admin.site.register(Biomes, HideSectorAdmin)
admin.site.register(MarineEcosystems, HideSectorAdmin)
admin.site.register(Biodiversity, HideSectorAdmin)
admin.site.register(Health, HideSectorAdmin)
admin.site.register(CoastalInfrastructure, HideSectorAdmin)
admin.site.register(Permafrost, HideSectorAdmin)

admin.site.register(ClimateDataType, HideAdmin)
admin.site.register(ClimateVariable, HideAdmin)
admin.site.register(InputPhase, HideAdmin)
admin.site.register(ReferencePaper, HideAdmin)
admin.site.register(Region, HideAdmin)
admin.site.register(Scenario, HideAdmin)
admin.site.register(SocioEconomicInputVariables, HideAdmin)
admin.site.register(ContactPerson, HideAdmin)
admin.site.register(SimulationRound, HideAdmin)