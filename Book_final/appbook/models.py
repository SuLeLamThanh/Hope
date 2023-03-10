from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship, backref
from appbook import db, app
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=False)

    def __str__(self):
        return self.name


prod_tag = db.Table('prod_tag',
                    Column('product_id', Integer,
                           ForeignKey('product.id'), nullable=False, primary_key=True),
                    Column('tag', Integer,
                           ForeignKey('tag.id'), nullable=False, primary_key=True))


class Product(BaseModel):
    name = Column(String(50), nullable=False)
    author = Column(String(50), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    quantity = Column(Integer)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    tags = relationship('Tag', secondary='prod_tag', lazy='subquery',
                        backref=backref('products', lazy=True))
    receipt_detail = relationship('ReceiptDetail', backref='product', lazy=True)
    comments = relationship('Comment', backref='product', lazy=True)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetail', backref='receipt', lazy=True)


class ReceiptDetail(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)


class Comment(BaseModel):
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # c1 = Category(name='S??ch v??n h???c')
        # c2 = Category(name='S??ch thi???u nhi')
        # c3 = Category(name='S??ch kinh t???')
        # c4 = Category(name='S??ch ti???u thuy???t')
        # c5 = Category(name='S??ch ?????a l??')
        #
        # db.session.add(c1)
        # db.session.add(c2)
        # db.session.add(c3)
        # db.session.add(c4)
        # db.session.add(c5)
        #
        # db.session.commit()
        #
        # p1 = Product(name= 'Nh?? gi??? kim', author = 'Paulo Coelho', description = 'Nh?? gi??? kim l?? ti???u thuy???t ???????c xu???t b???n l???n ?????u ??? Brasil n??m 1988, v?? l?? cu???n s??ch n???i ti???ng nh???t c???a nh?? v??n Paulo Coelho. T??c ph???m l?? m???t trong nh???ng cu???n s??ch b??n ch???y nh???t m???i th???i ?????i.',
        #             price = 55000, quantity = 300, image = 'https://res.cloudinary.com/drda2ewdn/image/upload/v1671207498/p1_wk9obk.jpg', category_id = 1)
        # p2 = Product(name= 'Ho??ng t??? b??', author= 'Antoine de Saint-Exup??ry', description = 'Ho??ng t??? b??, ???????c xu???t b???n n??m 1943, l?? ti???u thuy???t n???i ti???ng nh???t c???a nh?? v??n v?? phi c??ng Ph??p Antoine de Saint-Exup??ry.', price = 75000,
        #             quantity = 300, image = 'https://res.cloudinary.com/drda2ewdn/image/upload/v1671207498/p2_y76tm0.jpg', category_id = 2)
        # p3 = Product(name ='T??i t???o k??p', author = 'Mark W. Johnson', description = 'Th??? tr?????ng ng??y nay li??n t???c thay ?????i, c??c doanh nghi???p sinh ra v?? m???t ??i, v?? ngay c??? c??c doanh nghi???p uy t??n, l??u n??m v???n th?????ng xuy??n th???t b???i, th???m ch?? s???p ????? b???i nh???ng c??ng ngh??? ?????t ph??.', price = 128500,
        #             quantity = 300, image = 'https://res.cloudinary.com/drda2ewdn/image/upload/v1671207498/p3_cs8xtk.jpg', category_id = 3)
        # p4 = Product(name='R???ng Nauy', author='Haruki Murakami', description='R???ng Na uy", im l???ng, ma thu???t v?? tuy???t v???ng nh?? m???t ch???m m??u c?? ?????c gi???a b???t ng??n tuy???t l???nh.',
        #              price=150000, quantity=300, image='https://res.cloudinary.com/drda2ewdn/image/upload/v1671207498/p4_toxeoh.jpg', category_id=4)
        # p5 = Product(name='Spy X Family', author='Tatsuya Endo', description='Cu???i c??ng th?? Twilight c??ng ti???p x??c ???????c v???i m???c ti??u Desmond l???n ?????u ti??n b???ng c??ch xen v??o cu???c g???p g??? gi???a h???n v?? c???u con trai th??? Damian!!',
        #              price=	20000, quantity=300, image='https://res.cloudinary.com/drda2ewdn/image/upload/v1671207498/p5_t8uhrn.jpg', category_id=2)
        # p6 = Product(name='S??n Nam', author='S??n Nam',
        #              description='T??m hi???u ?????t H???u Giang l?? t??c ph???m bi??n kh???o ?????u ti??n c???a nh?? v??n S??n Nam v??? v??ng ?????t ??ng ???? sinh ra, l???n l??n v?? tr?????ng th??nh.',
        #              price=120000, quantity=300,
        #              image='https://res.cloudinary.com/drda2ewdn/image/upload/v1671207498/p6_fudtul.jpg', category_id=5)
        #
        # db.session.add(p1)
        # db.session.add(p2)
        # db.session.add(p3)
        # db.session.add(p4)
        # db.session.add(p5)
        # db.session.add(p6)
        #
        # db.session.commit()

        # import hashlib
        # password = str(hashlib.md5('12345678'.encode('utf-8')).hexdigest())
        # u = User(name='Thanh', username='admin',
        #         password=password,
        #         user_role=UserRole.ADMIN,
        #         avatar='https://res.cloudinary.com/drda2ewdn/image/upload/v1670590761/cn2bjpeh0dkjxcb7eymp.jpg')
        # db.session.add(u)
        # db.session.commit()
        #
