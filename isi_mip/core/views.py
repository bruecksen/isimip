from itertools import chain
from django.shortcuts import render

from wagtail.wagtailsearch.backends import get_search_backend
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query

from isi_mip.climatemodels.models import BaseImpactModel


def search(request, extra_context):
    # Search
    search_query = request.GET.get('query', None)
    if search_query:
        page_results = Page.objects.live().search(search_query)

        # Log the query so Wagtail can suggest promoted results
        Query.get(search_query).add_hit()

        # Also query non-wagtail models
        s = get_search_backend()
        model_results = s.search(search_query, BaseImpactModel.objects.filter(impact_model__public=True))

    else:
        page_results = []
        model_results = []

    context = {
        'search_query': search_query,
        'page_results': page_results,
        'model_results': model_results,
    }
    # raise Exception(dir(model_results[0]))

    if extra_context is not None:
        context.update(extra_context)

    # raise Exception(search_results)

    # Render template
    return render(request, 'pages/search_page.html', context)