from sqlalchemy import select, func, update, delete, insert

from database.connect import DataBase
from database.models.models import Category, Product, Category_Product


class ReqProduct:
    def __init__(self, db: DataBase) -> None:
        self.session = db.session

    def get_all_products(self):
        stmt = select(Product).order_by(Product.product_id)
        return self.session.execute(stmt).scalars().all()

    def get_product_by_category(self, category_id):
        stmt = select(Product).join(Category_Product).where(Category_Product.category_fk == category_id).order_by(Product.product_id)
        return self.session.execute(stmt).scalars().all()

    def delete_product(self, product_id):
        self.session.execute(
            delete(Product).where(Product.product_id == product_id)
        )
        self.session.commit()

    def update_product(self, product_id, **kwargs):
        self.session.execute(
            update(Product).where(Product.product_id == product_id).values(**kwargs)
        )
        self.session.commit()

