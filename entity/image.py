__author__ = 'qtahuy'


class Image(object):
    imageurl = ''
    refproduct = -1
    isdefault = 0

    def __init__(self, imageurl, refproduct, isdefault):
        self.imageurl = imageurl
        self.refproduct = refproduct
        self.isdefault = isdefault