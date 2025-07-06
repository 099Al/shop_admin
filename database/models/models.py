from sqlalchemy import String, Integer, ForeignKey, Float, Date, CheckConstraint, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Text
import enum
from database.models.base import Base


class AdminRoles(enum.Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    READ = "read"
    NO_ROLE = "no_role"

class ClientsBan(enum.Enum):
    BANNED = 1
    NOT_BANNED = 0

class Admin(Base):
    __tablename__ = 'admins'

    telegram_id: Mapped[str] = mapped_column(String(30), primary_key=True)
    telegram_name: Mapped[str] = mapped_column(String(50), nullable=True)
    telegram_link: Mapped[str] = mapped_column(String(100), nullable=True)
    name:  Mapped[str] = mapped_column(String(25), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(20), nullable=True)
    role: Mapped[str]  # = mapped_column(String(20), nullable=False)   #todo Роли должны задаваться через Enum
    # role: Mapped[AdminRoles] = mapped_column(SQLEnum(AdminRoles), name="role", native_enum=False, values_callable=lambda x: [e.value for e in AdminRoles])
    login: Mapped[str] = mapped_column(String(100), nullable=True)
    password: Mapped[str] = mapped_column(String(100), nullable=True)

    def __repr__(self):
        return (f'{self.__class__.__name__} (id={self.telegram_id}, name={self.name}, role={self.role})')


class Client(Base):
    __tablename__ = 'users'
    __table_args__ = (
        CheckConstraint("is_banned IN (0, 1)", name="chk_client_is_banned"),
    )

    telegram_id: Mapped[str] = mapped_column(String(30), primary_key=True)
    telegram_name: Mapped[str] = mapped_column(String(50), nullable=True)
    telegram_link: Mapped[str] = mapped_column(String(100), nullable=True)
    name:  Mapped[str] = mapped_column(String(25), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(20), nullable=True)
    type: Mapped[str] = mapped_column(String(20), nullable=True)
    # is_banned: Mapped[int]
    is_banned: Mapped[int] = mapped_column(Integer, nullable=False, default=ClientsBan.NOT_BANNED.value)
    ban_reason: Mapped[str]

    def __repr__(self):
        return (f'{self.__class__.__name__} (id={self.telegram_id}, telegram_name={self.telegram_name}, name={self.name})')



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

    def __repr__(self):
        return (f'{self.__class__.__name__} (id={self.id}, nm={self.name})')

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


class OrderSatus(enum.Enum):
    NEW = "новый"
    IN_PROCESS = "в работе"
    REJECTED = "отменен"
    DONE = "доставлен"


class Order(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        CheckConstraint("satus IN ('новый', 'в работе', 'не оплачен', 'отменен', 'доставлен')", name="chk_satus"),
        CheckConstraint("payment_status IN ('при получении', 'оплачен')", name="chk_payment_status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_tg_id: Mapped[str] = mapped_column(String(30), nullable=False)
    order_sum: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(Integer)
    payment_status: Mapped[str] = mapped_column(String(100))
    delivery_address: Mapped[str] = mapped_column(String(1000))
    created_at: Mapped[Date] = mapped_column(String(100), nullable=False)
    comment: Mapped[str] = mapped_column(String(2000))
    order_products: Mapped[str] = mapped_column(String)

