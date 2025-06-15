from database.requests.req_products import ReqProduct
from pages.config.errors import d_error_messages
from pages.config.sizes import d_product_column_size
from pages.dashboard.content.products.add_product_button import AddProductButton
from pages.dashboard.content.products.product_elements import ProductRow, Product_Header
from pages.dashboard.content.products.product_filter import Product_Filter
from pages.dashboard.head_elements import header

import flet as ft


class ProductsContent:

    def __init__(self, instance):
        self.page = instance.page
        self.user_role = instance.user_role
        self.view_content = []

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
                Product_Filter(self.page, self.column_with_product_rows.controls).build(),
                Product_Header(self.page, self.column_with_product_rows.controls).build(),
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








