from datetime import datetime

import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils.html import urlize, linebreaks
from wagtail.wagtailcore.models import Page

from isi_mip.climatemodels.forms import ImpactModelForm, ImpactModelStartForm, ContactPersonFormset, get_sector_form
from isi_mip.climatemodels.models import ImpactModel, InputData, ReferencePaper
from isi_mip.climatemodels.tools import ImpactModelToXLSX


def impact_model_details(page, request, id):
    impactmodel = ImpactModel.objects.get(id=id)
    subpage = {'title': 'Impact Model: %s' % impactmodel.name, 'url': ''}
    context = {'page': page, 'subpage': subpage, 'headline': impactmodel.name}

    im_values = impactmodel.values_to_tuples() + impactmodel.fk_sector.values_to_tuples()
    model_details = []
    for k, v in im_values:
        if any((y for x, y in v)):
            res = {'term': k,
                   'definitions': ({'text': "%s: <i>%s</i>" % (x, y)} for x, y in v if y)
                   }
            model_details.append(res)
    model_details[0]['opened'] = True
    context['list'] = model_details
    context['description'] = urlize(impactmodel.short_description or '')  # or ''

    if request.user == impactmodel.owner:
        context['editlink'] = '<a href="{}">edit</a>'.format(
            page.url + page.reverse_subpage('edit', args=(impactmodel.id,)))
    else:
        context['editlink'] = ''
    if request.user.is_superuser:
        context['editlink'] += ' | <a href="{}">admin edit</a>'.format(
            urlresolvers.reverse('admin:climatemodels_impactmodel_change', args=(impactmodel.id,)))

    template = 'climatemodels/details.html'
    return render(request, template, context)


def impact_model_download(page, request):
    imodels = ImpactModel.objects.order_by('name')
    if 'sector' in request.GET:
        imodels = imodels.filter(sector=request.GET['sector'])
    if 'driver' in request.GET:
        imodels = imodels.filter(climate_data_sets__name=request.GET['driver'])
    if 'searchvalue' in request.GET:
        q = request.GET['searchvalue']
        query = Q(name__icontains=q) | Q(sector__icontains=q) | Q(climate_data_sets__name__icontains=q) \
                | Q(contactperson__name__icontains=q) | Q(contactperson__email__icontains=q)
        imodels = imodels.filter(query)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="ImpactModels {:%Y-%m-%d}.xlsx"'.format(datetime.now())
    ImpactModelToXLSX(response, imodels)
    return response


def input_data_details(page, request, id):
    data = InputData.objects.get(id=id)
    template = 'pages/input_data_details_page.html'
    description = page.input_data_description or ''
    if request.user.is_superuser:
        description += ' <a href="{}">admin edit</a>'.format(
            urlresolvers.reverse('admin:climatemodels_inputdata_change', args=(data.id,)))

    subpage = {'title': 'Impact Model: %s' % data.name, 'url': ''}
    context = {'page': page,
               'subpage': subpage,
               'description': description,
               'list': [
                   {
                       'notoggle': True,
                       'opened': True,
                       'definitions': [
                           {'text': 'Data Type: %s' % data.data_type},
                           {'text': 'Scenario: %s' % data.scenario},
                           {'text': 'Phase: %s' % data.phase},
                           {'text': 'Variables: %s' % ', '.join((x.as_span() for x in data.variables.all()))},
                       ]
                   },
                   {'notoggle': True, 'opened': True, 'term': 'Description',
                    'definitions': [{'text': urlize(linebreaks(data.description))}]},
                   {'notoggle': True, 'opened': True, 'term': 'Caveats', 'definitions': [{'text': urlize(linebreaks(data.caveats))}]},
                   {'notoggle': True, 'opened': True, 'term': 'Download Instructions',
                    'definitions': [{'text': urlize(linebreaks(data.download_instructions))}]},
               ]
               }
    return render(request, template, context)


def crossref_proxy(request):
    url = 'http://api.crossref.org/works?rows={rows}&query={query}'
    response = requests.get(url.format(rows=5, query=request.GET['query']))
    res = response.json()
    return JsonResponse(res)


# authentication required.. #########################################################
def impact_model_edit(page, request, id):
    if not request.user.is_authenticated():
        messages.info(request, 'You need to be logged in to perform this action.')
        nexturl = reverse('wagtailadmin_login') + "?next={}".format(request.path)
        return HttpResponseRedirect(nexturl)
    impactmodel = ImpactModel.objects.get(id=id)
    if not (request.user == impactmodel.owner or request.user.is_superuser):
        messages.info(request, 'You need to be logged in to perform this action.')
        nexturl = reverse('wagtailadmin_login') + "?next={}".format(request.path)
        return HttpResponseRedirect(nexturl)

    subpage = {
        'title': 'Impact Model: %s' % impactmodel.name,
        'url': page.url + page.reverse_subpage('details', args=(id,)),
        'subpage': {'title': 'Edit', 'url': ''}
    }
    context = {'page': page, 'subpage': subpage}

    if request.method == 'POST':
        form = ImpactModelForm(request.POST, instance=impactmodel)
        contactform = ContactPersonFormset(request.POST, instance=impactmodel)
        if form.is_valid() and contactform.is_valid():
            form.save()
            contactform.save()
            if 'continue' in request.POST:
                messages.info(request, "All changes to the base model have been saved. Here you can change sector specific details.")
                target_url = page.url + page.reverse_subpage('edit_sector', args=(impactmodel.id,))
            else:
                messages.success(request, "Changes to your model have been saved successfully.")
                target_url = page.url + page.reverse_subpage('details', args=(impactmodel.id,))
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
    if not request.user.is_authenticated():
        messages.info(request, 'You need to be logged in to perform this action.')
        nexturl = reverse('wagtailadmin_login') + "?next={}".format(request.path)
        return HttpResponseRedirect(nexturl)
    impactmodel = ImpactModel.objects.get(id=id)
    if not (request.user == impactmodel.owner or request.user.is_superuser):
        messages.info(request, 'You need to be logged in to perform this action.')
        nexturl = reverse('wagtailadmin_login') + "?next={}".format(request.path)
        return HttpResponseRedirect(nexturl)

    subpage = {
        'title': 'Impact Model: %s' % impactmodel.name,
        'url': page.url + page.reverse_subpage('details', args=(id,)),
        'subpage': {'title': 'Edit Sector','url': ''}
    }
    context = {'page': page, 'subpage': subpage}
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
            return HttpResponseRedirect(target_url)
        else:
            messages.warning(request, form.errors)
    else:
        form = formular(instance=impactmodel.fk_sector)
    context['form'] = form
    template = 'climatemodels/{}'.format(formular.template)
    return render(request, template, context)


def impact_model_assign(request, username=None):
    if not request.user.is_superuser:
        messages.info(request, 'You need to be logged in to perform this action.')
        nexturl = reverse('wagtailadmin_login') + "?next={}".format(request.path)
        return HttpResponseRedirect(nexturl)
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