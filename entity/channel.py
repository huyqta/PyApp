__author__ = 'qtahuy'


class Channel(object):
    id = 0
    name = ''
    urlcrawl = ''
    urlapi = ''
    urllogo = ''
    refgroup = 0

    def __init__(self, id, name, urlcrawl, urlapi, urllogo, refgroup):
        self.id = id
        self.name = name
        self.urlcrawl = urlcrawl
        self.urlapi = urlapi
        self.urllogo = urllogo
        self.refgroup = refgroup