from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel, StreamFieldPanel
from wagtail.core.models import Orderable
from wagtail.core import blocks
from wagtail.core.fields import StreamField


@register_setting(icon='list-ul')
class HeaderLinks(ClusterableModel, BaseSetting):
    panels = [
        InlinePanel('header_links', label="Link"),
    ]


class BaseLinkBlock(blocks.StructBlock):
    """
    Base StructBlock class used to prevent DRY code.
    """
    name = blocks.CharBlock()


class JumpLinkBlock(BaseLinkBlock):
    """
    Block that holds a link to any URL.
    """
    link = blocks.CharBlock()

    class Meta:
        icon = 'fa fa-link'


class PageLinkBlock(BaseLinkBlock):
    """
    Block that holds a page.
    """
    page = blocks.PageChooserBlock()

    class Meta:
        icon = 'fa fa-file-o'


class HeaderLink(Orderable, models.Model):
    header = ParentalKey(HeaderLinks, related_name='header_links')
    target = models.ForeignKey('wagtailcore.Page')
    _name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Alt. name',
                             help_text='If left empty, the target\'s title will be used.')
    name = property(lambda self: self._name or self.target.title)
    menu_items = StreamField([
        ('jump_link', JumpLinkBlock()),
        ('page_link', PageLinkBlock()),
    ], null=True, blank=True)

    panels = [
        PageChooserPanel('target'),
        FieldPanel('_name'),
        StreamFieldPanel('menu_items'),
    ]


@register_setting(icon='list-ul')
class FooterLinks(ClusterableModel, BaseSetting):
    panels = [
        InlinePanel('footer_links', label="Link"),
    ]


class FooterLink(Orderable, models.Model):
    footer = ParentalKey(FooterLinks, related_name='footer_links')
    target = models.ForeignKey('wagtailcore.Page')
    anchor = models.CharField(max_length=500, null=True, blank=True, help_text='A specific anchor to scroll to.')
    _name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Alt. name',
                             help_text='If left empty, the target\'s title will be used.')
    name = property(lambda self: self._name or self.target.title)

    panels = [
        PageChooserPanel('target'),
        FieldPanel('anchor'),
        FieldPanel('_name'),

    ]


@register_setting(icon='mail')
class Invitation(BaseSetting):
    subject = models.CharField(max_length=500, help_text='Invitation subject', default='[ISIMIP] Registration invitation for impact-model database')
    body = models.TextField()


@register_setting(icon='mail')
class DataPublicationRequest(BaseSetting):
    subject = models.CharField(max_length=500, help_text='Data publication request subject', default="[ISIMIP] Data confirmation request")
    body = models.TextField(help_text='You can use the following tokens in the email template: {{model_contact_person}}, {{simulation_round}}, {{sector}}, {{impact_model_name}}, {{data_confirmation_link}}, {{custom_text}}')


@register_setting(icon='mail')
class DataPublicationConfirmation(BaseSetting):
    subject = models.CharField(max_length=500, help_text='Data publication confirmation subject', default="[ISIMIP] Data confirmation")
    body = models.TextField(help_text='You can use the following tokens in the email template: {{model_contact_person}}, {{simulation_round}}, {{impact_model_name}}, {{custom_text}}, {{license}}')
