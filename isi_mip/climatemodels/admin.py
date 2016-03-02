from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.core import urlresolvers

from .models import *

class ImpactModelAdmin(admin.ModelAdmin):
    def sector_link(self, obj):
        try:
            adminurl = "admin:%s_change" % obj.fk_sector._meta.db_table
            link=urlresolvers.reverse(adminurl, args=[obj.fk_sector.id])
            return '<a href="%s">%s</a>' % (link,obj.fk_sector)
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
    readonly_fields = ('sector_link', )

    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'sector', 'sector_link', 'region', 'version',
                       'contact_person_name', 'contact_person_email', 'contact_person_institute',
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


class HideAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class HideSectorAdmin(HideAdmin):
    # readonly_fields = ('impact_model',)
    pass

admin.site.register(ImpactModel, ImpactModelAdmin)
admin.site.register(InputData)
admin.site.register(OutputData)

admin.site.register(Agriculture, HideSectorAdmin)
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