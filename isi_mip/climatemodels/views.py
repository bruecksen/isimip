from django.shortcuts import render

from isi_mip.climatemodels.forms import GeneralForm
from isi_mip.climatemodels.models import ImpactModel


#
# def list(request):
#     table = ClimateModelTable(General.objects.all())
#     RequestConfig(request).configure(table)
#     template = "climatemodels/list.html"
#     context = {"table": table}
#     return render(request, template, context)


def edit(request, id=None):
    if id:
        gen = ImpactModel.objects.get(id=id)
        context = {'form': GeneralForm(instance=gen)}
    else:
        context = {'form': GeneralForm()}
    template = 'climatemodels/edit.html'
    # context = {'form': GeneralForm(instance=gen)}
    return render(request, template, context)
