from django.forms import RadioSelect


class SelectOrOther(RadioSelect):

    class Media:
        js = ('js/choiceorotherfield.js',)
        css = {
            'all': ('css/choiceorotherfield.css',)
        }
