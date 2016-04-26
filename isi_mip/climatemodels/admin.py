from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.core import urlresolvers

from .models import *


class HideAdmin(admin.ModelAdmin):
    # def get_model_perms(self, request):
    #     """
    #     Return empty perms dict thus hiding the model from admin index.
    #     """
    #     return {}
    pass


class HideSectorAdmin(HideAdmin):
    # readonly_fields = ('impact_model',)
    pass


class ContactPersonAdmin(admin.TabularInline):
    model = ContactPerson
    extra = 1

# class ImpactModelFormAdmin(forms.ModelForm):
#     sektor = forms.ChoiceField(choices=ImpactModel.SECTOR_CHOICES)
#     class Meta:
#         model = ImpactModel
#         fields = '__all__'
#     def save(self, commit=True):
#         sektor = self.cleaned_data.get('sektor', None)
#         return super().save(commit=commit)

class ImpactModelAdmin(admin.ModelAdmin):
    # form = ImpactModelFormAdmin
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj=obj, **kwargs)
    #     form.base_fields['sektor'].initial = obj.fk_sector._meta.verbose_name # "Computable General Equilibrium Modelling"
    #     # print('form', form.base_fields['sektor'].initial)
    #     return form

    def sector_link(self, obj):
        try:
            adminurl = "admin:%s_change" % obj.fk_sector._meta.db_table
            link = urlresolvers.reverse(adminurl, args=[obj.fk_sector.id])
            return '<a href="%s">%s</a>' % (link, obj.fk_sector._meta.verbose_name)
        except:
            return '<span style="color:#666;">will be shown, once the model is saved.</span>'
    sector_link.allow_tags = True
    sector_link.short_description = 'Sector link'
    readonly_fields = ('sector_link',)

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
                'spatial_aggregation', 'spatial_resolution', 'temporal_resolution_climate', 'temporal_resolution_co2',
                'temporal_resolution_land', 'temporal_resolution_soil',
                # input data
                'climate_data_sets', 'climate_variables',
                'socioeconomic_input_variables', 'soil_dataset', 'additional_input_data_sets',
                # more
                'exceptions_to_protocol', 'spin_up', 'spin_up_design',
                'natural_vegetation_partition', 'natural_vegetation_dynamics', 'natural_vegetation_cover_dataset',
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
admin.site.register(WaterGlobal, HideSectorAdmin)
admin.site.register(WaterRegional, HideSectorAdmin)
admin.site.register(Biomes, HideSectorAdmin)
admin.site.register(Forests, HideSectorAdmin)
admin.site.register(MarineEcosystemsGlobal, HideSectorAdmin)
admin.site.register(MarineEcosystemsRegional, HideSectorAdmin)
admin.site.register(Biodiversity, HideSectorAdmin)
admin.site.register(Health, HideSectorAdmin)
admin.site.register(CoastalInfrastructure, HideSectorAdmin)
admin.site.register(Permafrost, HideSectorAdmin)
admin.site.register(ComputableGeneralEquilibriumModelling, HideSectorAdmin)
admin.site.register(AgroEconomicModelling, HideSectorAdmin)

admin.site.register(ClimateDataType, HideAdmin)
admin.site.register(ClimateVariable, HideAdmin)
admin.site.register(InputPhase, HideAdmin)
admin.site.register(ReferencePaper, HideAdmin)
admin.site.register(Region, HideAdmin)
admin.site.register(Scenario, HideAdmin)
admin.site.register(SocioEconomicInputVariables, HideAdmin)
admin.site.register(ContactPerson, HideAdmin)
admin.site.register(SimulationRound, HideAdmin)
admin.site.register(SpatialAggregation, HideAdmin)