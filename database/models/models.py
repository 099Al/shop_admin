from sqlalchemy import String, Integer, ForeignKey, Float, Date, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from database.models.base import Base


class Admin(Base):
    __tablename__ = 'admins'

    telegram_id: Mapped[str] = mapped_column(String(30), primary_key=True)
    telegram_name: Mapped[str] = mapped_column(String(50), nullable=True)
    telegram_link: Mapped[str] = mapped_column(String(100), nullable=True)
    name:  Mapped[str] = mapped_column(String(25), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(20), nullable=True)
    role: Mapped[str]  # = mapped_column(String(20), nullable=False)
    login: Mapped[str] = mapped_column(String(100), nullable=True)
    password: Mapped[str] = mapped_column(String(100), nullable=True)

class Category_Product(Base):
    __tablename__ = 'a_category_product'

    category_fk: Mapped[int] = mapped_column(ForeignKey('categories.id'), primary_key=True)
    product_fk: Mapped[int] = mapped_column(ForeignKey('products.product_id'), primary_key=True)

class Category(Base):
    __tablename__ = 'categories'
    """
        В таблице должна быть default категория
        Для случая если хотим отображать товары без категорий
        Товары из нее отображаются, если она одна, в ддругих случаях не выводятся.
        Сама категория для пользователя не выводится, только для администратора
        """
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(25), unique=True)
    order_number: Mapped[int] = mapped_column(Integer, nullable=True)
    r_products: Mapped[List['Product']] = relationship(secondary=Category_Product.__tablename__, back_populates='r_categories', lazy="selectin")

class Product(Base):
    __tablename__ = 'products'
    """
        У продукта всегда должна быть категория
    """
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name:  Mapped[str] = mapped_column(String(25))
    item_no: Mapped[str] = mapped_column(String(100), nullable=True) # артикул

    description: Mapped[str] = mapped_column(String(300), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=True)
    status_product: Mapped[int] = mapped_column(Integer, nullable=True)
    image_id: Mapped[int] = mapped_column(Integer, ForeignKey('images.image_id', ondelete='SET NULL'),nullable=True)
    promo_desc: Mapped[str] = mapped_column(String(30), nullable=True)
    promo_price: Mapped[float] = mapped_column(Float, nullable=True)
    promo_expire_date: Mapped[Date] = mapped_column(Date, nullable=True)

    r_image: Mapped['ImagePhoto'] = relationship(back_populates='r_product', uselist=False, lazy="selectin")
    r_categories: Mapped[List['Category']] = relationship(secondary=Category_Product.__tablename__, back_populates='r_products')

    def __repr__(self):
        return (f'{self.__class__.__name__} (id={self.product_id}, nm={self.name}, im_id={self.image_id}, {self.price})')


class ImagePhoto(Base):
    __tablename__ = 'images'
    image_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image_name: Mapped[str] = mapped_column(String(500), nullable=True)
    # img_format: Mapped[ImageFormat]
    img_format: Mapped[str]
    info: Mapped[str] = mapped_column(String(500), nullable=True)
    caption: Mapped[str] = mapped_column(String(500), nullable=True)
    id_1: Mapped[str] = mapped_column(String(100), nullable=True)
    id_2: Mapped[str] = mapped_column(String(100), nullable=True)
    id_3: Mapped[str] = mapped_column(String(100), nullable=True)
    id_4: Mapped[str] = mapped_column(String(100), nullable=True)
    sq_id_1: Mapped[str] = mapped_column(String(100), nullable=True)
    sq_id_2: Mapped[str] = mapped_column(String(100), nullable=True)
    sq_id_3: Mapped[str] = mapped_column(String(100), nullable=True)
    sq_id_4: Mapped[str] = mapped_column(String(100), nullable=True)

    __table_args__ = (
        CheckConstraint("img_format IN ('squared', 'horizontal', 'vertical')",
                        name='check_formats'),
    )

    r_product: Mapped['Product'] = relationship(back_populates='r_image', uselist=False)

    def __repr__(self):
        return f'ImagePhoto(id={self.image_id}, name={self.image_name}, format={self.img_format})'