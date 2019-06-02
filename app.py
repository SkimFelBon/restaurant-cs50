import os, psycopg2
import json, urllib.parse, datetime
from flask import Flask, request, make_response, render_template, redirect, url_for
from flask import flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from flask_babelex import Babel, gettext
from werkzeug.security import check_password_hash

from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
babel = Babel(app)
login = LoginManager(app)

from models import Users, Product, Language, Product_translation, Picture
from helpers import translateOrder, trelloCard, trelloChecklist, addCheckListItem
#--------------------------------------------------
@login.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'en')

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class LogOutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect(url_for("login"))


admin = Admin(app, index_view = MyAdminIndexView(), name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(Users, db.session))
admin.add_view(MyModelView(Product, db.session))
admin.add_view(MyModelView(Language, db.session))
admin.add_view(MyModelView(Product_translation, db.session))
admin.add_view(LogOutView(name='Log out', endpoint='login'))
#--------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user
    logout_user()
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide valid username", "alert-warning")
            return redirect("/login")
        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide valid password", "alert-warning")
            return redirect("/login")
        rows = Users.query.filter_by(name=request.form.get("username")).first()
        if rows == None:
            flash("invalid username and/or password", "alert-warning")
            return redirect("/login")
        if rows.id <= 0 or not (check_password_hash(rows.hash, request.form.get("password"))):
            flash("invalid username and/or password", "alert-warning")
            return redirect("/login")

        login_user(rows)
        return redirect(url_for("admin.index"))
    return render_template("login.html", title="Login")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))
#----------------------------------------
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    # !!! add your custom code to check that the uploaded file is,
    # a valid image and not a malicious file
    file.save(f)
    upload_img_loc = Picture(ImageLocation=f)
    db.session.add(upload_img_loc)
    db.session.commit()
    return redirect(url_for("admin.index"))

#------------------ADMIN-PART-END--------------------------------------

@app.route("/")
def index():
    pageLanguage = get_locale()

    encodedOrder = translateOrder('Order', pageLanguage)
    title = gettext("Order pizza online")
    resp = make_response(render_template("index.html", title=title))
    if encodedOrder != 0:
        expire_date = datetime.datetime.now()
        expire_date = expire_date + datetime.timedelta(days=1)
        resp.set_cookie('Order', encodedOrder, expires=expire_date, path='/')
    return resp

@app.route("/menu")
def menu():
    # DONE Create multi language db for menu
    # DONE create pizza menu table
    # DONE add way to insert images to menu, from admin page
    """ Show Menu"""
    arrayName = []; arrayIngrd = [] ;arrayPrice = []; arrayImage = []
    pageLang = get_locale()
    lang_id = Language.query.filter_by(name=pageLang).first()
    results = Product_translation.query.filter_by(language_id=lang_id.id).all()
    for i in range(len(results)):
        arrayName.append(results[i].name)
        arrayIngrd.append(results[i].ingredients)
        Resultprice = Product.query.filter_by(id=results[i].product_non_trans_id).first()
        ResultImage = Picture.query.filter_by(id=results[i].ImageLoc_id).first()
        arrayPrice.append(Resultprice.price)
        arrayImage.append(ResultImage.ImageLocation)
    title = gettext("Menu")
    return render_template("menu.html", title=title,
    arrayName=arrayName, arrayIngrd=arrayIngrd, arrayPrice=arrayPrice, arrayImage=arrayImage)
#-------------------------------------------------------------
@app.route("/locations")
def locations():
    title = gettext("Locations of Restaurant")
    return render_template("locations.html", title=title)

#-------------------------------------------------------------
@app.route("/contact")
def contact():
    title = gettext('Contacts')
    return render_template("contact.html", title=title)

#-------------------------------------------------------------

@app.route("/order", methods=["GET", "POST"])
def order():
    if request.method == "POST":
        customer_name = request.form.get('name')
        customer_phone = request.form.get('phone')
        customer_address = request.form.get('address')
        if not customer_name:
            nameEmpty = gettext("Please fill out Name field!")
            flash(nameEmpty, "alert-warning")
            return redirect("/order")
        if not customer_phone:
            phoneEmpty = gettext("Please provide a valid phone number.")
            flash(phoneEmpty, "alert-warning")
            return redirect("/order")
        if not customer_address:
            customer_address = "self-pickup"
        orderCookie = request.cookies.get('Order', 0)
        # DONE Check if orderCookie exist
        orderEmpty = gettext("Your order is empty")
        if orderCookie == 0:
            flash(orderEmpty, "alert-warning")
            return redirect("/order")
        strCookie = urllib.parse.unquote(orderCookie)
        dictCookie = json.loads(strCookie)
        # DONE check if dictCookie isn't empty
        if len(dictCookie['Pizza'].keys()) == 0:
            resp = make_response(redirect("/order"))
            resp.set_cookie('Order',"", expires=0, path='/')
            flash(orderEmpty, "alert-warning")
            return resp

        # DONE query db for OrderCookie Check if item exist and price is correct
        for pizzaName in dictCookie['Pizza'].keys():
            productObject = Product_translation.query.filter_by(name=pizzaName).first()
            if productObject == None:
                resp = make_response(redirect("/order"))
                resp.set_cookie('Order',"", expires=0, path='/')
                faultyOrder = gettext("Faulty order, please create new order")
                flash(faultyOrder, "alert-danger")
                return resp
            # DONE check price
            priceResult = Product.query.filter_by(id=productObject.product_non_trans_id).first()
            if dictCookie['Pizza'][pizzaName][0]['Price'] != priceResult.price:
                resp = make_response(redirect("/order"))
                resp.set_cookie('Order',"", expires=0, path='/')
                flash(faultyOrder, "alert-danger")
                return resp
        # DONE add card to board
        newCard = trelloCard(customer_name, customer_phone, customer_address, dictCookie)
        if newCard == None:
            failedOrder = gettext("Failed to finish your order")
            flash(failedOrder, "alert-danger")
            return redirect("/order")

        # DONE Add checklist to card
        newChecklist = trelloChecklist(newCard)

        # DONE add an checklist item for every pizza in order
        for pizzaName in dictCookie['Pizza'].keys():
            pizzaAmount = dictCookie['Pizza'][pizzaName][1]['Amount']
            for i in range(pizzaAmount):
                addCheckListItem(pizzaName,newChecklist)
        successOrder = gettext("Your order will be delivered shortly!")
        boardTrello = gettext("Trello Board with your Order")
        flash(successOrder, "alert-success")
        title = gettext("Order pizza online")
        link = "<a href=\"https://trello.com/b/xOv78tYw/restaurant\">" + str(boardTrello) + "</a>"
        resp = make_response(render_template("index.html",
            title=title, link=link))
        # DONE delete Cookie file
        resp.set_cookie('Order',"", expires=0, path='/')
        return resp
    ## DONE translate OrderCookie upon language change
    ## TODO newpageLanguage = get_locale()
    pageLanguage = get_locale()



    encodedOrder = translateOrder('Order', pageLanguage)
    resp = make_response(render_template("order.html", title="Order"))
    if encodedOrder != 0:
        expire_date = datetime.datetime.now()

        expire_date = expire_date + datetime.timedelta(days=1)

        resp.set_cookie('Order', encodedOrder, expires=expire_date, path='/')
    return resp


if __name__ == "__main__":
    app.run()
