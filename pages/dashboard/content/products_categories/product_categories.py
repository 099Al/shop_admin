from database.models.models import Category
from database.models.result_objects import CategoryProducts
from database.requests.req_categories import ReqCategory
from database.requests.req_catgprod import ReqCategoryProduct
from pages.config.errors import d_error_messages_ctg_prod
from pages.config.sizes import d_category_product_column_size
from pages.dashboard.content.filter_header import GenericFilter
from pages.dashboard.content.header import GenericHeader

from pages.dashboard.content.products_categories.product_categories_elements import CategoryProductsRow

from pages.dashboard.head_elements import header

import flet as ft


class ProductsAndCategoriesContent:

    def __init__(self, instance):
        self.page = instance.page
        self.user_role = instance.user_role
        self.view_content = []

        self.field_definitions_filter = [
            ("category_name", True),
            ("item_no", True),
            ("name", True),
        ]

        self.field_definitions_header = [
            {"label": "", "field_name": "edit", "sort_attr": None, "is_sortable": False, "type": None},
            {"label": "Категория", "field_name": "category_name", "sort_attr": "category_name", "is_sortable": True, "type": str},
            {"label": "Артикул", "field_name": "item_no", "sort_attr": "item_no", "is_sortable": True, "type": str},
            {"label": "Продукт", "field_name": "name", "sort_attr": "name", "is_sortable": True, "type": str},
            {"label": "Фото", "field_name": "image", "sort_attr": None, "is_sortable": False, "type": None},
            {"label": "Удалить/Добавить", "field_name": "dell_add", "sort_attr": None, "is_sortable": False, "type": None, "right_devider": False},
        ]

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

        self.row_1 = ft.Row(controls=[ft.Container(margin=36)])
        self.view_content.append(self.row_1)

        req = ReqCategoryProduct()
        req_ctg = ReqCategory()
        res: list[Category] = req_ctg.get_all_categories()


        self.column_1 = ft.Column(
            controls=[
                GenericFilter(self.page, self.column_with_rows_elements.controls, self.field_definitions_filter, d_category_product_column_size).build(),
                GenericHeader(
                    self.page,
                    self.column_with_rows_elements.controls,
                    self.field_definitions_header,
                    d_category_product_column_size,
                    'product_id',
                    int,
                    False
                ).build(),
                self.column_with_rows_elements
            ],
            expand=True
        )

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

        #Горизонтальная прокрутка
        self.row_scroll = ft.Row(controls=[self.column_1],
                                 expand=True,  # без expand scroll не работает
                                 scroll=ft.ScrollMode.AUTO
                                 )

        self.view_content.append(self.row_scroll)


        self.view_content.append(d_error_messages_ctg_prod)



        return self.view_content