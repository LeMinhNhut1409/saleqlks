from collections import defaultdict

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from app import db
from flask_login import UserMixin
import enum
from datetime import datetime



class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default='https://hoanghamobile.com/tin-tuc/wp-content/uploads/2023/07/avatar-dep-13-1.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    # receipts = relationship('Receipt', backref='user', lazy=True)
    # comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name


class LoaiPhong(db.Model):
    __tablename__ = 'LoaiPhong'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    products= relationship('Phong', backref='loaiphong', lazy=True)

    def __str__(self):
        return self.name


class Phong(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    price = Column(Float, default=0)
    category_id = Column(Integer, ForeignKey(LoaiPhong.id), nullable=False)
    image = Column(String(100))
    acreage =Column(Float,default=0)
    # receipt_details = relationship('ReceiptDetails', backref='phong', lazy=True)
    # comments = relationship('Comment', backref='phong', lazy=True)


    def __str__(self):
        return self.name


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)


class Receipt(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Phong.id), nullable=False)


class Interaction(BaseModel):
    __abstract__ = True

    product_id = Column(Integer, ForeignKey(Phong.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)


# class Comment(Interaction):
#     content = Column(String(255), nullable=False)
#     created_date = Column(DateTime, default=datetime.now())





if __name__ == "__main__":
    from app import app
    with app.app_context():
          db.create_all()

        #
        # import hashlib
        # u = User(name='Admin',
        #          username='admin',
        #          password=str(hashlib.md5('1234567'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.ADMIN)
        #
        # db.session.add(u)
        # db.session.commit()

        #
        # l1 = LoaiPhong(name='Phòng 1 giường')
        # l2 = LoaiPhong(name='Phòng 2 giường')
        #
        #
        # db.session.add(l1)
        # db.session.add(l2)
        # db.session.commit()
        #
        #
        # p1 = Phong(name='Phòng 1 giường đôi cao cấp', price=1300000,
        #             category_id=1,
        #              image="https://www.cet.edu.vn/wp-content/uploads/2018/01/cac-loai-giuong-trong-khach-san.jpg",
        #              acreage=20.2)
        # p2 = Phong(name='Phòng 2 giường ', price=2000000,
        #              category_id=2,
        #              image="https://noithatmyhouse.net/wp-content/uploads/2019/10/giuong-ngu-khach-san_11.jpg",
        #              acreage=27.0)
        # p3 = Phong(name='Phòng 1 giường đơn', price=850000,
        #              category_id=1,
        #              image="https://chefjob.vn/wp-content/uploads/2020/07/tieng-anh-loai-phong-khach-san.jpg",
        #              acreage=15.5)
        # p4 = Phong(name='Phòng 2 giường cao cấp ', price=2500000,
        #              category_id=2,
        #              image="https://decoxdesign.com/upload/images/hotel-caitilin-1952m2-phong-ngu-06-decox-design.jpg",
        #              acreage=25.2)
        # p5 = Phong(name='Phòng 1 giường đôi view biển', price=1500000,
        #              category_id=1,
        #              image="https://www.hoteljob.vn/files/Anh-HTJ-Hong/tieu-chi-can-co-trong-thiet-ke-phong-khach-san-1.jpg",
        #              acreage=12.5)
        # p6 = Phong(name='Phòng 1 giường đôi đầy đủ nội thất', price=1200000,
        #              category_id=1,
        #              image="https://tubepfurniture.com/wp-content/uploads/2020/09/phong-mau-khach-san-go-cong-nghiep-01.jpg",
        #              acreage=15.2)
        # p7 = Phong(name='Phòng 2 giường đơn', price=1300000,
        #              category_id=2,
        #              image="https://everon.com/upload_images/images/noi-that-phong-ngu-khach-san/phong-ngu-khach-san-2.jpg",
        #              acreage=20.2)
        # p8 = Phong(name='Phòng 2 giường đôi và đơn', price=1800000,
        #              category_id=2,
        #              image="https://www.hoteljob.vn/files/VB2-%E1%BA%A3nh%20HTJ/cac-loai-phong-trong-khach-san-2.jpg",
        #              acreage=23.2)
        #
        # db.session.add_all([p1,p2,p3,p4,p5,p6,p7,p8])
        # db.session.commit()
