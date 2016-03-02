from django.forms import ModelForm

from isi_mip.climatemodels.models import ImpactModel


class GeneralForm(ModelForm):
    class Meta:
        model = ImpactModel
        exclude = ('version',)
