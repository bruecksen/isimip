from django.conf.urls import url

from isi_mip.climatemodels.views import impact_model_assign, impact_model_assign, crossref_proxy

urlpatterns = [
    url(r'^assign/(?P<username>[^/]*)/$', impact_model_assign, name='assign'),
    url(r'^assign/$', impact_model_assign, name='assign'),
    url(r'^crossref/$', crossref_proxy, name='crossref'),
]