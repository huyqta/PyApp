import os
import urllib
import urllib2
import re
from flask import Flask, render_template, url_for, request, redirect, session, jsonify, send_from_directory, make_response
from werkzeug import secure_filename
# from flask.ext import breadcrumbs
# from flask import Blueprint
# from flask.ext.cors import CORS
from entity.category import Category
from entity.product import Product
from entity.trademark import Trademark
from entity.image import Image
from model.main_model import *
from JSONEncoder import *
from breadcrumb import breadcrumb
from myutils import *
from myapis import *

app = Flask(__name__)

# Initialize Flask-Breadcrumbs
# breadcrumbs.Breadcrumbs(app=app)

# conn = pymysql.connect(host='localhost', user='root', passwd='', port=3306, db='dbtracking', charset='utf8', autocommit=True)
# cur = conn.cursor()
# CORS(app, resources=r'/admin/*', headers='Content-Type')
# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'static/public/img/products/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
@app.route('/public')
def index():
    product = load_all_product()
    category = load_all_category()
    trademmark = load_all_trademark()
    return render_template('public/index.html', product=product, category=category, trademark=trademmark)


@app.route('/public/gmap')
def gmap():
    return render_template('public/gmap.html')


# @app.route('/public/product')
# def product():
# product = load_all_product()
# category = load_all_category()
# return render_template('public/category.html', product=product, category=category)


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
    result = SelectDB('account')
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


@app.route('/admin/trademark')
def admin_trademark():
    trm_result = load_all_trademark()
    cat_result = load_all_category()
    return render_template('/admin/trademark.html', trademarks=trm_result, category=cat_result)


@app.route('/admin/product')
def admin_product():
    pro_result = load_all_product()
    cat_result = load_all_category()
    img_result = load_all_images()
    trm_result = load_all_trademark()
    return render_template('/admin/product.html', product=pro_result, category=cat_result, images=img_result, trademark=trm_result)


# @app.route('/admin/images')
# def admin_images():
# pro_result = load_all_product()
# img_result = load_all_images()
# return render_template('/admin/images.html', product=pro_result, images=img_result)


def load_all_category():
    listCategory = []
    cat_result = SelectDB('category')
    for cat in cat_result:
        listCategory.append(Category(cat[0], cat[1], cat[2], cat[3], cat[4]))

    return listCategory


def load_all_trademark():
    listTrademark = []
    trm_result = SelectDB('trademark')
    for trm in trm_result:
        listTrademark.append(Trademark(trm[0], trm[1], trm[2], trm[3], trm[4], trm[5]))

    return listTrademark


def load_all_product():
    listProduct = []
    pro_result = SelectDB('product')
    for prd in pro_result:
        listProduct.append(Product(prd[0], prd[1], prd[2], prd[3], prd[4], prd[5], prd[6], prd[7], prd[8], prd[9], prd[10], prd[11]))

    return listProduct


def load_single_product(id=None):
    listProduct = []
    pro_result = SelectDBWhere('product', 'id = ' + id)
    for prd in pro_result:
        listProduct.append(Product(prd[0], prd[1], prd[2], prd[3], prd[4], prd[5], prd[6], prd[7], prd[8], prd[9], prd[10], prd[11]))

    return listProduct[0]


def load_random_product():
    listProduct = []
    pro_result = Execute('SELECT * FROM `product` WHERE id >= (SELECT FLOOR( MAX(id) * RAND()) FROM `product` ) AND active = 1 ORDER BY id LIMIT 5')
    for prd in pro_result:
        listProduct.append(Product(prd[0], prd[1], prd[2], prd[3], prd[4], prd[5], prd[6], prd[7], prd[8], prd[9], prd[10], prd[11]))

    return listProduct


def load_all_images():
    listImages = []
    img_result = SelectDB('images')
    for img in img_result:
        listImages.append(Image(img[0], img[1], img[2]))
    return listImages


def load_product_images(productid=None):
    listImages = []
    img_result = SelectDBWhere('images', 'refproduct = ' + productid)
    for img in img_result:
        listImages.append(Image(img[0], img[1], img[2]))
    return listImages


@app.route('/admin/images/<product>', methods=['GET', 'POST'])
def admin_images(product=None):
    listImage = []
    # if 'product' in request.form:
    # product = request.form['product']
    # else:
    # product = None

    if (product == None):
        where = "refproduct = -1"
    else:
        where = "refproduct = '" + product + "'"

    img_result = SelectDBWhere('images', where)
    # return str(len(pro_result))
    for prd in img_result:
        listImage.append(Image(prd[0], prd[1], prd[2]))

    prd_result = load_all_product()

    return render_template('/admin/images.html', product=prd_result, images=listImage)


@app.route('/<category>', methods=['GET', 'POST'])
@app.route('/public/category/<category>', methods=['GET', 'POST'])
# @app.route('/public/trademark/category/<category>', methods=['GET', 'POST'])
def public_category(category=None):
    listProduct = []
    where = "refcategory = '" + category + "' AND active = '1'"

    where = where + getFilterPrice()

    pro_result = SelectDBWhere('product', where)
    # return str(len(pro_result))
    for prd in pro_result:
        listProduct.append(Product(prd[0], prd[1], prd[2], prd[3], prd[4], prd[5], prd[6], prd[7], prd[8], prd[9], prd[10], prd[11]))

    cat_result = load_all_category()
    img_result = load_all_images()
    trm_result = load_all_trademark()

    bc = parseBreadCrumbCategory(cat_result, "/public/category/" + category, category)
    return render_template('/public/category.html', products=listProduct, category=cat_result, images=img_result, trademark=trm_result, breadcrumb=bc)


@app.route('/public/trademark/<trademark>', methods=['GET', 'POST'])
# @app.route('/public/trademark/trademark/<trademark>', methods=['GET', 'POST'])
def public_trademark(trademark=None):
    listProduct = []
    if 'filter_price' in request.form:
        filterprice = request.form['filter_price']
    else:
        filterprice = None

    where = "reftrademark = '" + trademark + "' AND active = '1'"
    if filterprice != None:
        where = where + getFilterPrice(filterprice)

    pro_result = SelectDBWhere('product', where)
    # return str(len(pro_result))
    for prd in pro_result:
        listProduct.append(Product(prd[0], prd[1], prd[2], prd[3], prd[4], prd[5], prd[6], prd[7], prd[8], prd[9], prd[10], prd[11]))

    cat_result = load_all_category()
    img_result = load_all_images()
    trm_result = load_all_trademark()
    bc = parseBreadCrumbTrademark(trm_result, cat_result, "/public/category/" + trademark, trademark)
    return render_template('/public/category.html', products=listProduct, category=cat_result, images=img_result, trademark=trm_result, breadcrumb=bc)


@app.route('/public/search', methods=['GET', 'POST'])
def public_search():
    listProduct = []
    input = request.form['input']
    query = "SELECT * FROM product WHERE name LIKE '%" + input + "%'"
    pro_result = Execute(query)
    for prd in pro_result:
        listProduct.append(Product(prd[0], prd[1], prd[2], prd[3], prd[4], prd[5], prd[6], prd[7], prd[8], prd[9], prd[10], prd[11]))

    cat_result = load_all_category()
    img_result = load_all_images()
    return render_template('/public/search_result.html', products=listProduct, category=cat_result, images=img_result)


@app.route('/product/<product>', methods=['GET', 'POST'])
@app.route('/public/product/<product>', methods=['GET', 'POST'])
def public_product(product=None):
    cat_result = load_all_category()
    productobj = load_single_product(product)
    images = load_product_images(product)
    random_product = load_random_product()
    r = make_response(render_template('/public/product.html', category=cat_result, product=productobj, images=images, randomprd=random_product))
    # r.mimetype = 'text/html'
    return r
    # return render_template('/public/product.html', category=cat_result, product=productobj, images=images, mimetype = 'text/html')


def getFilterPrice():
    filter = ""
    if 'filter_price' in request.form:
        filterprice = request.form['filter_price']
    else:
        filterprice = None

    if filterprice != None:
        if (filterprice == "1"):
            filter += " AND price > 5000000"
        elif (filterprice == "2"):
            filter += " AND price <= 5000000 AND price > 3000000"
        elif (filterprice == "3"):
            filter += " AND price <= 3000000 AND price > 1000000"
        elif (filterprice == "4"):
            filter += " AND price <= 1000000"
        elif (filterprice == "0"):
            filter += ""

    if 'filter_trademark' in request.form:
        filtertrademark = request.form['filter_trademark']
    else:
        filtertrademark = None

    if filtertrademark != None:
        filter += " AND reftrademark = '" + filtertrademark + "'"

    return filter


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

        if type == 'C':
            InsertDB(data, 'category')

        elif type == 'U':
            UpdateDB(data, 'category', 'id', id)

        elif type == 'D':
            DeleteDB('category', 'id', id)

        else:
            return

    return redirect(url_for('admin_category'))


@app.route('/admin/trademark', methods=['POST'])
def trademark_crud():
    if request.method == "POST":
        id = request.form['new_trm_id']
        name = request.form['new_trm_name']
        desc = request.form['new_trm_des']
        act = request.form['new_trm_act']
        par = request.form['new_trm_par']
        cat = request.form['new_trm_cat']
        type = request.form['new_trm_type']

        data = {}
        data['name'] = name
        data['description'] = desc
        data['active'] = act
        data['urllogo'] = par
        data['refcategory'] = cat

        if type == 'C':
            InsertDB(data, 'trademark')

        elif type == 'U':
            UpdateDB(data, 'trademark', 'id', id)

        elif type == 'D':
            DeleteDB('trademark', 'id', id)

        else:
            return

    return redirect(url_for('admin_trademark'))


@app.route('/admin/product', methods=['POST'])
def product_crud():
    if request.method == "POST":

        id = request.form['new_prd_id']
        name = request.form['new_prd_name']
        desc = request.form['new_prd_des']
        tech = request.form['new_prd_tech']
        image = request.form['new_prd_img']
        price = request.form['new_prd_price']
        cate = request.form['new_prd_cate']
        dis = request.form['new_prd_dis']
        act = request.form['new_prd_act']
        type = request.form['new_prd_type']
        disprice = request.form['new_prd_disprice']
        trademark = request.form['new_prd_trm']
        option = request.form['new_prd_option']  # + request.form['new_prd_option_2'] (if have)

        data = {}
        data['name'] = name
        data['description'] = desc
        data['technical'] = tech
        data['imageurl'] = image
        data['price'] = price
        data['refcategory'] = cate
        data['refdiscount'] = dis
        data['active'] = act
        data['discount_price'] = disprice
        data['option'] = option
        data['reftrademark'] = trademark

        if type == "C":
            InsertDB(data, 'product')

        elif type == "U":
            UpdateDB(data, 'product', 'id', id)

        elif type == "D":
            DeleteDB('product', 'id', id)

        else:
            return

    return redirect(url_for('admin_product'))


def image_crud(isdefault=None, refproduct=None, imageurl=None, type=None):
    data = {}
    data['imageurl'] = imageurl
    data['refproduct'] = refproduct
    data['isdefault'] = isdefault

    if type == "C":
        InsertDB(data, 'images')
    #
    # elif type == "U":
    # UpdateDB(data, 'images', 'id', id)

    elif type == "D":
        DeleteDB('images', 'imageurl', imageurl)

    return


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


# Route that will process the file upload
@app.route('/admin/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    uploaded_files = request.files.getlist("file")
    refproduct = request.form['refproduct']
    filenames = []
    for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to the upload
            # folder we setup
            fullpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(fullpath)
            # Save the filename into a list, we'll use it later
            filenames.append(filename)
            # image_crud("0", refproduct, request.url_root + fullpath, "C")
            image_crud("0", refproduct, fullpath, "C")
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
    # Load an html page with a link to each uploaded file
    return redirect(url_for('uploaded_file',
                            filename=filename))


# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/admin/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/delivery_policy')
def delivery_policy():
    return render_template('public/delivery_policy.html')


@app.route('/maintain_policy')
def maintain_policy():
    return render_template('public/maintain_policy.html')


@app.route('/change_policy')
def change_policy():
    return render_template('public/change_policy.html')


@app.route('/target_policy')
def target_policy():
    return render_template('public/target_policy.html')


@app.route('/apis/getstreamfromhttp', methods=['POST'])
def get_stream_from_url():
    url = request.form['url']
    try:
        resp = urllib2.urlopen(url)
        contents = resp.read()
        if url.find("xemphimso.com") > -1:
            matchObj = re.search("(file: ').*(',)", contents)
            if matchObj:
                last_url = matchObj.group().replace("file: '", "").replace("',", "")
                return last_url

        elif url.find("www.tivi24h.com") > -1:
            matchObj = re.search("(var responseText = ).*(;)", contents)
            if matchObj:
                last_url = matchObj.group().replace('var responseText = "', '').replace('";', '')
                return last_url

        elif url.find("tv.tivi24h.com") > -1:
            matchObj = re.search("(var responseText = ).*(;)", contents)
            if matchObj:
                last_url = matchObj.group().replace('file: "', '').replace('",image:', '').replace('";', '')
                return last_url

            matchObj = re.search("(var responseText = ).*(;)", contents)
            if matchObj:
                last_url = matchObj.group().replace('file: "', '').replace('",image:', '').replace('";', '')
                return last_url

        elif url.find("tivi360") > -1:
            matchObj = re.search("(var responseText = ).*(;)", contents)
            if matchObj:
                last_url = matchObj.group().replace('var responseText = "', '').replace('";', '')
                return last_url

        elif url.find("htvonline") > -1:
            matchObj = re.search('(file: ").*(",)', contents)
            if matchObj:
                last_url = matchObj.group().replace('file: "', '').replace('",', '')
                return last_url

	elif url.find("http://tv24.vn/") > -1:
            matchObj = re.search("('file': 'http).*(',)", contents)
            if matchObj:
                last_url = matchObj.group().replace("'file': '", "").replace("',", "")
                return last_url


        return ""
    except urllib2.HTTPError, error:
        contents = error.read()
        return "ERROR"

if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(host='0.0.0.0', debug=True)
