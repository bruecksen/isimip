from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView

from isi_mip.climatemodels.forms import ImpactModelForm, ImpactModelStartForm
from isi_mip.climatemodels.models import ImpactModel


class Assign(SuccessMessageMixin, UpdateView):
    template_name = 'climatemodels/assign.html'
    form_class = ImpactModelStartForm
    model = ImpactModel
    success_message = 'The model has been successfully created and assigned'

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET['next']
        return reverse('admin:auth_user_list')

    def get_object(self, queryset=None):
        if 'username' in self.kwargs:
            user = User.objects.get(username=self.kwargs['username'])
            return ImpactModel(owner=user)
        return None

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
