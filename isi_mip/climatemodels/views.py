from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_tables2 import RequestConfig

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query

from isi_mip.climatemodels.forms import GeneralForm
from isi_mip.climatemodels.models import General
from isi_mip.climatemodels.tables import ClimateModelTable


def list(request):
    table = ClimateModelTable(General.objects.all())
    RequestConfig(request).configure(table)
    template = "climatemodels/list.html"
    context = {"table": table}
    return render(request, template, context)


def edit(request, id=None):
    if id:
        gen = General.objects.get(id=id)
        context = {'form': GeneralForm(instance=gen)}
    else:
        context = {'form': GeneralForm()}
    template = 'climatemodels/edit.html'
    # context = {'form': GeneralForm(instance=gen)}
    return render(request, template, context)
