from django.conf.urls import url

from isi_mip.climatemodels import views

urlpatterns = [
    url(r'^assign/(?P<username>[^/]*)/$', views.impact_model_assign, name='assign'),
    url(r'^assign/$', views.impact_model_assign, name='assign'),
]
