from app.models import LoaiPhong, Phong, User, Receipt, ReceiptDetails
from app import app, db
import hashlib
import cloudinary.uploader
from flask_login import current_user
from sqlalchemy import func


def load_categories():
    return LoaiPhong.query.all()


def load_products(kw=None, cate_id=None, page = None):

   products = Phong.query

   if kw:
       products = products.filter(Phong.name.contains(kw))



   if cate_id:
        products = products.filter(Phong.category_id.__eq__(cate_id))

   if page:
        page = int(page)
        page_size = app.config['PAGE_SIZE']
        start = (page - 1) * page_size
        return products.slice(start, start + page_size)

   return products.all()

def count_product():
    return Phong.query.count()

def get_user_by_id(id):
    return User.query.get(id)



def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                            User.password.__eq__(password)).first()

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                            User.password.__eq__(password)).first()


def add_user(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username, password=password)
    if avatar:
        res = cloudinary.uploader.upload(avatar)
        print(res)
        u.avatar = res['secure_url']

    db.session.add(u)
    db.session.commit()

def count_products_by_cate():
    return db.session.query(LoaiPhong.id, LoaiPhong.name, func.count(Phong.id))\
                     .join(Phong, Phong.category_id == LoaiPhong.id, isouter=True).group_by(LoaiPhong.id).all()


def revenue_stats(kw=None):
    query = db.session.query(Phong.id,Phong.name, func.sum(ReceiptDetails.price*ReceiptDetails.quantity))\
                     .join(ReceiptDetails, ReceiptDetails.product_id == Phong.id).group_by(Phong.id)
    if kw:
        query = query.filter(Phong.name.contains(kw))

    return query


def add_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], price=c['price'],
                               receipt=r, product_id=c['id'])
            db.session.add(d)

        db.session.commit()