__author__ = 'qtahuy'


class Trademark(object):
    id = 0
    name = ''
    description = ''
    urllogo = ''
    active = 0
    refcategory = None

    def __init__(self, id, name, description, urllogo, active, refcategory):
        self.id = id
        self.name = name
        self.description = description
        self.urllogo = urllogo
        self.active = active
        self.refcategory = refcategory