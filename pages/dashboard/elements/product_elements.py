from datetime import datetime

import flet as ft
from flet_core.icons import MEDIATION

from database.models.models import Product
from database.requests.req_products import ReqProduct
from pages.style.style import *
from config import settings

el_divider = ft.Container(
                height=25,
                width=1,
                bgcolor="white",
                margin=0,
                padding=0
            )


def el_products_header(d_width):
    return ft.Row(
        controls=[
            ft.Container(
                width=d_width["c1"],
            ),
            el_divider,
            ft.Container(
                content=ft.Text(
                    "Изображение",
                    color=defaultFontColor,
                    size=15,
                    font_family="cupurum",
                ),
                width=d_width["c2"],
                alignment=ft.alignment.bottom_left,
            ),
            el_divider,
            ft.Container(
                content=ft.Text(
                    "Наименование",
                    color=defaultFontColor,
                    size=15,
                    font_family="cupurum",
                ),
                width=d_width["c2"],
                alignment=ft.alignment.bottom_left,
            ),
            el_divider,
            ft.Container(
                content=ft.Text(
                    "Артикул",
                    color=defaultFontColor,
                    size=15,
                    font_family="cupurum",
                ),
                width=d_width["c3"],
            ),
            el_divider,
            ft.Container(
                content=ft.Text(
                    "Цена",
                    color=defaultFontColor,
                    size=15,
                    font_family="cupurum",
                ),
                width=d_width["c4"],
            ),
            el_divider,
            ft.Container(
                content=ft.Text(
                    "Описание",
                    color=defaultFontColor,
                    size=15,
                    font_family="cupurum",
                ),
                width=d_width["c4"],
            ),
            el_divider,
            ft.Container(
                content=ft.Text(
                    "Цена по Акции",
                    color=defaultFontColor,
                    size=15,
                    font_family="cupurum",
                ),
                width=d_width["c4"],
            ),
            el_divider,
            ft.Container(
                content=ft.Text(
                    "Акция до",
                    color=defaultFontColor,
                    size=15,
                    font_family="cupurum",
                ),
                width=d_width["c4"],
            ),
            el_divider,
            ft.Container(
                content=ft.Text(
                    "Акция Описание",
                    color=defaultFontColor,
                    size=15,
                    font_family="cupurum",
                ),
                width=d_width["c4"],
            ),
            el_divider,

        ],
        height=50,
        vertical_alignment=ft.CrossAxisAlignment.END,
    )





class ProductRow(ft.Row):
    def __init__(self, **kwargs):
        super().__init__()
        self.page = kwargs["page"]
        self.d_width = kwargs["d_width"]
        self.d_error_messages = kwargs["d_error_messages"]
        # self.product_id = kwargs["product_id"]                 #id продукта в БД
        # self.p_name = kwargs["p_name"]         #название категории
        # self.p_item_no = kwargs["p_item_no"]   #Артикул
        # self.p_price = kwargs["p_price"]       #цена
        # self.p_desc = kwargs["p_desc"]         #описание
        # self.p_promo_price = kwargs["p_promo_price"]   #цена по акции
        # self.p_promo_end = kwargs["p_promo_end"]       #дата окончания акции
        # self.p_promo_desc = kwargs["p_promo_desc"]     #описание акции

        self.product: Product = kwargs["product"]
        self.product_id = self.product.product_id
        self.p_name = self.product.name
        self.p_item_no = self.product.item_no
        self.p_price = self.product.price
        self.p_desc = self.product.description
        self.p_promo_price = self.product.promo_price
        self.p_promo_end = self.product.promo_expire_date
        self.p_promo_desc = self.product.promo_desc
        self.p_img = self.product.r_image.image_name if self.product.r_image else None

        self.l_elements = kwargs["l_elements"]    #ссылка на список продуктов, чтобы отсюда ее модифицировать

        # self.error_upd = ft.SnackBar(
        #     content=ft.Text('категория с таким названием уже существует'),
        #     bgcolor=inputBgErrorColor
        # )



        self.el_divider = ft.Container(
            height=25,
            width=1,
            bgcolor="white",
            margin=0,
            padding=0
        )

        _img = ft.Container(
            content=ft.Image(
                src=f"{settings.MEDIA}/original/{self.p_img}.jpeg" if self.p_img else f"{settings.MEDIA}/default/no_product_photo.jpeg",
                width=100,
                height=100,
                fit=ft.ImageFit.CONTAIN
            )
            ,padding=ft.padding.only(top=5)
        )
        self.r_img = _img
        self.r_name = self._field(text=self.p_name, width=self.d_width['c2'])
        self.r_item_no = self._field(text=self.p_item_no, width=self.d_width['c3'])
        self.r_price = self._field(text=self.p_price, width=self.d_width['c4'])
        self.r_desc = self._field(text=self.p_desc, width=self.d_width['c4'])
        self.r_promo_price = self._field(text=self.p_promo_price, width=self.d_width['c4'])
        self.r_promo_end = self._field(text=self.p_promo_end, width=self.d_width['c4'])
        self.r_promo_desc = self._field(text=self.p_promo_desc, width=self.d_width['c4'])

        self.r_content_edit = ft.Row(controls=[
            ft.Container(
                scale=0.8,
                # bgcolor="blue",
                margin=ft.margin.only(left=47),
                content=ft.IconButton(ft.icons.EDIT, on_click=self.edit)
            )
        ])

        # элемент с редактированием
        self.r_container_icon = ft.Container(
            # bgcolor="orange",
            width=self.d_width['c1'],
            # padding=ft.padding.only(right=30),
            content=self.r_content_edit
        )

        # сборка элементов в строку
        self.controls = [
            self.r_container_icon,
            self.el_divider,
            self.r_img,
            self.el_divider,
            self.r_name,
            self.el_divider,
            self.r_item_no,
            self.el_divider,
            self.r_price,
            self.el_divider,
            self.r_desc,
            self.el_divider,
            self.r_promo_price,
            self.el_divider,
            self.r_promo_end,
            self.el_divider,
            self.r_promo_desc,
            self.el_divider,
            ft.Container(
                scale=0.8,
                margin=ft.margin.only(left=0),
                content=ft.IconButton(ft.icons.DELETE, on_click=self.delete_dialog)
            ),
        ]




    def _field(self, text, width):
        return ft.Container(
            content=ft.Text(
                text,
                color=defaultFontColor,
                size=15,
                font_family="cupurum",

            ),
            # height=25,
            width=width,
            alignment=ft.alignment.bottom_left,
            #bgcolor=ft.colors.DEEP_ORANGE_800
        )


    def edit(self, e):
        v_name = self.r_name.content.value
        v_item_no = self.r_item_no.content.value
        v_price = self.r_price.content.value
        v_desc = self.r_desc.content.value
        v_promo_price = self.r_promo_price.content.value
        v_promo_end = self.r_promo_end.content.value
        v_promo_desc = self.r_promo_desc.content.value

        self.p_name = v_name
        self.p_item_no = v_item_no
        self.p_price = v_price
        self.p_desc = v_desc
        self.p_promo_price = v_promo_price
        self.p_promo_end = v_promo_end
        self.p_promo_desc = v_promo_desc


        self.r_name.content = ft.TextField(v_name, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15, max_length=300)
        self.r_item_no.content = ft.TextField(v_item_no, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)
        self.r_price.content = ft.TextField(v_price, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)
        self.r_desc.content = ft.TextField(v_desc, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15, multiline=True, max_length=1000, shift_enter=True)
        self.r_promo_price.content = ft.TextField(v_promo_price, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)
        self.r_promo_end.content = ft.TextField(v_promo_end, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)
        self.r_promo_desc.content = ft.TextField(v_promo_desc, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15, max_length=1000)

        self.r_container_icon.content = ft.Row(
            spacing=0,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            controls=[
                ft.Container(margin=ft.margin.all(0),
                             padding=ft.padding.all(0),
                             adaptive=True,
                             scale=0.8,
                             # bgcolor="red",
                             content=ft.IconButton(ft.icons.SAVE, on_click=self.save)),
                ft.Container(margin=ft.margin.only(left=0),
                             scale=0.8,
                             # bgcolor="green",
                             content=ft.IconButton(ft.icons.CANCEL, on_click=self.cancel))
            ]
        )
        self.r_container_icon.update()
        self.r_name.update()
        self.r_item_no.update()
        self.r_price.update()
        self.r_desc.update()
        self.r_promo_price.update()
        self.r_promo_end.update()
        self.r_promo_desc.update()


    def save(self, e):
        v_name = self.r_name.content.value
        v_item_no = self.r_item_no.content.value
        v_price = self._cut_price(self.r_price.content.value)
        v_desc = self.r_desc.content.value
        v_promo_price = self._cut_price(self.r_promo_price.content.value)
        v_promo_end = self.r_promo_end.content.value
        v_promo_desc = self.r_promo_desc.content.value

        flag_valid = True

        if (
                not self._is_valid_price(v_price)
                or (v_promo_price and not self._is_valid_price(v_promo_price))
                or (v_promo_end and not self._is_valid_date(v_promo_end))
        ):
            flag_valid = False

        if not flag_valid:
            error_validation = self.d_error_messages["validation_error"]
            error_validation.open = True
            error_validation.update()

        else:

            req = ReqProduct()

            d_new_values = {
                "name": v_name,
                "item_no": v_item_no,
                "price": float(v_price),
                "description": v_desc,
                "promo_price": float(v_promo_price) if v_promo_price else None,
                "promo_expire_date": v_promo_end if v_promo_end else None,
                "promo_desc": v_promo_desc
            }



            is_exists_product = req.check_product_exists(v_name, v_item_no, self.product_id)
            if is_exists_product:
                if is_exists_product == 1:
                    error_validation = self.d_error_messages["error_pk_item_no"]
                else:
                    error_validation = self.d_error_messages["error_pk_name"]
                error_validation.open = True
                error_validation.update()
            else:
                upd_res = req.update_product(self.product_id, **d_new_values)

                if upd_res is None:

                    self.r_name.content = ft.TextField(self.p_name, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)
                    self.r_item_no.content = ft.TextField(self.p_item_no, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)
                    self.r_price.content = ft.TextField(self.p_price, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)
                    self.r_desc.content = ft.TextField(self.p_desc, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)
                    self.r_promo_price.content = ft.TextField(self.p_promo_price, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)
                    self.r_promo_end.content = ft.TextField(self.p_promo_end, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)
                    self.r_promo_desc.content = ft.TextField(self.p_promo_desc, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)
                else:
                    self.r_name.content = ft.Text(v_name, color=defaultFontColor, size=15, font_family="cupurum")
                    self.r_item_no.content = ft.Text(v_item_no, color=defaultFontColor, size=15, font_family="cupurum")
                    self.r_price.content = ft.Text(v_price, color=defaultFontColor, size=15, font_family="cupurum")
                    self.r_desc.content = ft.Text(v_desc, color=defaultFontColor, size=15, font_family="cupurum")
                    self.r_promo_price.content = ft.Text(v_promo_price, color=defaultFontColor, size=15, font_family="cupurum")
                    self.r_promo_end.content = ft.Text(v_promo_end, color=defaultFontColor, size=15, font_family="cupurum")
                    self.r_promo_desc.content = ft.Text(v_promo_desc, color=defaultFontColor, size=15, font_family="cupurum")

                    self.r_container_icon.content = self.r_content_edit
                    self.r_container_icon.update()


        self.r_name.update()
        self.r_item_no.update()
        self.r_price.update()
        self.r_desc.update()
        self.r_promo_price.update()
        self.r_promo_end.update()
        self.r_promo_desc.update()


        # self.page.update()

    def cancel(self, e):
        self.r_container_icon.content = self.r_content_edit
        self.r_name.content = ft.Text(self.p_name, color=defaultFontColor, size=15, font_family="cupurum")
        self.r_item_no.content = ft.Text(self.p_item_no, color=defaultFontColor, size=15, font_family="cupurum")
        self.r_price.content = ft.Text(self.p_price, color=defaultFontColor, size=15, font_family="cupurum")
        self.r_desc.content = ft.Text(self.p_desc, color=defaultFontColor, size=15, font_family="cupurum")
        self.r_promo_price.content = ft.Text(self.p_promo_price, color=defaultFontColor, size=15, font_family="cupurum")
        self.r_promo_end.content = ft.Text(self.p_promo_end, color=defaultFontColor, size=15, font_family="cupurum")
        self.r_promo_desc.content = ft.Text(self.p_promo_desc, color=defaultFontColor, size=15, font_family="cupurum")

        self.r_container_icon.update()
        self.r_name.update()
        self.r_item_no.update()
        self.r_price.update()
        self.r_desc.update()
        self.r_promo_price.update()
        self.r_promo_end.update()
        self.r_promo_desc.update()


    def delete_dialog(self, e):
        def delete_category_handle_yes(e):
            req = ReqProduct()
            req.delete_product(self.product_id)

            for x in self.l_elements:
                if x.id == self.product_id:
                    self.l_elements.remove(x)

            dlg_delete.open = False
            self.page.update()

        def delete_category_handle_close(e):
            dlg_delete.open = False
            self.page.update()

        dlg_delete = ft.AlertDialog(
            modal=True,
            title=ft.Text("Подтверждение"),
            content=ft.Text("Вы действительно хотите удалить продукт?"),
            actions=[
                ft.TextButton("Yes", on_click=delete_category_handle_yes),
                ft.TextButton("No", on_click=delete_category_handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            # on_dismiss=lambda e: self.page.add(ft.Text("Modal dialog dismissed"),),
        )

        self.page.dialog = dlg_delete
        dlg_delete.open = True
        self.page.update()



    def _cut_price(self, price):
        price = str(price)
        if '.' in price:
            price = price.split('.')[0] + '.' + price.split('.')[1][:2]
        return price

    def _is_valid_date(self, date_str):
        formats = ["%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d", "%Y-%m-%d"]
        for fmt in formats:
            try:
                datetime.strptime(date_str, fmt)
                return True
            except ValueError:
                continue
        return False


    def _is_valid_price(self, price):
        try:
            float(price)
            return True
        except ValueError:
            return False
