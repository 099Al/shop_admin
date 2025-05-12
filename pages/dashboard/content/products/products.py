from database.requests.req_products import ReqProduct
from pages.dashboard.content.products.add_product_button import AddProductButton
from pages.dashboard.content.products.product_elements import ProductRow, Product_Header
from pages.dashboard.head_elements import header
from pages.config.style import inputBgErrorColor
import flet as ft


class ProductsContent:

    def __init__(self, instance):
        self.page = instance.page
        self.user_role = instance.user_role
        self.new_content = []



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
        self.new_content.append(content_header)

        # resul append to body_content
        req = ReqProduct()
        max_length_product = max(req.get_max_length(), len("Наименование"))
        name_width = max(max_length_product * 9, 100)  # 7 letter size
        d_column_width = {"c_edit": 100,
                          "c_image": 100,
                          "c_name": 150,
                          "с_item_no": 90,
                          "c_price": 80,
                          "c_desc": 150,
                          "c_price_promo": 80,
                          "c_promo_end": 80,
                          "c_promo_desc": 150
                          }


        # кнопка "Добавить новый продукт"
        self.new_content.append(
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

        self.new_content.append(Product_Header(self.page, self.column_with_product_rows.controls).el_products_header(d_column_width))  # table header
        # ---rows---
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



        self.new_content.append(self.column_with_product_rows)
        # --rows-----------

        self.new_content.append(error_message_validation)
        self.new_content.append(error_message_pk_item_no)
        self.new_content.append(error_message_pk_name)
        self.new_content.append(error_message_image)
        self.new_content.append(error_insert_product)

        return self.new_content








