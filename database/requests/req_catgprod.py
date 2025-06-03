from sqlalchemy import select, func, update, delete, insert

from database.connect import DataBase
from database.models.models import Category, Product, ImagePhoto, Category_Product


class ReqCategory:

    def __init__(self):
        #self.session = db.get_session()
        self.session = DataBase().get_session()

    def get_all_categories(self):
        result = self.session.execute(select(Category))
        return result.scalars().all()

class ReqCategoryProduct:

    def __init__(self):
        self.session = DataBase().get_session()

    def get_all_categories_and_products(self):
        stmt = (
            select(
                Category.id,
                Category.name.label("category_name"),
                Product.product_id,
                Product.name,
                Product.item_no,
                ImagePhoto.image_name
            )
            .select_from(Product)
            .outerjoin(Product.r_categories)
            .outerjoin(Product.r_image)
            .order_by(Category.id, Product.product_id)
        )

        result = self.session.execute(stmt)
        return result.fetchall()


    def update_category_product(self, old_category_id, new_category_id, product_id):
        try:
            self.session.execute(
                update(Category_Product)
                .where((Category_Product.product_fk == product_id) & (Category_Product.category_fk == old_category_id))
                .values(category_fk=new_category_id)
            )
            self.session.commit()

            return True
        except Exception as e:
            self.session.rollback()
            return None

    def add_category_product(self, category_id, product_id):
        try:
            result = self.session.execute(
                insert(Category_Product)
                .values(category_fk=category_id, product_fk=product_id)
            )
            self.session.commit()

            id = result.inserted_primary_key[0]

            return id
        except Exception as e:
            self.session.rollback()
            return None

    def check_if_prodict_exist_in_category(self, category_id, product_id):
        stmt = select(Category_Product).where((Category_Product.product_fk == product_id) & (Category_Product.category_fk == category_id))
        result = self.session.execute(stmt)
        if result.scalar():
            return True
        else:
            return False

    def delete_category_product(self, category_id, product_id):
        try:
            self.session.execute(
                delete(Category_Product).where((Category_Product.product_fk == product_id) & (Category_Product.category_fk == category_id))
            )
            self.session.commit()

            return True
        except Exception as e:
            self.session.rollback()
            return None