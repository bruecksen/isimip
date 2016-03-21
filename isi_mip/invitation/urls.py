from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from isi_mip.invitation.views import InvitationView, RegistrationView


def superuser_required(view):
    def f(request, *args, **kwargs):
        if request.user.is_superuser:
            return view(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('admin:login') + '?next=' + request.META['PATH_INFO'])

    return f


urlpatterns = [
    url(r'^invite/$', superuser_required(InvitationView.as_view()), name='invite'),
    url(r'^register/(?P<pk>\d+)/(?P<token>[0-9a-f]{40})/$', RegistrationView.as_view(), name='register'),
]
