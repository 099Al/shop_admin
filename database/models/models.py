from sqlalchemy import String, Integer, ForeignKey, Float, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from database.models.base import Base


class Admin(Base):
    __tablename__ = 'admins'

    telegram_id: Mapped[str] = mapped_column(String(30), primary_key=True)
    telegram_name: Mapped[str] = mapped_column(String(50), nullable=True)
    role: Mapped[str] #= mapped_column(String(20), nullable=False)
    name:  Mapped[str] = mapped_column(String(25), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(20), nullable=True)
    login: Mapped[str] = mapped_column(String(100), nullable=True)
    password: Mapped[str] = mapped_column(String(100), nullable=True)

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(25), unique=True)
    r_products: Mapped[List['Product']] = relationship(back_populates='r_categories', uselist=True)

class Product(Base):
    __tablename__ = 'products'

    product_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name:  Mapped[str] = mapped_column(String(25))
    item_no: Mapped[str] = mapped_column(String(100), nullable=True) # артикул
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    r_categories: Mapped['Category'] = relationship(back_populates='r_products', uselist=False)
    description: Mapped[str] = mapped_column(String(300), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=True)
    status_product: Mapped[int] = mapped_column(Integer, nullable=True)
    image_id: Mapped[int] = mapped_column(Integer, ForeignKey('images.image_id', ondelete='SET NULL'),nullable=True)
    promo_desc: Mapped[str] = mapped_column(String(30), nullable=True)
    promo_price: Mapped[float] = mapped_column(Float, nullable=True)
    promo_expire_date: Mapped[Date] = mapped_column(Date, nullable=True)

    #r_image: Mapped['ImagePhoto'] = relationship(back_populates='r_product', uselist=False, lazy="selectin")
