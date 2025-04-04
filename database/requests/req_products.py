from sqlalchemy import select, func, update, delete, insert

from database.connect import DataBase
from database.models.models import Category, Product, Category_Product


class ReqCategory:

    def __init__(self, db: DataBase):
        self.session = db.get_session()

    def get_all_categories(self):
        result = self.session.execute(select(Category))
        return result.scalars().all()

    def get_max_length(self):
        max_length = self.session.query(func.max(func.length(Category.name))).scalar()
        return max_length

    def category_products_cnt(self):
        category_counts = (
            self.session.query(Category.id, Category.name, func.count(Category_Product.product_fk).label("product_count"))
            .join(Category_Product, Category.id == Category_Product.category_fk, isouter=True)
            .group_by(Category.name)
            .all()
        )
        return category_counts

    def update_category(self, name, new_name):
        try:
            self.session.execute(
                update(Category)
                .where(Category.name == name)
                .values(name=new_name)
            )
            self.session.commit()
            return 1
        except Exception as e:
            self.session.rollback()
            return None

    def delete_category(self, category_id):
        self.session.execute(
            delete(Category)
            .where(Category.id == category_id)
        )
        self.session.commit()

    def new_category(self, category_name):
        try:
            result = self.session.execute(
                insert(Category)
                .values(name=category_name)
            )
            self.session.commit()

            id = result.inserted_primary_key[0]

            return id
        except Exception as e:
            self.session.rollback()
            return None