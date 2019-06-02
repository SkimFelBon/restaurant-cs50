from app import db
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    hash = db.Column(db.String(256), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phoneNumber = db.Column(db.String(255), unique=True, nullable=False)
    comment = db.Column(db.String(255), nullable=False)

    def __init__(self, name = "", hash = "", address = "", phoneNumber = "", comment = ""):
        self.name = name
        self.hash = hash
        self.address = address
        self.phoneNumber = phoneNumber
        self.comment = comment

    def __repr__(self):
        return '<name {}>'.format(self.name)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    trans = db.relationship('Product_translation', backref='price')

    def __init__(self, price = ""):
        self.price = price

    def __repr__(self):
        return '<price {}>'.format(self.price)

class Picture(db.Model):
    __tablename__ = 'picture'
    id = db.Column(db.Integer, primary_key=True)
    ImageLocation = db.Column(db.String(255), unique=True, nullable=False)
    pic = db.relationship('Product_translation', backref='images')

    def __init__(self, ImageLocation = ""):
        self.ImageLocation = ImageLocation

    def __repr__(self):
        return '<picture {}>'.format(self.ImageLocation)

class Language(db.Model):
    __tablename__ = 'language'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    lang = db.relationship('Product_translation', backref='language')

    def __init__(self, name = ""):
        self.name = name

    def __repr__(self):
        return '<language {}>'.format(self.name)

class Product_translation(db.Model):
    __tablename__ = 'product_translation'
    id = db.Column(db.Integer, primary_key=True)
    product_non_trans_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
    ImageLoc_id = db.Column(db.Integer, db.ForeignKey("picture.id"))
    type = db.Column(db.String(255))
    name = db.Column(db.String(255))
    ingredients = db.Column(db.String(255))

    def __init__(self,product_non_trans_id="",language_id="",ImageLoc_id="",type="",name="",ingredients=""):
        self.product_non_trans_id = product_non_trans_id
        self.language_id = language_id
        self.ImageLoc_id = ImageLoc_id
        self.type = type
        self.name = name
        self.ingredients = ingredients

    def __repr__(self):
        return '<product_translation {}>'.format(self.name)
