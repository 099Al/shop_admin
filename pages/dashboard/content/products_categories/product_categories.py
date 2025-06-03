from database.models.models import Category
from database.models.result_objects import CategoryProducts
from database.requests.req_categories import ReqCategory
from database.requests.req_catgprod import ReqCategoryProduct
from database.requests.req_products import ReqProduct
from pages.config.errors import d_error_messages, d_error_messages_ctg_prod
from pages.config.sizes import d_product_column_size
from pages.dashboard.content.products.add_product_button import AddProductButton
from pages.dashboard.content.products.product_elements import ProductRow, Product_Header
from pages.dashboard.content.products.product_filter import Product_Filter
from pages.dashboard.content.products_categories.product_categories_elements import CategoryProductsRow
from pages.dashboard.head_elements import header
from pages.config.style import inputBgErrorColor
import flet as ft


class ProductsAndCategoriesContent:

    def __init__(self, instance):
        self.page = instance.page
        self.user_role = instance.user_role
        self.view_content = []

    def build(self):
        self.column_with_rows_elements = ft.Column(
            controls=[],
            spacing=1,
            # height=600,     #scroll не будет работать, если изменить размер окна
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        content_header = header(label_name="Продукты в категориях", user_role=self.user_role)
        self.view_content.append(content_header)

        req = ReqCategoryProduct()
        req_ctg = ReqCategory()
        res: list[Category] = req_ctg.get_all_categories()

        self.d_categories = {category.id: category.name for category in res}

        self.l_categories = []

        for ctg_id, ctg_name in self.d_categories.items():
            self.l_categories.append(ft.DropdownOption(key=str(ctg_id), text=str(ctg_name)))

        for element in req.get_all_categories_and_products():
            element_p_c = CategoryProducts(category_name=element.category_name,
                                           category_id=element.id,
                                           product_id=element.product_id,
                                           name=element.name,
                                           item_no=element.item_no,
                                           image_name=element.image_name
                                           )

            self.column_with_rows_elements.controls.append(
                CategoryProductsRow(
                    page=self.page,
                    element=element_p_c,
                    column_with_rows=self.column_with_rows_elements,
                    d_categories=self.d_categories,
                    l_categories=self.l_categories
                )

            )

        self.view_content.append(self.column_with_rows_elements)


        self.view_content.append(d_error_messages_ctg_prod)



        return self.view_content