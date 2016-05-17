from datetime import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core import urlresolvers
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Q
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.html import urlize
from django.views.generic import UpdateView
from wagtail.wagtailcore.models import Page

from isi_mip.climatemodels.forms import ImpactModelForm, ImpactModelStartForm, ContactPersonFormset, get_sector_form
from isi_mip.climatemodels.models import ImpactModel, InputData
from isi_mip.climatemodels.tools import ImpactModelToXLSX


def impact_model_assign(request, username=None):
    user = User.objects.get(username=username)
    impactmodel = ImpactModel(owner=user)

    if request.method == 'POST':
        form = ImpactModelStartForm(request.POST, instance=impactmodel)
        if form.is_valid():
            imodel = form.cleaned_data['model']
            if imodel:
                imodel.owner = form.cleaned_data['owner']
                imodel.save()
                messages.success(request, "The new owner has been assigned successfully")
            else:
                del (form.cleaned_data['model'])
                ImpactModel.objects.create(**form.cleaned_data)
                messages.success(request, "The model has been successfully created and assigned")
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('admin:auth_user_list'))
        else:
            messages.warning(request, form.errors)
    else:
        form = ImpactModelStartForm(instance=impactmodel)
    template = 'climatemodels/assign.html'
    return render(request, template, {'form': form})


def impact_model_details(page, request, id):
    im = ImpactModel.objects.get(id=id)
    im_values = im.values_to_tuples() + im.fk_sector.values_to_tuples()
    model_details = []
    for k, v in im_values:
        if any((y for x, y in v)):
            res = {'term': k,
                   'definitions': ({'text': "<i>%s</i>: %s" % (x, y)} for x, y in v if y)
                   }
            model_details.append(res)
    model_details[0]['opened'] = True

    description = urlize(im.short_description)  # or ''
    context = {
        'page': page,
        'subpage': Page(title='Impact Model: %s' % im.name),
        'description': description or '',
        'headline': im.name,
        'list': model_details,
    }
    if request.user == im.owner:
        context['editlink'] = '<a href="{}">edit</a>'.format(
            page.url + page.reverse_subpage('edit', args=(im.id,)))
    else:
        context['editlink'] = ''
    if request.user.is_superuser:
        context['editlink'] += ' | <a href="{}">admin edit</a>'.format(
            urlresolvers.reverse('admin:climatemodels_impactmodel_change', args=(im.id,)))

    template = 'climatemodels/details.html'
    return render(request, template, context)


def impact_model_download(page, request):
    imodels = ImpactModel.objects.all()
    if 'sector' in request.GET:
        imodels = imodels.filter(sector=request.GET['sector'])
    if 'driver' in request.GET:
        imodels = imodels.filter(climate_data_sets__name=request.GET['driver'])
    if 'q' in request.GET:
        q = request.GET['q']
        query = Q(name__icontains=q) | Q(sector__icontains=q) | Q(climate_data_sets__name__icontains=q) \
                | Q(contactperson__name__icontains=q) | Q(contactperson__email__icontains=q)
        imodels = imodels.filter(query)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="ImpactModels {:%Y-%m-%d}.xlsx"'.format(datetime.now())
    ImpactModelToXLSX(response, imodels)
    return response


def impact_model_edit(page, request, id):
    impactmodel = ImpactModel.objects.get(id=id)
    context = {'page': page, 'subpage': Page(title='Impact Model: %s' % impactmodel.name)}

    if request.method == 'POST':
        form = ImpactModelForm(request.POST, instance=impactmodel)
        contactform = ContactPersonFormset(request.POST, instance=impactmodel)
        if form.is_valid() and contactform.is_valid():
            form.save()
            contactform.save()
            messages.success(request, "Changes to your model have been saved successfully.")
            target_url = page.url + page.reverse_subpage('edit_sector', args=(impactmodel.id,))
            return HttpResponseRedirect(target_url)
        else:
            messages.error(request, 'Your form has errors.')
            messages.warning(request, form.errors)
            messages.warning(request, contactform.errors)
    else:
        form = ImpactModelForm(instance=impactmodel)
        contactform = ContactPersonFormset(instance=impactmodel)
    context['form'] = form
    context['cform'] = contactform
    template = 'climatemodels/edit_impact_model.html'
    return render(request, template, context)


def impact_model_sector_edit(page, request, id):
    impactmodel = ImpactModel.objects.get(id=id)
    context = {'page': page, 'subpage': Page(title='Impact Model: %s' % impactmodel.name)}
    formular = get_sector_form(impactmodel.fk_sector_name)

    # No further changes, because the Sector has none.
    target_url = page.url + page.reverse_subpage('details', args=(impactmodel.id,))
    if formular is None:
        return HttpResponseRedirect(target_url)

    if request.method == 'POST':
        form = formular(request.POST, instance=impactmodel.fk_sector)
        if form.is_valid():
            form.save()
            messages.success(request, "Changes to your model have been saved successfully.")
            HttpResponseRedirect(target_url)
        else:
            messages.warning(request, form.errors)
    else:
        form = formular(instance=impactmodel.fk_sector)
    context['form'] = form
    template = 'climatemodels/{}'.format(formular.template)
    return render(request, template, context)


def input_data_details(page, request, id):
    data = InputData.objects.get(id=id)
    template = 'pages/input_data_details_page.html'
    description = page.input_data_description or ''
    if request.user.is_superuser:
        description += ' <a href="{}">admin edit</a>'.format(
            urlresolvers.reverse('admin:climatemodels_inputdata_change', args=(data.id,)))

    context = {'page': page,
               'subpage': Page(title='Input Data Set: %s' % data),
               'description': description or '',
               'list': [
                   {
                       'notoggle': True,
                       'opened': True,
                       # 'term': data.name, # TODO: Tom schau mal hier.
                       'definitions': [
                           {'text': 'Data Type: %s' % data.data_type},
                           {'text': 'Scenario: %s' % data.scenario},
                           {'text': 'Phase: %s' % data.phase},
                           {'text': 'Variables: %s' % ', '.join((x.as_span() for x in data.variables.all()))},
                       ]
                   },
                   {'notoggle': True, 'opened': True, 'term': 'Description',
                    'definitions': [{'text': data.description}]},
                   {'notoggle': True, 'opened': True, 'term': 'Caveats', 'definitions': [{'text': data.caveats}]},
                   {'notoggle': True, 'opened': True, 'term': 'Download Instructions',
                    'definitions': [{'text': data.download_instructions}]},
               ]
               }
    return render(request, template, context)
