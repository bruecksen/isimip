from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.core import urlresolvers

from isi_mip.climatemodels.models import BaseImpactModel


class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_model', 'get_sector', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'baseimpactmodel__sector')

    def get_model(self, obj):
        try:
            base_models = BaseImpactModel.objects.filter(owners=obj)
            adminurl = "admin:%s_change" % BaseImpactModel._meta.db_table
        except:
            return '-'
        results = []
        for bm in base_models:
            link = urlresolvers.reverse(adminurl, args=[bm.id])
            results.append('<a href="%s">%s</a>' % (link, bm.name))
        return ', '.join(results)
    get_model.admin_order_field = 'get_model'
    get_model.short_description = 'Impact Model'
    get_model.allow_tags = True

    def get_sector(self, obj):
        try:
            base_models = BaseImpactModel.objects.filter(owners=obj)
        except:
            return '-'
        return ', '.join([bm.sector.name for bm in base_models])
    get_sector.admin_order_field = 'get_sector'
    get_sector.short_description = 'Sector'
    get_sector.allow_tags = True


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
