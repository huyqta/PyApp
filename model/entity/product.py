__author__ = 'qtahuy'


class Product(object):
    id = 0
    name = ''
    description = ''
    imageurl = ''
    price = None
    refcategory = None
    refdiscount = None
    active = 0
    disprice =None
    option = None

    def __init__(self, id, name, description, imageurl, price, refcategory, refdiscount, active, disprice, option):
        self.id = id
        self.name = name
        self.description = description
        self.imageurl = imageurl
        self.price = price
        self.refcategory = refcategory
        self.refdiscount = refdiscount
        self.active = active
        self.disprice = disprice
        self.option = option