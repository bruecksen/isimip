# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class RichPage:
    def __init__(self, apps, type, ctlabel, ctmodel):
        ContentType = apps.get_model('contenttypes.ContentType')
        self.Page = apps.get_model(type)

        self.page_content_type, created  = ContentType.objects.get_or_create(
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

    site = Site.objects.create(hostname='localhost', root_page=homepage.page, is_default_site=True)

    HeaderLinks = apps.get_model('core.HeaderLinks')
    hls = HeaderLinks.objects.create(site=site)
    HeaderLink = apps.get_model('core.HeaderLink')
    FooterLinks = apps.get_model('core.FooterLinks')
    fls = FooterLinks.objects.create(site=site)
    FooterLink = apps.get_model('core.FooterLink')

    # play headsie
    faqpage = RichPage(apps, 'pages.FAQPage', 'pages', 'faqpage')
    faqpage.page('FAQ', 'faq')
    homepage.add_child(faqpage)
    HeaderLink.objects.create(header=hls, target=faqpage.page)

    outcomespage = RichPage(apps, 'pages.OutcomesPage', 'pages', 'outcomespage')
    outcomespage.page('Outcomes', 'outcomes')
    homepage.add_child(outcomespage)
    HeaderLink.objects.create(header=hls, target=outcomespage.page)

    outputdatapage = RichPage(apps, 'pages.OutputDataPage', 'pages', 'outputdatapage')
    outputdatapage.page('Output Data', 'outputdata')
    homepage.add_child(outputdatapage)
    HeaderLink.objects.create(header=hls, target=outputdatapage.page)

    impactmodelspage = RichPage(apps, 'pages.ImpactModelsPage', 'pages', 'impactmodelspage')
    impactmodelspage.page('Impact Models', 'impactmodels')
    homepage.add_child(impactmodelspage)
    HeaderLink.objects.create(header=hls, target=impactmodelspage.page)

    gettingstartedpage = RichPage(apps, 'pages.GettingStartedPage', 'pages', 'gettingstartedpage')
    gettingstartedpage.page('Getting Started', 'gettingstarted')
    homepage.add_child(gettingstartedpage)
    HeaderLink.objects.create(header=hls, target=gettingstartedpage.page)

    aboutpage = RichPage(apps, 'pages.AboutPage', 'pages', 'aboutpage')
    aboutpage.page('About ISI-MIP', 'about')
    homepage.add_child(aboutpage)
    HeaderLink.objects.create(header=hls, target=aboutpage.page)


    # play footsie
    linklistpage = RichPage(apps, 'pages.LinkListPage', 'pages', 'linklistpage')
    linklistpage.page('Press','press')
    homepage.add_child(linklistpage)
    FooterLink.objects.create(footer=fls, target=linklistpage.page)

    contactpage = RichPage(apps, 'pages.ContactPage', 'pages', 'contactpage')
    contactpage.page('Contact','contact')
    homepage.add_child(contactpage)
    FooterLink.objects.create(footer=fls, target=contactpage.page)

    linklistpage = RichPage(apps, 'pages.LinkListPage', 'pages', 'linklistpage')
    linklistpage.page('Supporters','supporters')
    homepage.add_child(linklistpage)
    FooterLink.objects.create(footer=fls, target=linklistpage.page)

    dashboardpage = RichPage(apps, 'pages.DashboardPage', 'pages', 'dashboardpage')
    dashboardpage.page('Login/Dashboard','dashboard')
    homepage.add_child(dashboardpage)
    FooterLink.objects.create(footer=fls, target=dashboardpage.page)

    newsletterpage = RichPage(apps, 'pages.NewsletterPage', 'pages', 'newsletterpage')
    newsletterpage.page('Newsletter','newsletter')
    homepage.add_child(newsletterpage)
    FooterLink.objects.create(footer=fls, target=newsletterpage.page)

    linklistpage = RichPage(apps, 'pages.LinkListPage', 'pages', 'linklistpage')
    linklistpage.page('Links','links')
    homepage.add_child(linklistpage)
    FooterLink.objects.create(footer=fls, target=linklistpage.page)


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_structure),
    ]
