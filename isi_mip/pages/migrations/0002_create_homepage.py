# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class RichPage:
    def __init__(self, apps, type, ctlabel, ctmodel):
        ContentType = apps.get_model('contenttypes.ContentType')
        self.Page = apps.get_model(type)

        self.page_content_type, created = ContentType.objects.get_or_create(
            model=ctmodel, app_label=ctlabel)
        self.parent = None

    def page(self, title, slug):
        self.page = self.Page(
            title=title,
            slug=slug,
            content_type=self.page_content_type,
            numchild=0,
        )

    def save(self):
        if not self.parent:
            self.page.path = '00010001'
            self.page.depth = 2
            self.page.url_path='/%s/' % self.page.slug
        self.page.save()

    # @staticmethod
    def add_child(self, child):
        child.page.path = self.page.path + '%04d' % (self.page.numchild + 1)
        child.page.url_path = self.page.url_path + '%s/' % child.page.slug
        child.page.depth = self.page.depth + 1
        self.page.numchild += 1

        child.parent = self
        child.page.save()
        self.page.save()


def  create_structure(apps, schema_editor):
    Page = apps.get_model('wagtailcore.Page')
    Site = apps.get_model('wagtailcore.Site')
    Page.objects.get(id=2).delete()
    homepage = RichPage(apps,'pages.HomePage','pages','homepage')
    homepage.page("Homepage", "home")
    homepage.save()

    site = Site.objects.create(
        hostname='localhost', root_page=homepage.page, is_default_site=True)

    HeaderLinks = apps.get_model('core.HeaderLinks')
    hls = HeaderLinks.objects.create(site=site)
    HeaderLink = apps.get_model('core.HeaderLink')
    FooterLinks = apps.get_model('core.FooterLinks')
    fls = FooterLinks.objects.create(site=site)
    FooterLink = apps.get_model('core.FooterLink')

    faqpage = RichPage(apps, 'pages.FAQPage', 'pages', 'faqpage')
    faqpage.page('FAQ', 'faq')
    homepage.add_child(faqpage)
    HeaderLink.objects.create(name='FAQ', header=hls, target=faqpage.page)

    outcomespage = RichPage(apps, 'pages.OutcomesPage', 'pages', 'outcomespage')
    outcomespage.page('Outcomes', 'outcomes')
    homepage.add_child(outcomespage)
    HeaderLink.objects.create(name='Outcomes', header=hls, target=outcomespage.page)

    impactmodelspage = RichPage(apps, 'pages.ImpactModelsPage', 'pages', 'impactmodelspage')
    impactmodelspage.page('Impact Models', 'impactmodels')
    homepage.add_child(impactmodelspage)
    HeaderLink.objects.create(name='Impact Models', header=hls, target=impactmodelspage.page)


    linklistpage = RichPage(apps, 'pages.LinkListPage', 'pages', 'linklistpage')
    linklistpage.page('Press','press')
    homepage.add_child(linklistpage)
    FooterLink.objects.create(name='Press', footer=fls, target=linklistpage.page)

    linklistpage = RichPage(apps, 'pages.LinkListPage', 'pages', 'linklistpage')
    linklistpage.page('Supporters','supporters')
    homepage.add_child(linklistpage)
    FooterLink.objects.create(name='Supporters', footer=fls, target=linklistpage.page)

    linklistpage = RichPage(apps, 'pages.LinkListPage', 'pages', 'linklistpage')
    linklistpage.page('Links','links')
    homepage.add_child(linklistpage)
    FooterLink.objects.create(name='Links', footer=fls, target=linklistpage.page)


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_structure),
    ]
