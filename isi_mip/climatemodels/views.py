from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_tables2 import RequestConfig

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query

from isi_mip.climatemodels.models import General
from isi_mip.climatemodels.tables import ClimateModelTable


def list(request):
    table = ClimateModelTable(General.objects.all())
    RequestConfig(request).configure(table)
    return render(request, "climatemodels/list.html", {"table": table})