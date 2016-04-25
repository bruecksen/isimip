# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

def loremi(count, method, random=False):
    from django.template.base import Context, Token, Parser, TOKEN_TEXT
    from django.template.defaulttags import lorem
    c = Context()
    lorem_str = "lorem %s %s" % (count, method)
    if random:
        lorem_str += " random"
    t = Token(TOKEN_TEXT, lorem_str)
    p = Parser(t)
    return lorem(p, t).render(c)


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
        self.page.save()

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

    ruhtpage = RichPage(apps,'wagtailcore.Page','wagtailcore','page')
    ruhtpage.page = Page.objects.get(id=1)



    Page.objects.get(id=2).delete()
    homepage = RichPage(apps,'pages.HomePage','pages','homepage')
    homepage.page("Homepage", "home")
    ruhtpage.add_child(homepage)
    # homepage.save()
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
    aboutpage.page('About ISIMIP', 'about')
    homepage.add_child(aboutpage)
    HeaderLink.objects.create(header=hls, target=aboutpage.page)


    # play footsie
    linklistpage = RichPage(apps, 'pages.LinkListPage', 'pages', 'linklistpage')
    linklistpage.page('Press','press')
    homepage.add_child(linklistpage)
    FooterLink.objects.create(footer=fls, target=linklistpage.page)

    # contactpage = RichPage(apps, 'pages.ContactPage', 'pages', 'contactpage')
    # contactpage.page('Contact','contact')
    # homepage.add_child(contactpage)
    FooterLink.objects.create(footer=fls, target=outcomespage.page, _name='Contact')

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


    ### BLOG
    from django.utils.text import slugify
    for wohinpage, blogtitle in [(homepage,'News'),
                      (gettingstartedpage, 'Input Data Changelog'),
                      (gettingstartedpage, 'Newsletter'),
                      (impactmodelspage, 'Impact Models Changelog' ),
                      (outputdatapage, 'Output Data Changelog')]:
        blogindexpage = RichPage(apps, 'pages.BlogIndexPage', 'pages', 'blogindexpage')
        blogindexpage.page(blogtitle, slugify(blogtitle))
        wohinpage.add_child(blogindexpage)

        for i in range(5):
            blogpage = RichPage(apps, 'pages.BlogPage', 'pages', 'blogpage')
            header = loremi(3,"w",True).title()
            blogpage.page(header, slugify(header))
            blogpage.page.body = loremi(5,'b',True)
            blogindexpage.add_child(blogpage)

    ### Changelog
    # blogindexpage2 = RichPage(apps, 'blog.BlogIndexPage', 'blog', 'blogindexpage')
    # blogindexpage2.page('Changelog', 'changelog')
    # ruhtpage.add_child(blogindexpage2)
    #
    # from django.utils.text import slugify
    #
    # for i in range(5):
    #     blogpage = RichPage(apps, 'blog.BlogPage', 'blog', 'blogpage')
    #     header = loremi(3,"w",True).title()
    #     blogpage.page(header, slugify(header))
    #     blogpage.page.body = loremi(5,'b',True)
    #     blogindexpage2.add_child(blogpage)

class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_structure),
    ]
