# from django import template
# from django.template.loader import render_to_string
#
# register = template.Library()
#
#
# @register.simple_tag(takes_context=True)
# def carousel(context, carousel=None, **kwargs):
#     carousel = carousel or context.get('carousel')
#     page = context.get('page')
#
#     title = getattr(page, 'carousel_text', None)
#     text = getattr(page, 'carousel_link_text', None)
#     target = getattr(page, 'carousel_link_target', None)
#     images = getattr(page, 'carousel_images', None)
#
#     if images:
#         images = [image.value.get_rendition('fill-1800x600') for image in images]
#
#     if target:
#         url = target.url
#     else:
#         url = None
#
#     context = carousel or {
#         'images': images,
#         'title': title,
#         'button': {'text': text, 'url': url},
#     }
#     context.update(kwargs)
#     template = 'widgets/carousel.html'
#     if context['images']:
#         return render_to_string(template, context=context)
#     else:
#         return ''
