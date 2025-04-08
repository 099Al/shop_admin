from sqlalchemy import select, func, update, delete, insert

from database.connect import DataBase
from database.models.models import Category, Product, Category_Product


class ReqCategory:

    def __init__(self):
        #self.session = db.get_session()
        self.session = DataBase().get_session()

    def get_all_categories(self):
        result = self.session.execute(select(Category))
        return result.scalars().all()

    def get_max_length(self):
        max_length = self.session.query(func.max(func.length(Category.name))).scalar()
        return max_length

    def category_products_cnt(self):
        category_counts = (
            self.session.query(Category.id, Category.name, Category.order_number, func.count(Category_Product.product_fk).label("product_count"))
            .join(Category_Product, Category.id == Category_Product.category_fk, isouter=True)
            .group_by(Category.name)
            .all()
        )

        category_counts.sort(key=lambda x: x.order_number if x.order_number is not None else 0)

        return category_counts

    def update_category(self, name, new_name, order_num):
        try:
            if order_num.strip() == '':
                order_num = None
            self.session.execute(
                update(Category)
                .where(Category.name == name)
                .values(name=new_name, order_number=order_num)
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

    def delete_category_cascade(self, category_id: int):
        stmt = select(Category_Product.product_fk).join(Category).where(
                Category.id == category_id
            )
        product_ids = (self.session.execute(stmt)).scalars().all()

        for product_id in product_ids:
                # Check if the product exists in other categories
            other_categories_stmt = select(Category_Product).join(Category).where(
                    Category_Product.product_fk == product_id,
                    Category.id != category_id  # Ensure it's in a different category
                )
            other_categories = (self.session.execute(other_categories_stmt)).first()

            if not other_categories:
                    # Product exists only in this category; delete it
                self.session.execute(
                        delete(Product).where(Product.product_id == product_id)
                    )

                self.session.execute(
                        delete(Category_Product).where(Category_Product.product_fk == product_id, Category_Product.category_fk == category_id)
                    )

        # Delete the category
        self.session.execute(
                        delete(Category).where(Category.id == category_id)
                    )
        self.session.execute(
                delete(Category_Product).where(Category_Product.category_fk == category_id)
            )
        self.session.commit()

    def new_category(self, category_name, category_order=None):
        try:
            result = self.session.execute(
                insert(Category)
                .values(name=category_name, order_number=category_order)
            )
            self.session.commit()

            id = result.inserted_primary_key[0]

            return id
        except Exception as e:
            self.session.rollback()
            return None