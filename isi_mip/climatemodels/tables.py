import django_tables2 as tables
from .models import *


class ClimateModelTable(tables.Table):
    class Meta:
        model = General
        fields = ('name', 'sector', 'contact_person')
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
