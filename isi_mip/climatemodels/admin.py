from django.contrib import admin
from django.core import urlresolvers

from isi_mip.climatemodels.models import ClimateDataSet, ClimateVariable, ReferencePaper, SocioEconomicInputVariables
from .models import General, Sector, Water, AgroEconomicModelling

# class WaterAdmin(admin.StackedInline):
#     model = Water
#
# class GeneralAdmin(admin.ModelAdmin):
#     inlines = [WaterAdmin]

class WaterAdmin(admin.StackedInline):
    model = Water

    list_display = ('id', 'general','technological_progress')

class ReferencePaperInlineAdmin(admin.TabularInline):
    model = ReferencePaper
    extra = 1

class GeneralAdmin(admin.ModelAdmin):
    def sector(self, obj):
        try:
            adminurl = "admin:%s_change" % obj.sector._meta.db_table
            link=urlresolvers.reverse(adminurl, args=[obj.sector.id])
            return '<a href="%s">%s</a>' % (link,obj.sector)
        except:
            return
    sector.allow_tags = True

    def trenner(self, obj):
        return '<hl />'
    trenner.allow_tags = True
    trenner.short_description = 'trennerli'
    readonly_fields = ('sector','trenner')

    inlines = [WaterAdmin, ReferencePaperInlineAdmin]

    fieldsets = [
        ('Basic Information', {
            'fields':['name', 'sector', 'region', 'contact_person','version',
                      'main_reference_paper', 'short_description']}
         ),
        ('Technical Information', {
            'fields': [
                # resolution
                'resolution','temporal_resolution_climate','temporal_resolution_co2',
                'temporal_resolution_land', 'temporal_resolution_soil',
                # input data
                'climate_data_sets', 'climate_variables',
                'socioeconomic_input_variables', 'soil_dataset', 'additional_input_data_sets',
                # more
                'exceptions_to_protocol','spin_up','spin_up_design',
                'natural_vegetation_partition', 'natural_vegetation_simulation', 'natural_vegetation_cover_dataset',
                'management', 'extreme_events',
                'anything_else', 'comments'
            ],
        }),
    ]

admin.site.register(General, GeneralAdmin)
# admin.site.register(General)
admin.site.register(ClimateDataSet)
admin.site.register(ClimateVariable)
admin.site.register(SocioEconomicInputVariables)
admin.site.register(ReferencePaper)
# admin.site.register(Water)