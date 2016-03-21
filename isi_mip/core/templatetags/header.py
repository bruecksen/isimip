# from django import template
# from django.template.loader import render_to_string
# from django.utils import timezone
#
# from isi_mip.pages.models import HomePage, SignLanguagePage, SimpleLanguagePage, EnglishLanguagePage
#
# register = template.Library()
#
#
# @register.simple_tag(takes_context=True)
# def header(context, header=None, **kwargs):
#     header = header or context.get('header')
#
#     current_page = context.get('page')
#     home_page = HomePage.objects.live().in_menu().first()
#     main_pages = home_page.get_children().live().in_menu().specific()
#     if current_page:
#         ancestors = current_page.get_ancestors().live().in_menu().specific()
#     else:
#         ancestors = []
#
#     links = []
#     links_secondary = []
#     for page in main_pages:
#         url = page.url
#
#         # Checking if this main page page is an ancestor of the current page
#         if page.specific == current_page or page.specific in ancestors:
#             active = True
#         else:
#             active = False
#
#         if isinstance(page, (SignLanguagePage, SimpleLanguagePage, EnglishLanguagePage)):
#             links_secondary.append({
#                 'text': page.title if isinstance(page, EnglishLanguagePage) else '',
#                 'url': url,
#                 'active': active,
#                 'sign_language_icon': isinstance(page, SignLanguagePage),
#                 'simple_language_icon': isinstance(page, SimpleLanguagePage),
#             })
#         else:
#             subpages = page.get_children().live().in_menu()
#             if active:
#                 sublinks = [{'text': page.title, 'url': page.url, 'active': page.specific == current_page or page.specific in ancestors} for page in subpages]
#             else:
#                 sublinks = []
#             text = page.title
#             links.append({
#                 'text': text,
#                 'url': url,
#                 'active': active,
#                 'sublinks': sublinks,
#             })
#
#     context = header or {
#         'id': timezone.now().microsecond,
#         'links': links,
#         'links_secondary': links_secondary,
#     }
#     context.update(kwargs)
#     template = 'widgets/header.html'
#     return render_to_string(template, context=context)
