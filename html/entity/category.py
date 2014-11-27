__author__ = 'qtahuy'


class Category(object):
    id = 0
    category = ''
    description = ''
    active = 0
    refparent = 0

    def __init__(self, id, category, description, active, refparent):
        self.id = id
        self.category = category
        self.description = description
        self.active = active
        self.refparent = refparent