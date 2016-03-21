from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import defaults as default_views
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailsearch import urls as wagtailsearch_urls

from isi_mip.climatemodels import urls as climatemodels_urls
from isi_mip.invitation import urls as invitations_urls


def superuser_required(view):
    def f(request, *args, **kwargs):
        if request.user.is_superuser:
            return view(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('admin:login')+'?next='+request.META['PATH_INFO'])
    return f


urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name="home"),
    # url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name="about"),
    # url(r'^search/', include(wagtailsearch_urls)),
    # url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^styleguide/', include("isi_mip.styleguide.urls", namespace="styleguide")),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^cms/', include(wagtailadmin_urls)),

    url(r'^models/', include(climatemodels_urls, namespace='climatemodels')),
    url(r'^accounts/', include(invitations_urls), name='account'),

    url(r'^blog/', include('blog.urls', namespace="blog")),

    # url(r'^accounts/invite/$', superuser_required(InvitationView.as_view()), name='account_invite'),
    # url(r'^accounts/register/(?P<pk>\d+)/(?P<token>[0-9a-f]{40})/$', RegistrationView.as_view(), name='account_register'),
    # url(r'^accounts/', include('allauth.urls')),

    url(r'', include(wagtail_urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception("Bad Request!")}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception("Permission Denied")}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception("Page not Found")}),
        url(r'^500/$', default_views.server_error),
    ]
