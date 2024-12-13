from sqlalchemy import select, func, update, delete

from database.connect import DataBase
from database.models.models import Category, Product


class ReqCategory:

    def __init__(self, db: DataBase):
        self.session = db.get_session()

    def get_all_categories(self):
        result = self.session.execute(select(Category))
        return result.scalars().all()

    def get_max_length(self):
        max_length = self.session.query(func.max(func.length(Category.name))).scalar()
        return max_length

    def category__products_cnt(self):
        category_counts = (
            self.session.query(Category.id, Category.name, func.count(Product.product_id).label("product_count"))
            .join(Product, Category.id == Product.category_id, isouter=True)
            .group_by(Category.name)
            .all()
        )
        return category_counts

    def update_category(self, name, new_name):
        self.session.execute(
            update(Category)
            .where(Category.name == name)
            .values(name=new_name)
        )
        self.session.commit()

    def delete_category(self, category_id):
        self.session.execute(
            delete(Category)
            .where(Category.id == category_id)
        )
        self.session.commit()