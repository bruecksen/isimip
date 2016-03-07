from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView

from isi_mip.climatemodels.forms import ImpactModelForm, ImpactModelStartForm
from isi_mip.climatemodels.models import ImpactModel


class Assign(UpdateView):
    template = 'climatemodels/assign.html'
    form_class = ImpactModelStartForm
    model = ImpactModel
    # success_url = '/admin/'
    # error_url = '/django-admin/'

    def get_object(self, queryset=None):
        return get_object_or_404()

    # data = {'owner': username}
    # form = (initial=data)
    # context = {'form':form}
    # return render(request, template, context)


def edit(request, id=None):
    if id:
        gen = ImpactModel.objects.get(id=id)
        context = {'form': ImpactModelForm(instance=gen)}
    else:
        context = {'form': ImpactModelForm()}
    template = 'climatemodels/edit.html'
    return render(request, template, context)
