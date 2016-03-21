# from django import template
# from django.template.loader import render_to_string
#
# from mswissenschaft.pages.models import FooterSettings, HomePage, SignLanguagePage, SimpleLanguagePage, \
#     EnglishLanguagePage
#
# register = template.Library()
#
#
# @register.simple_tag(takes_context=True)
# def footer(context, **kwargs):
#     request = context['request']
#     settings = FooterSettings.for_site(request.site)
#
#     page = context.get('page')
#     if page:
#         ancestors = page.get_ancestors().specific
#     else:
#         ancestors = []
#
#     text = settings.text
#
#     links = []
#     for link in settings.footer_links.all():
#         name = link.name
#         target = link.target.specific
#         if page and target == page:
#             active = True
#         else:
#             active = False
#         links.append({'url': target.url, 'text': name, 'active': active})
#
#     context = {
#         'page': page,
#         'links': links,
#         'partnertext': text,
#     }
#
#     home_page = HomePage.objects.first()
#     if home_page:
#         """
#         1. Get 1st level navigation elements (main_elements)
#         2. For each element add the element and its 2nd level children as a link.
#         """
#         sitemap_links = []
#         main_elements = home_page.get_children().in_menu()
#         for element in main_elements:
#             if isinstance(element.specific, (SignLanguagePage, SimpleLanguagePage, EnglishLanguagePage)):
#                 continue
#             sub_elements = element.get_children()
#             sitemap_links.append({
#                 'links': [{'text': sub_element.title, 'url': sub_element.url} for sub_element in sub_elements],
#                 'text': element.title,
#                 'url': element.url,
#             })
#         context['sitemap_links'] = sitemap_links
#
#     context.update(kwargs)
#     template = 'widgets/footer.html'
#     return render_to_string(template, context=context)
