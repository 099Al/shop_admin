from sqlalchemy import select, func, update, delete, insert

from database.connect import DataBase
from database.models.models import Category, Product, Category_Product, ImagePhoto
import utils.functions as ut

class ReqProduct:
    def __init__(self) -> None:
        self.session = DataBase().get_session()

    def get_all_products(self):
        stmt = select(Product).order_by(Product.product_id)
        return self.session.execute(stmt).scalars().all()

    def get_product_by_category(self, category_id):
        stmt = select(Product).join(Category_Product).where(Category_Product.category_fk == category_id).order_by(Product.product_id)
        return self.session.execute(stmt).scalars().all()

    def get_max_length(self):
        max_length = self.session.query(func.max(func.length(Product.name))).scalar()
        return max_length


    def delete_product(self, product_id):
        self.session.execute(
            delete(Product).where(Product.product_id == product_id)
        )

        self.session.execute(
            delete(Category_Product).where(Category_Product.product_fk == product_id)
        )

        self.session.commit()



    def check_product_exists(self, name, item_no, product_id):
        """
        Функция отлияается от проекта shop.
        Смотрим по всей базе, не зависимо от категории
        Если есть артикул, он должен быть уникальным
        Если его нет, то название должно быть уникальным
        """
        query = (
            select(Product).filter_by(item_no=item_no)
            if item_no
            else select(Product).where((Product.name == name) & (Product.item_no.is_(None)))
        )

        products = self.session.execute(query).scalars().all()
        l_products_ids = [p.product_id for p in products if product_id != p.product_id]

        if l_products_ids:
            return 1 if item_no else 2
        else:
            return False


    def check_product_by_name_item_num(self, name, item_num):
        product = self.session.execute(
                select(Product).where((Product.name == name) & (Product.item_no == item_num))
            )
        if product.scalars().first():
            return True
        else:
            return False




    def update_product(self, product_id, **kwargs):
        try:
            self.session.execute(
                update(Product).where(Product.product_id == product_id).values(**kwargs)
            )
            self.session.commit()

            return True
        except Exception as e:
            self.session.rollback()
            return None

    def update_image(self, product_id, image_name):
        try:
            image_name_old = self.session.execute(
                select(ImagePhoto.image_name).where(ImagePhoto.image_id == select(Product.image_id).where(
                    Product.product_id == product_id).scalar_subquery()
                )
            ).scalars().first()

            if image_name_old:
                self.session.execute(
                    update(ImagePhoto)
                    .where(ImagePhoto.image_id == select(Product.image_id).where(
                        Product.product_id == product_id).scalar_subquery())
                    .values(image_name=image_name)
                )
            else:
                image = ImagePhoto(image_name=image_name)  # Новое изображение, т.к. новый продукт
                self.session.add(image)
                self.session.flush()

                image_id = image.image_id

                self.session.execute(
                    update(Product).where(Product.product_id == product_id).values(image_id=image_id)
                )

            self.session.commit()


            return image_name_old, 1  #картинки могло не быть

        except Exception as e:
            self.session.rollback()
            return None, None


    def delete_image(self, product_id):
        try:
            image_name = self.session.execute(
                select(ImagePhoto.image_name).where(ImagePhoto.image_id == select(Product.image_id).where(
                    Product.product_id == product_id).scalar_subquery()
                )
            ).scalars().first()

            self.session.execute(
                delete(ImagePhoto).where(ImagePhoto.image_id == select(Product.image_id).where(
                    Product.product_id == product_id).scalar_subquery()
                )
            )

            self.session.execute(
                update(Product).where(Product.product_id == product_id).values(image_id=None)
            )

            self.session.commit()

            return image_name, 1  #картинки могло не быть

        except Exception as e:
            self.session.rollback()
            return None, None