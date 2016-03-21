from django import template

register = template.Library()


# Messages
@register.inclusion_tag('widgets/messages.html', takes_context=True)
def messages(context):
    django_messages = context['messages']
    messages = []
    for message in django_messages:
        messages.append({'tags': message.tags, 'text': message})
    return {
        'messages': messages,
    }
