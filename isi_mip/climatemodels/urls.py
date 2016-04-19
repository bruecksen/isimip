from django.conf.urls import url

from isi_mip.climatemodels import views

urlpatterns = [
    url(r'^assign/(?P<username>[^/]*)/$', views.Assign.as_view(), name='assign'),
    url(r'^assign/$', views.Assign.as_view(), name='assign'),
    # url(r'^edit/$', views.edit, name='climatemodels_edit'),
    # url(r'^edit/(?P<id>[0-9]*)/$', views.edit, name='climatemodels_edit'),
]
