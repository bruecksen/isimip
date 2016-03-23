from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.wagtailcore.models import Page, Orderable

from isi_mip.climatemodels.models import ImpactModel


@register_setting
class HeaderLinks(ClusterableModel, BaseSetting):
    panels = [
        InlinePanel('header_links', label="Link"),
    ]


class HeaderLink(Orderable, models.Model):
    header = ParentalKey(HeaderLinks, related_name='header_links')
    target = models.ForeignKey('wagtailcore.Page')
    _name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Alt. name',
                             help_text='If left empty, the target\'s title will be used.')
    name = property(lambda self: self._name or self.target.title)

    panels = [
        PageChooserPanel('target'),
        FieldPanel('_name'),
    ]


@register_setting
class FooterLinks(ClusterableModel, BaseSetting):
    panels = [
        InlinePanel('footer_links', label="Link"),
    ]


class FooterLink(Orderable, models.Model):
    footer = ParentalKey(FooterLinks, related_name='footer_links')
    target = models.ForeignKey('wagtailcore.Page')
    _name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Alt. name',
                             help_text='If left empty, the target\'s title will be used.')
    name = property(lambda self: self._name or self.target.title)

    panels = [
        PageChooserPanel('target'),
        FieldPanel('_name'),
    ]
