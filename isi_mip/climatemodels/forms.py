from django.forms import ModelForm

from isi_mip.climatemodels.models import General


class GeneralForm(ModelForm):
    class Meta:
        model = General
        exclude = ('version',)
