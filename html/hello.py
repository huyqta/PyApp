from flask import Flask, render_template, url_for, request, redirect, session

from jinja2 import Environment
from flask.ext.cors import CORS

import pymysql
from entity.category import Category
from entity.product import Product
from model.main_model import MainModel

app = Flask(__name__)

# conn = pymysql.connect(host='localhost', user='root', passwd='', port=3306, db='dbtracking', charset='utf8', autocommit=True)
# cur = conn.cursor()
CORS(app, resources=r'/admin/*', headers='Content-Type')


@app.route('/')
def index():
    product = load_all_product()
    category = load_all_category()
    return render_template('public/index.html', product=product, category=category)


@app.route('/public/gmap')
def gmap():
    return render_template('public/gmap.html')


# @app.route('/public/product')
# def product():
# product = load_all_product()
#     category = load_all_category()
#     return render_template('public/product.html', product=product, category=category)


@app.route('/admin')
def login():
    # if session['username'] == 'admin':
    # return redirect(url_for('main_admin'))
    # else:
    # return render_template('admin/index.html', loginfail="")
    return render_template('admin/index.html', loginfail="")


@app.route('/logout')
def logout():
    # session.clear()
    return redirect(url_for('login'))


@app.route('/admin/login', methods=['POST'])
def admin_login():
    username = request.form['username']
    password = request.form['password']
    main = MainModel
    result = main.SelectDB('account')
    number_of_rows = result[0]

    if number_of_rows == 0:
        return redirect(url_for('login'))
    else:
        session['username'] = request.form['username']
        return redirect(url_for('main_admin'))


@app.route('/admin/main')
def main_admin():
    cat_result = load_all_category()
    prd_result = load_all_product()
    return render_template('/admin/main.html', category=cat_result, product=prd_result)


@app.route('/admin/category')
def admin_category():
    cat_result = load_all_category()
    return render_template('/admin/category.html', category=cat_result)


@app.route('/admin/product')
def admin_product():
    pro_result = load_all_product()
    cat_result = load_all_category()
    return render_template('/admin/product.html', product=pro_result, category=cat_result)


def load_all_category():
    listCategory = []
    main = MainModel
    cat_result = main.SelectDB('category')
    for cat in cat_result:
        listCategory.append(Category(cat[0], cat[1], cat[2], cat[3], cat[4]))

    return listCategory


def load_all_product():
    listProduct = []
    main = MainModel
    pro_result = main.SelectDB('product')
    for prd in pro_result:
        listProduct.append(Product(prd[0], prd[1], prd[2], prd[3], prd[4], prd[5], prd[6], prd[7], prd[8], prd[9]))

    return listProduct


@app.route('/public/category/<category>', methods=['GET', 'POST'])
def public_category(category=None):
    listProduct = []
    main = MainModel
    if (int(category) >= 10):
        pro_result = main.SelectDBWhere('product', "refcategory = '" + category + "' AND active = '1'")
    else:
        pro_result = main.SelectDBWhere('product', "refcategory in (SELECT id FROM category WHERE refparent = '" + category + "') AND active = '1'")
    for prd in pro_result:
        listProduct.append(Product(prd[0], prd[1], prd[2], prd[3], prd[4], prd[5], prd[6], prd[7], prd[8], prd[9]))

    cat_result = load_all_category()
    return render_template('/public/product.html', products=listProduct, category=cat_result)


@app.route('/admin/category', methods=['POST'])
def category_crud():
    if request.method == "POST":
        id = request.form['new_cat_id']
        name = request.form['new_cat_name']
        desc = request.form['new_cat_des']
        act = request.form['new_cat_act']
        par = request.form['new_cat_par']
        type = request.form['new_cat_type']

        data = {}
        data['category'] = name
        data['description'] = desc
        data['active'] = act
        data['refparent'] = par

        main = MainModel

        if type == 'C':
            main.InsertDB(data, 'category')

        elif type == 'U':
            main.UpdateDB(data, 'category', 'id', id)

        elif type == 'D':
            main.DeleteDB('category', 'id', id)

        else:
            return

    return redirect(url_for('admin_category'))


@app.route('/admin/product', methods=['POST'])
def product_crud():
    id = request.form['new_prd_id']
    name = request.form['new_prd_name']
    desc = request.form['new_prd_des']
    image = request.form['new_prd_img']
    price = request.form['new_prd_price']
    cate = request.form['new_prd_cate']
    dis = request.form['new_prd_dis']
    act = request.form['new_prd_act']
    type = request.form['new_prd_type']
    disprice = request.form['new_prd_disprice']
    option = request.form['new_prd_option_1'] # + request.form['new_prd_option_2'] (if have)

    data = {}
    data['name'] = name
    data['description'] = desc
    data['imageurl'] = image
    data['price'] = price
    data['refcategory'] = cate
    data['refdiscount'] = dis
    data['active'] = act
    data['discount_price'] = disprice
    data['option'] = option

    main = MainModel
    
    if type == "C":
        main.InsertDB(data, 'product')

    elif type == "U":
        main.UpdateDB(data, 'product', 'id', id)

    elif type == "D":
        main.DeleteDB('product', 'id', id)

    else:
        return

    return redirect(url_for('admin_product'))


if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True)
