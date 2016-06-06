from datetime import date

import requests

from django.db import models

CROSSREF_URL = 'http://api.crossref.org/works?rows={rows}&query={query}'


class Author(models.Model):
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    email = models.EmailField()
    homepage = models.URLField()

    def __str__(self):
        ret = "%s %s" % (self.first_name, self.last_name)
        if self.email:
            ret += " (%s)" % self.email
        return ret


class Paper(models.Model):
    title = models.CharField(max_length=1000)
    doi = models.CharField(max_length=500, null=True, blank=True)

    lead_author = models.CharField(max_length=500, blank=True, null=True)
    authors = models.ManyToManyField(Author, blank=True)
    journal_name = models.CharField(max_length=500, null=True, blank=True)
    journal_volume = models.IntegerField(null=True, blank=True)
    journal_number = models.IntegerField(null=True, blank=True)
    journal_pages = models.CharField(max_length=500, null=True, blank=True)
    first_published = models.DateField(null=True, blank=True)
    # published_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "%s (%s)" % (self.title, self.doi) if self.doi else self.title

    def to_bibtex(self):
        url = "http://dx.doi.org/" + self.doi
        headers = {"accept": "application/x-bibtex"}
        r = requests.get(url, headers=headers)
        return r.text

    @staticmethod
    def create_from_query(query):
        if not query.strip():
            raise Exception("No search term")
        response = requests.get(CROSSREF_URL.format(rows=5, query=query))
        res = response.json()
        if res['message']['items'][0]['score'] > 1:
            paper_dict = res['message']['items'][0]
            paper, created = Paper.objects.get_or_create(doi=paper_dict['DOI'])
            paper.title = paper_dict['title'][0]
            paper.journal_name = paper_dict['container-title'][0]
            # print(paper_dict['container-title'])
            # print(paper_dict['title'])
            paper.journal_volume = paper_dict['volume']
            # paper.journal_number = 0
            paper.journal_pages = paper_dict['page']

            y,m,d = paper_dict['published-online']['date-parts'][0]
            paper.first_published = date(y,m,d)

            for author in paper_dict['author']:
                au, created = Author.objects.get_or_create(first_name=author['given'], last_name=author['family'])
                paper.authors.add(au)
            paper.save()
            return

        raise Exception('No matches')