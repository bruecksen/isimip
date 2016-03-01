from django.conf.urls import url

from isi_mip.climatemodels import views

urlpatterns = [
    # url(r'^$', views.list, name='climatemodellist'),
    url(r'^edit/$', views.edit, name='climatemodeledit'),
    url(r'^edit/(?P<id>[0-9]*)/$', views.edit, name='climatemodeledit'),
]
