from django.contrib import admin

from .models import *


# class WaterAdmin(admin.StackedInline):
#     model = Water
#
# class GeneralAdmin(admin.ModelAdmin):
#     inlines = [WaterAdmin]


# class ReferencePaperInlineAdmin(admin.TabularInline):
#     model = ReferencePaper
#     extra = 1

class GeneralAdmin(admin.ModelAdmin):
    # def sector(self, obj):
    #     try:
    #         adminurl = "admin:%s_change" % obj.sector._meta.db_table
    #         link=urlresolvers.reverse(adminurl, args=[obj.sector.id])
    #         return '<a href="%s">%s</a>' % (link,obj.sector)
    #     except:
    #         return
    # sector.allow_tags = True
    #
    # def trenner(self, obj):
    #     return '<hl />'
    #
    # trenner.allow_tags = True
    # trenner.short_description = 'trennerli'
    # readonly_fields = ('sector', 'trenner')

    # inlines = [ReferencePaperInlineAdmin]

    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'sector', 'region', 'contact_person', 'version',
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

admin.site.register(General, GeneralAdmin)
admin.site.register(InputData)
admin.site.register(OutputData)

admin.site.register(Agriculture, HideAdmin)
admin.site.register(Energy, HideAdmin)
admin.site.register(Water, HideAdmin)
admin.site.register(Biomes, HideAdmin)
admin.site.register(MarineEcosystems, HideAdmin)
admin.site.register(Biodiversity, HideAdmin)
admin.site.register(Health, HideAdmin)
admin.site.register(CoastalInfrastructure, HideAdmin)
admin.site.register(Permafrost, HideAdmin)

admin.site.register(ClimateDataType, HideAdmin)
admin.site.register(ClimateVariable, HideAdmin)
admin.site.register(InputPhase, HideAdmin)
admin.site.register(ReferencePaper, HideAdmin)
admin.site.register(Region, HideAdmin)
admin.site.register(Scenario, HideAdmin)
admin.site.register(SocioEconomicInputVariables, HideAdmin)
