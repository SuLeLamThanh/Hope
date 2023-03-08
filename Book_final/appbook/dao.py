from appbook.models import User, Category, Product, User, ReceiptDetail, Comment, Receipt
from flask_login import current_user
from sqlalchemy import func
from appbook import db
import hashlib
from sqlalchemy.sql import extract


def load_categories():
    return Category.query.all()


def load_products(category_id=None, kw=None):
    query = Product.query.filter(Product.active.__eq__(True))

    if category_id:
        query = query.filter(Product.category_id.__eq__(category_id))

    if kw:
        query = query.filter(Product.name.contains(kw))

    return query.all()


def get_product_by_id(product_id):
    return Product.query.get(product_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def register(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username.strip(), password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def add_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetail(quantity=c['quantity'], price=c['price'],
                               receipt=r, product_id=c['id'])
            db.session.add(d)

        try:
            db.session.commit()
        except:
            return False
        else:
            return True


def count_product_by_cate():
    return db.session.query(Category.id, Category.name, func.count(Product.id))\
                     .join(Product, Product.category_id.__eq__(Category.id), isouter=True)\
                     .group_by(Category.id).order_by(Category.id).all()


def stats1_revenue(year):
    p = db.session.query(extract('month', Receipt.created_date), Product.name,
                         func.sum(ReceiptDetail.quantity))\
                  .join(Category, Product.category_id.__eq__(Category.id), isouter=True)\
                  .join(ReceiptDetail, ReceiptDetail.product_id.__eq__(Product.id), isouter=True)\
                  .join(Receipt, Receipt.id.__eq__(ReceiptDetail.receipt_id))\
                  .group_by(extract('month', Receipt.created_date), Product.name)

    return p.order_by(extract('month', Receipt.created_date)).all()


def stats_revenue(kw=None, from_date=None, to_date=None):
    p = db.session.query(extract('month', Receipt.created_date), Category.name,
                         func.sum(ReceiptDetail.quantity * ReceiptDetail.price))\
                  .join(Product, Product.category_id.__eq__(Category.id), isouter=True)\
                  .join(ReceiptDetail, ReceiptDetail.product_id.__eq__(Product.id), isouter=True)\
                  .join(Receipt, Receipt.id.__eq__(ReceiptDetail.receipt_id))\
                  .group_by(extract('month', Receipt.created_date), Category.name)

    if kw:
        p = p.filter(Product.name.contains(kw))

    if from_date:
        p = p.filter(Receipt.created_date.__ge__(from_date))

    if to_date:
        p = p.filter(Receipt.created_date.__le__(to_date))

    return p.order_by(extract('month', Receipt.created_date)).all()


def load_comments_by_prod(product_id):
    return Comment.query.filter(Comment.product_id.__eq__(product_id)).order_by(-Comment.id).all()


def add_comment(product_id, content):
    c = Comment(content=content, product_id=product_id, user=current_user)
    db.session.add(c)
    db.session.commit()

    return c


if __name__ == '__main__':
    from appbook import app
    with app.app_context():
        print(load_comments_by_prod(1))