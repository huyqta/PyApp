__author__ = 'qtahuy'
from flask import Flask
from entity.category import Category
from entity.product import Product
from entity.trademark import Trademark
from entity.image import Image

app = Flask(__name__)


def parseBreadCrumbCategory(listcategory, url, obj):
    home = '<a href="/">HOME</a>'
    category = ' | <a href="category/[category]">VOT</a>'

    if url.index('category') > -1:
        for cat in listcategory:
            if cat.id == int(obj):
                category = " | <a href='category/" + str(cat.id) + "'>" + cat.category + "</a>'"
                return home + category

    return home


def parseBreadCrumbTrademark(listtrademark, listcategory, url, obj):
    home = '<a href="/">HOME</a>'
    category = '>> <a href="category/[category]">VOT</a>'
    trademark = '>> <a href="trademark/[trademark]">YON</a>'
    cat_id = -1
    # if url.index('trademark') > -1:
    for trm in listtrademark:
        if trm.id == int(obj):
            trademark = " | <a href='trademark/" + str(trm.id) + "'>" + trm.name + "</a>'"
            cat_id = trm.refcategory

    for cat in listcategory:
        if cat.id == cat_id:
            category = " | <a href='category/" + str(cat.id) + "'>" + cat.category + "</a>'"

    return home + category + trademark


# def parseBreadCrumb(listtrademark=None, listcategory=None, url=None, obj=object):
# home = '<a href="/">HOME</a>'
# category = '>> <a href="category/[category]">VOT</a>'
#     trademark = '>> <a href="trademark/[trademark]">YON</a>'
#     product = '>> <a href="/1/7">ABC</a>'
#     if url.index('category') > -1:
#         category = ">> <a href='category/" + obj[0] + "'>[category]</a>'"
#         return home + category
#     if url.index('trademark') > -1:
#         for cat in listcategory:
#             if cat.id == obj[5]:
#                 category = ">> <a href='category/" + obj[5] + "'>" + cat.category + "</a>'"
#
#             trademark = ">> <a href='trademark/" + obj[0] + "'>" + obj[1] + "</a>'"
#             return home + category + trademark
#
#     if url.index('product') > -1:
#         for cat in listcategory:
#             if cat.id == obj.refcategory:
#                 category = ">> <a href='category/" + obj[5] + "'>" + cat.category + "</a>'"
#         for trm in listtrademark:
#             if trm.id == obj.reftrademark:
#                 trademark = ">> <a href='trademark/" + obj[11] + "'>" + obj[1] + "</a>'"
#
#         product = ">> <a href='/product/" + obj[0] + "'>" + obj[1] + "</a>"
#         return home + category + trademark + product
