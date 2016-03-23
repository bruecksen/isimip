from django.forms import ModelForm

from isi_mip.climatemodels.models import ImpactModel


class ImpactModelStartForm(ModelForm):
    class Meta:
        model = ImpactModel
        fields = ('name', 'sector', 'owner')


class ImpactModelForm(ModelForm):
    class Meta:
        model = ImpactModel
        exclude = ('version',)
