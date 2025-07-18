from database.models.models import Product
from database.requests.req_products import ReqProduct
from pages.config.errors import d_error_messages
from pages.config.sizes import d_product_column_size
from pages.dashboard.content.products.validation import is_valid_price, is_valid_date, cut_price
from pages.dashboard.content.products.product_elements import ProductRow
import flet as ft



class AddProductButton:
    def __init__(self, page, column_with_rows, **kwargs):
        self.page = page
        self.column_with_rows = column_with_rows
        #self.d_column_size = d_product_column_size
        self.d_error_messages = d_error_messages

    def build(self):
        return ft.Container(
                    content=ft.ElevatedButton("Добавить продукт",
                                              icon=ft.icons.ADD,
                                              on_click=self.add_product2),
                    margin=ft.margin.only(right=30, top=40),
                    #width=250,

                )

    def add_product2(self, e):
        new_product = Product(
            product_id=None,
            name=None,
            item_no=None,
            price=None,
            description=None,
            promo_price=None,
            promo_expire_date=None,
            promo_desc=None
        )

        new_product_row = ProductRow(
            page=self.page,
            product=new_product,
            column_with_rows=self.column_with_rows

        )

        self.column_with_rows.controls.insert(0, new_product_row)

        self.page.update()



    def add_product(self, e):
        def add_product_handle_yes(e):
            req = ReqProduct()
            product_name = dlg_create.content.content.controls[0].value
            product_item_no = dlg_create.content.content.controls[1].value
            product_price = dlg_create.content.content.controls[2].value
            product_desc = dlg_create.content.content.controls[3].value
            product_prome_price = dlg_create.content.content.controls[4].value
            product_prome_end = dlg_create.content.content.controls[5].value
            product_prome_desc = dlg_create.content.content.controls[6].value

            product_price = cut_price(product_price)
            product_prome_price = cut_price(product_prome_price)



            flag_valid = True

            if not is_valid_price(product_price):
                product_price = None
                flag_valid = False
            else:
                product_price = float(product_price)


            if not is_valid_price(product_prome_price):
                product_prome_price = None
            else:
                product_prome_price = float(product_prome_price)

            valid_date = is_valid_date(product_prome_end)
            if valid_date:
                product_prome_end = valid_date
            else:
                product_prome_end = None




            if not flag_valid:
                error_validation = self.d_error_messages["validation_error"]
                error_validation.open = True
                error_validation.update()
            else:

                is_exists_product = req.check_product_exists(product_name, product_item_no, None)
                if is_exists_product:
                    if is_exists_product == 1:
                        error_validation = self.d_error_messages["error_pk_item_no"]
                    else:
                        error_validation = self.d_error_messages["error_pk_name"]
                    error_validation.open = True
                    error_validation.update()
                else:

                    new_product = Product(
                        name=product_name,
                        item_no=product_item_no,
                        price=product_price,
                        description=product_desc,
                        promo_price=product_prome_price,
                        promo_expire_date=product_prome_end,
                        promo_desc=product_prome_desc
                    )

                    new_product_id = req.add_product(new_product)

                    if new_product_id is None:
                        error_validation = self.d_error_messages["insert_error"]
                        error_validation.open = True
                        error_validation.update()
                        return
                    else:
                        new_row = ProductRow(
                                page=self.page,
                                product=new_product,
                                column_with_rows=self.column_with_rows
                        )

                        self.column_with_rows.controls.append(new_row)

                        dlg_create.open = False
                        self.page.update()

        def add_product_handle_close(e):
            dlg_create.open = False
            self.page.update()

        dlg_create = ft.AlertDialog(
            modal=True,
            title=ft.Text("Новый продукт"),
            content=ft.Container(
                height=320,
                content=ft.Column(
                    controls=[
                        ft.TextField(label="Название", height=40, read_only=False, text_size=15),
                        ft.TextField(label="Артикул", height=40, read_only=False, text_size=15),
                        ft.TextField(label="Цена", height=40, read_only=False, text_size=15),
                        ft.TextField(label="Описание", height=40, read_only=False, text_size=15),
                        ft.TextField(label="Цена акции", height=40, read_only=False, text_size=15),
                        ft.TextField(label="Дата окончания акции", height=40, read_only=False, text_size=15),
                        ft.TextField(label="Описание акции", height=40, read_only=False, text_size=15),
                    ]
                )
            ),
            actions=[
                ft.TextButton("Yes", on_click=add_product_handle_yes),
                ft.TextButton("No", on_click=add_product_handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            # on_dismiss=lambda e: self.page.add(ft.Text("Modal dialog dismissed"),),
        )

        self.page.open(dlg_create)
        # dlg_create.open = True
        self.page.update()