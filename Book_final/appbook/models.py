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
        # c1 = Category(name='Sách văn học')
        # c2 = Category(name='Sách thiếu nhi')
        # c3 = Category(name='Sách kinh tế')
        # c4 = Category(name='Sách tiểu thuyết')
        # c5 = Category(name='Sách địa lý')
        #
        # db.session.add(c1)
        # db.session.add(c2)
        # db.session.add(c3)
        # db.session.add(c4)
        # db.session.add(c5)
        #
        # db.session.commit()
        #
        # p1 = Product(name= 'Nhà giả kim', author = 'Paulo Coelho', description = 'Nhà giả kim là tiểu thuyết được xuất bản lần đầu ở Brasil năm 1988, và là cuốn sách nổi tiếng nhất của nhà văn Paulo Coelho. Tác phẩm là một trong những cuốn sách bán chạy nhất mọi thời đại.',
        #             price = 55000, quantity = 300, image = 'https://res.cloudinary.com/drda2ewdn/image/upload/v1671207498/p1_wk9obk.jpg', category_id = 1)
        # p2 = Product(name= 'Hoàng tử bé', author= 'Antoine de Saint-Exupéry', description = 'Hoàng tử bé, được xuất bản năm 1943, là tiểu thuyết nổi tiếng nhất của nhà văn và phi công Pháp Antoine de Saint-Exupéry.', price = 75000,
        #             quantity = 300, image = 'https://res.cloudinary.com/drda2ewdn/image/upload/v1671207498/p2_y76tm0.jpg', category_id = 2)
        # p3 = Product(name ='Tái tạo kép', author = 'Mark W. Johnson', description = 'Thị trường ngày nay liên tục thay đổi, các doanh nghiệp sinh ra và mất đi, và ngay cả các doanh nghiệp uy tín, lâu năm vẫn thường xuyên thất bại, thậm chí sụp đổ bởi những công nghệ đột phá.', price = 128500,
        #             quantity = 300, image = 'https://res.cloudinary.com/drda2ewdn/image/upload/v1671207498/p3_cs8xtk.jpg', category_id = 3)
        # p4 = Product(name='Rừng Nauy', author='Haruki Murakami', description='Rừng Na uy", im lặng, ma thuật và tuyệt vọng như một chấm máu cô độc giữa bạt ngàn tuyết lạnh.',
        #              price=150000, quantity=300, image='https://res.cloudinary.com/drda2ewdn/image/upload/v1671207498/p4_toxeoh.jpg', category_id=4)
        # p5 = Product(name='Spy X Family', author='Tatsuya Endo', description='Cuối cùng thì Twilight cũng tiếp xúc được với mục tiêu Desmond lần đầu tiên bằng cách xen vào cuộc gặp gỡ giữa hắn và cậu con trai thứ Damian!!',
        #              price=	20000, quantity=300, image='https://res.cloudinary.com/drda2ewdn/image/upload/v1671207498/p5_t8uhrn.jpg', category_id=2)
        # p6 = Product(name='Sơn Nam', author='Sơn Nam',
        #              description='Tìm hiểu đất Hậu Giang là tác phẩm biên khảo đầu tiên của nhà văn Sơn Nam về vùng đất ông đã sinh ra, lớn lên và trưởng thành.',
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
