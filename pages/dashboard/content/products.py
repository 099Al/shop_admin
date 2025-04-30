from database.requests.req_products import ReqProduct
from pages.dashboard.elements.category_elements import AddCategoryButton, el_category_header, CategoryRow
from pages.dashboard.elements.product_elements import el_products_header, ProductRow
from pages.dashboard.head_elements import header
from pages.style.style import inputBgErrorColor
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


        content_header = header(label_name="Список Продуктов", user_role=self.user_role)
        self.new_content.append(content_header)

        # resul append to body_content
        req = ReqProduct()
        max_length_product = max(req.get_max_length(), len("Наименование"))
        name_width = max(max_length_product * 9, 100)  # 7 letter size
        d_column_width = {"c_edit": 100,
                          "c_image": 100,
                          "c_name": name_width,
                          "с_item_no": 90,
                          "c_price": 80,
                          "c_desc": 150,
                          "c_price_promo": 80,
                          "c_promo_end": 50,
                          "c_promo_desc": 150
                          }
        l_controls = []

        # кнопка "Добавить новый продукт"  TODO
        # self.new_content.append(
        #     AddProductButton(page=self.page,
        #                       d_width=d_width,
        #                       error_message=error_message,
        #                       l_elements=l_controls,
        #                       # передается ссылка на список строк, чтобы к нему добавить новую категорию
        #                       )
        # )

        self.new_content.append(el_products_header(d_column_width))  # table header
        # ---rows---
        for product in req.get_all_products():
            l_controls.append(
                ProductRow(
                    page=self.page,
                    d_column_width=d_column_width,
                    d_error_messages={"error_pk_item_no": error_message_pk_item_no, "error_pk_name": error_message_pk_name, "validation_error": error_message_validation},
                    product=product,
                    #product_id=product.product_id,
                    # p_name=product.name,
                    # p_item_no=product.item_no,
                    # p_price=product.price,
                    # p_desc=product.description,
                    # p_promo_price=product.promo_price,
                    # p_promo_end=product.promo_expire_date,
                    # p_promo_desc=product.promo_desc,
                    # p_img=product.r_image,
                    l_elements=l_controls
                )

            )

        self.new_content.append(ft.Column(
            controls=l_controls,
            spacing=1,
            # height=600,     #scroll не будет работать, если изменить размер окна
            scroll=ft.ScrollMode.AUTO,
            expand=True
        ))
        # --rows-----------

        self.new_content.append(error_message_validation)
        self.new_content.append(error_message_pk_item_no)
        self.new_content.append(error_message_pk_name)

        return self.new_content