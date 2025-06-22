from database.requests.req_products import ReqProduct
from pages.config.errors import d_error_messages
from pages.config.sizes import d_product_column_size
from pages.dashboard.content.filter_header import GenericFilter
from pages.dashboard.content.header import GenericHeader
from pages.dashboard.content.products.add_product_button import AddProductButton
from pages.dashboard.content.products.product_elements import ProductRow
from pages.dashboard.head_elements import header
from datetime import date

import flet as ft


class ProductsContent:

    def __init__(self, instance):
        self.page = instance.page
        self.user_role = instance.user_role
        self.view_content = []

        self.field_definitions_filter = [
            ("image", False),
            ("name", True),
            ("item_no", True),
        ]

        #  ),
        #         el_divider,
        #         self._create_header_cell("Изображение", self.d_column_size["c_image"]),
        #         el_divider,
        #         sort_name.attribute_header_with_sort("Наименование", self.d_column_size["c_name"], str, 'p_name'),
        #         el_divider,
        #         sort_item_no.attribute_header_with_sort("Артикул", self.d_column_size["с_item_no"], str, 'p_item_no'),
        #         el_divider,
        #         sort_price.attribute_header_with_sort("Цена", self.d_column_size["c_price"], float, 'p_price'),
        #         el_divider,
        #         self._create_header_cell("Описание", self.d_column_size["c_desc"]),
        #         el_divider,
        #         self._create_header_cell("Цена по Акции", self.d_column_size["c_price_promo"]),
        #         el_divider,
        #         sort_promo.attribute_header_with_sort("Акция до", self.d_column_size["c_promo_end"], date, 'p_promo_end'),
        #         el_divider,
        #         self._create_header_cell("Акция Описание", self.d_column_size["c_promo_desc"]),
        #         el_divider,
                #self.header_category

        self.field_definitions_header = [
            {"label": "", "field_name": "edit", "sort_attr": None, "is_sortable": False, "type": None},
            {"label": "Изображение", "field_name": "image", "sort_attr": None, "is_sortable": False, "type": None},
            {"label": "Наименование", "field_name": "name", "sort_attr": "name", "is_sortable": True, "type": str},
            {"label": "Артикул", "field_name": "item_no", "sort_attr": "item_no", "is_sortable": True, "type": str},
            {"label": "Цена", "field_name": "price", "sort_attr": "price", "is_sortable": True, "type": float},
            {"label": "Описание", "field_name": "desc", "sort_attr": None, "is_sortable": False, "type": None},
            {"label": "Цена по\nАкции", "field_name": "promo_price", "sort_attr": "promo_price", "is_sortable": True, "type": float},
            {"label": "Акция до", "field_name": "promo_end", "sort_attr": "promo_end", "is_sortable": True, "type": date},
            {"label": "Акция Описание", "field_name": "promo_desc", "sort_attr": None, "is_sortable": False, "type": None},
        ]


    def build(self):
        self.column_with_product_rows = ft.Column(
            controls=[],
            spacing=1,
            # height=600,     #scroll не будет работать, если изменить размер окна
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        content_header = header(label_name="Список Продуктов", user_role=self.user_role)
        self.view_content.append(content_header)

        # resul append to body_content
        req = ReqProduct()
        max_length_product = max(req.get_max_length(), len("Наименование"))
        name_width = max(max_length_product * 9, 100)  # 7 letter size
        #d_column_width = d_product_column_size

        add_button = AddProductButton(
                                page=self.page,
                                column_with_rows=self.column_with_product_rows,
                                # передается ссылка на список строк, чтобы к нему добавить новую категорию
                                ).build()
        self.row_1 = ft.Row(
            controls=[add_button],
            alignment=ft.MainAxisAlignment.END,  #Приживается к правому краю. При изменении размеров окна - сдвигается соответственно
        )
        # кнопка "Добавить новый продукт"
        self.view_content.append(self.row_1)

        self.column_1 = ft.Column(
            controls=[
                GenericFilter(self.page, self.column_with_product_rows.controls, self.field_definitions_filter, d_product_column_size).build(),
                Product_Header(self.page, self.column_with_product_rows.controls).build(),
                GenericHeader(
                    self.page,
                    self.column_with_product_rows.controls,
                    self.field_definitions_header,
                    d_product_column_size,
                    default_sort_key='product_id',
                    sort_key_type=int,
                    sort_key_reverse=True
                ).build(),
                self.column_with_product_rows
            ],
            expand=True  #без expand scroll не работает
        )


        # ---rows--- заполнене списка продукатами
        for product in req.get_all_products():
            self.column_with_product_rows.controls.append(
                ProductRow(
                    page=self.page,
                    product=product,
                    column_with_rows=self.column_with_product_rows
                )

            )

        self.row_scroll = ft.Row(controls=[self.column_1],
                                 expand=True,                #без expand scroll не работает
                                 scroll=ft.ScrollMode.AUTO
                                 )

        self.view_content.append(self.row_scroll)

        # --rows-----------

        self.view_content.append(d_error_messages["validation_error"])
        self.view_content.append(d_error_messages["error_pk_item_no"])
        self.view_content.append(d_error_messages["error_pk_name"])
        self.view_content.append(d_error_messages["image_error"])
        self.view_content.append(d_error_messages["insert_error"])

        return self.view_content








