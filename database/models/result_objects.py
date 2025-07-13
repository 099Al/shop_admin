import os

from config import settings



class CategoryProducts:
    def __init__(self, category_id, category_name, product_id, name, item_no, image_name, **kwargs):
        self.product_id: int = product_id
        self.category_id: int = category_id
        self.category_name: str = category_name
        self.name: str = name
        self.item_no: str = item_no
        self.image_name: str = image_name if image_name else None

        if not os.path.isfile(f"{settings.MEDIA}/original/{self.image_name}.jpeg"):
            self.image_name = None

        self.image_path: str = f"{settings.MEDIA}/original/{self.image_name}.jpeg" if self.image_name else f"{settings.MEDIA}/default/no_product_photo.jpeg"

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'CategoryProducts(product_id={self.product_id}, category_id={self.category_id}, name={self.name}, item_no={self.item_no}, image_name={self.image_name})'

