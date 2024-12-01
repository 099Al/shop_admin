from sqlalchemy import String
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
    #r_products: Mapped[List['Product']] = relationship(back_populates='r_categories', uselist=True)

