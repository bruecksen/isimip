import requests

# DOI http://stackoverflow.com/questions/27910/finding-a-doi-in-a-document-or-page
url = 'http://api.crossref.org/works?rows={rows}&query={query}'

class Reference:
    def __init__(self, json):
        for key in json.keys():
            setattr(self, key, json[key])

    def to_bibtex(self):
        url = "http://dx.doi.org/" + self.DOI
        headers = {"accept": "application/x-bibtex"}
        r = requests.get(url, headers = headers)
        return r.text


class ReferenceException(Exception):
    pass


def query(string):
    if not string.strip().replace("-",""):
        raise ReferenceException("No search term")
    response = requests.get(url.format(rows=5, query=string))
    res = response.json()
    try:
        if res['message']['items'][0]['score'] > 1:
            return Reference(res['message']['items'][0])
    except:
        print(string)
        print(res['message'])
    raise ReferenceException('No matches')


if __name__ == '__main__':
    import sys
    query(sys.argv[0])