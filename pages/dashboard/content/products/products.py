from database.requests.req_products import ReqProduct
from pages.config.sizes import d_product_column_size
from pages.dashboard.content.products.add_product_button import AddProductButton
from pages.dashboard.content.products.product_elements import ProductRow, Product_Header
from pages.dashboard.content.products.product_filter import Product_Filter
from pages.dashboard.head_elements import header
from pages.config.style import inputBgErrorColor
import flet as ft


class ProductsContent:

    def __init__(self, instance):
        self.page = instance.page
        self.user_role = instance.user_role
        self.view_content = []



    def build(self):
        error_message_pk_name = ft.SnackBar(
            content=ft.Text('Продукт с таким названием уже существует'),
            bgcolor=inputBgErrorColor
        )

        error_message_pk_item_no = ft.SnackBar(
            content=ft.Text('Продукт с таким артикулом уже существует'),
            bgcolor=inputBgErrorColor
        )

        error_message_validation = ft.SnackBar(
            content=ft.Text('Неверный формат данных'),
            bgcolor=inputBgErrorColor
        )

        error_message_image = ft.SnackBar(
            content=ft.Text('Неверный формат изображения'),
            bgcolor=inputBgErrorColor
        )

        error_insert_product = ft.SnackBar(
            content=ft.Text('Ошибка при добавлении в базу данных'),
            bgcolor=inputBgErrorColor
        )


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
        d_column_width = d_product_column_size


        # кнопка "Добавить новый продукт"
        self.view_content.append(
            AddProductButton(page=self.page,
                              d_column_width=d_column_width,
                              d_error_messages={"error_pk_item_no": error_message_pk_item_no,
                                               "error_pk_name": error_message_pk_name,
                                               "validation_error": error_message_validation,
                                               "image_error": error_message_image,
                                               "insert_error": error_insert_product

                                                },
                              column_with_rows=self.column_with_product_rows,
                              # передается ссылка на список строк, чтобы к нему добавить новую категорию
                              ).build()
        )

        self.column_1 = ft.Column(
            controls=[
                Product_Filter(self.page, self.column_with_product_rows.controls, d_column_width).build(),
                Product_Header(self.page, self.column_with_product_rows.controls).build(d_column_width),
                self.column_with_product_rows
            ],
            expand=True  #без expand scroll не работает
        )


        # ---rows--- заполнене списка продукатами
        for product in req.get_all_products():
            self.column_with_product_rows.controls.append(
                ProductRow(
                    page=self.page,
                    d_column_width=d_column_width,
                    d_error_messages={"error_pk_item_no": error_message_pk_item_no,
                                      "error_pk_name": error_message_pk_name,
                                      "validation_error": error_message_validation,
                                      "image_error": error_message_image},
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

        self.view_content.append(error_message_validation)
        self.view_content.append(error_message_pk_item_no)
        self.view_content.append(error_message_pk_name)
        self.view_content.append(error_message_image)
        self.view_content.append(error_insert_product)

        return self.view_content








