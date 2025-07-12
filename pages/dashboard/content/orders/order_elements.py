import json
from typing import Dict

import flet as ft

from database.requests.req_orders import ReqOrders
from database.requests.req_products import ReqProduct
from pages.config.sizes import d_order_column_size
from pages.config.style import defaultFontColor, secondaryBgColor, textFieldColor


class OrderRow(ft.Row):
    def __init__(self, page, order_info, column_with_rows, l_status_options, **kwargs):
        super().__init__()
        self.page = page
        self.order_info = order_info
        self.column_with_rows = column_with_rows
        self.d_column_size = d_order_column_size
        self.l_status_options = l_status_options

        self.order_info = order_info

        self.phone = self.order_info.phone
        self.telegram_link = self.order_info.telegram_link

        self.order_id: int = self.order_info.id
        self.user_tg_id: str = self.order_info.user_tg_id
        self.order_sum: float = self.order_info.order_sum
        self.status: str = self.order_info.status
        self.payment_status: str = self.order_info.payment_status
        self.delivery_address: str = self.order_info.delivery_address
        self.created_at: str = self.order_info.created_at.strftime("%Y-%m-%d %H:%M")
        self.comment: str = self.order_info.comment
        self.order_products: Dict = {item['product_id']: item for item in json.loads(self.order_info.order_products or "[]")}

        self.d_cnt_info = {}

        # self.order_products_cnt = sum([int(x["cnt"]) for x in self.order_products.values()])

        self._init_ui_components()

        self.set_read_view()

    @property
    def order_products_cnt(self):
        return sum([int(x["cnt"]) for x in self.order_products.values()])

    def _create_divider(self, height=None):
        return ft.Container(
            height=height or self.d_column_size['el_height'],
            width=1,
            bgcolor="white",
            margin=ft.margin.only(bottom=5),
            padding=0
        )

    def _init_ui_components(self):
        self.dividers = [self._create_divider() for _ in range(11)]

        # self.el_divider = ft.Container(
        #         height=self.d_column_size['el_height'],
        #         width=1,
        #         bgcolor="white",
        #         margin=ft.margin.only(bottom=5),
        #         padding=0
        # )



        # Text containers
        self._init_attr_containers()

        # Edit button
        self._init_edit_button()

        # Delete button
        self._init_delete_button()

        # Main row controls
        self._init_compile_row()




    def _field(self, text, width, max_lines=2):
        return ft.Text(
                text,
                color=defaultFontColor,
                size=15,
                font_family="cupurum",
                width=width,
                max_lines=max_lines,
                overflow=ft.TextOverflow.FADE,  #не работает с max_lines
            )

    def _init_attr_containers(self):
        self.r_order_id = ft.Container(width=self.d_column_size['order_id'], alignment=ft.alignment.bottom_left)
        self.r_phone = ft.Container(width=self.d_column_size['phone'], alignment=ft.alignment.bottom_left)
        self.r_telegram_link = ft.Container(width=self.d_column_size['telegram_link'], alignment=ft.alignment.bottom_left)
        self.r_order_sum = ft.Container(width=self.d_column_size['order_sum'], alignment=ft.alignment.bottom_left)
        self.r_status = ft.Container(width=self.d_column_size['status'], alignment=ft.alignment.bottom_left)
        self.r_payment_status = ft.Container(width=self.d_column_size['payment_status'], alignment=ft.alignment.bottom_left)
        self.r_delivery_address = ft.Container(width=self.d_column_size['delivery_address'], alignment=ft.alignment.bottom_left)
        self.r_created_at = ft.Container(width=self.d_column_size['created_at'], alignment=ft.alignment.bottom_left)
        self.r_comment = ft.Container(width=self.d_column_size['comment'], alignment=ft.alignment.bottom_left)
        self.r_order_products = ft.Container(width=self.d_column_size['order_products'], alignment=ft.alignment.bottom_left)

    def _init_edit_button(self):
        self.r_content_edit = ft.Row(controls=[
            ft.Container(
                scale=0.8,
                # bgcolor="blue",
                margin=ft.margin.only(left=47),
                content=ft.IconButton(ft.icons.EDIT, on_click=self.set_edit_view)
            )
        ])

        # элемент с редактированием
        self.r_container_icon = ft.Container(
            # bgcolor="orange",
            width=self.d_column_size['edit'],
            content=None
        )

    def _init_delete_button(self):
        self.r_delete_container = ft.Container(
            scale=0.8,
            margin=ft.margin.only(left=0),
            padding=ft.padding.only(right=15),
            content=ft.IconButton(ft.icons.DELETE, on_click=self.delete_dialog)
        )

    def _init_compile_row(self):
        self.controls = [
            self.r_container_icon,
            self.r_order_products,
            self.dividers[0],
            self.r_phone,
            self.dividers[1],
            self.r_telegram_link,
            self.dividers[2],
            self.r_created_at,
            self.dividers[3],
            self.r_order_sum,
            self.dividers[4],
            self.r_status,
            self.dividers[5],
            self.r_payment_status,
            self.dividers[6],
            self.r_delivery_address,
            self.dividers[7],
            self.r_comment,
            self.dividers[8],
            self.r_order_id,
            self.dividers[9],
            #self.r_order_products,
            self.dividers[10],
            self.r_delete_container,
        ]

    def set_read_view(self):
        self.r_container_icon.content = self.r_content_edit
        self.r_phone.content = self._field(self.phone, self.d_column_size['phone'])
        self.r_telegram_link.content = self._field(self.telegram_link, self.d_column_size['telegram_link'])
        self.r_created_at.content = self._field(self.created_at, self.d_column_size['created_at'])
        self.r_order_sum.content = self._field(self.order_sum, self.d_column_size['order_sum'])
        self.r_status.content = self._field(self.status, self.d_column_size['status'])
        self.r_payment_status.content = self._field(self.payment_status, self.d_column_size['payment_status'])
        self.r_delivery_address.content = self._field(self.delivery_address, self.d_column_size['delivery_address'])
        self.r_comment.content = self._field(self.comment, self.d_column_size['comment'])
        self.r_order_id.content = self._field(self.order_id, self.d_column_size['order_id'])
        #self.r_order_products.content = self._field(self.order_products_cnt, self.d_column_size['order_products'])


        self.order_content_short_text = ft.Text(f"{self.order_products_cnt}", color=ft.Colors.WHITE, size=14)
        self.order_content_short = ft.Row(
               spacing=0,
               alignment=ft.MainAxisAlignment.SPACE_EVENLY,
               controls=[
                   self.order_content_short_text,
                   ft.Container(margin=ft.margin.only(left=0),
                                scale=0.8,
                                # bgcolor="green",
                                content=ft.IconButton(ft.icons.ARROW_DROP_DOWN, on_click=self.expand_order_list))
               ]
        )
        self.r_order_products.content = self.order_content_short

    def expand_order_list(self, e):

        column_item_list = ft.Column()

        product_ids = [int(x["product_id"]) for x in self.order_products.values()]
        req = ReqProduct()
        d_product_info = req.get_products_short_info_by_ids(product_ids)

        bt_1 = ft.Container(
            content=ft.Icon(ft.Icons.CHECK_CIRCLE),
            # bgcolor=ft.colors.GREEN,
            alignment=ft.alignment.center,
            height=25,
            on_click=self.save_count
        )

        column_item_list.controls.append(bt_1)

        max_lenth_info = 0
        for k, item in self.order_products.items():
            info = d_product_info[k]
            info_text = f'#{info["item_no"]}: {(info["name"])[:15]}{"..." if len(info["name"]) > 15 else ""}'      #
            info_length = len(info_text)               #возможно нет смысла использовать, лучше зафиксировать размер
            max_lenth_info = max(info_length, max_lenth_info)

            text_cnt_info = ft.TextField(item["cnt"], height=45, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=14, text_align=ft.TextAlign.CENTER)
            self.d_cnt_info[item["product_id"]] = text_cnt_info

            bt_i = ft.Container(
                    content=ft.Row(
                        controls=[
                                  ft.Container(content=ft.Text(info_text, color=ft.Colors.WHITE, size=14,text_align=ft.TextAlign.CENTER), width=150, alignment=ft.alignment.center),
                                  ft.Container(content=text_cnt_info
                                               , width=60, alignment=ft.alignment.center, padding=ft.padding.only(right=3)
                                               )
                                  ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    #width=50,#max_lenth_info * 8 + 50,
                    height=50,
                    bgcolor=ft.Colors.GREEN_400,
                    border_radius=ft.border_radius.all(2),
                    margin=0,
                    padding=0,
                    # on_click=lambda e: print("A1"),
                    alignment=ft.alignment.center
            )

            column_item_list.controls.append(bt_i)

        bt_add = ft.Container(
            content=ft.Row(controls=[ft.Icon(ft.Icons.ADD), ft.Text("Добавить", color=ft.Colors.WHITE, size=14)], alignment=ft.MainAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            height=40,
            padding=ft.padding.only(left=50),
            on_click=self.add_to_basket
        )

        column_item_list.controls.append(bt_add)

        cnt_items = len(column_item_list.controls)

        self.r_order_products.content = column_item_list
        self.r_order_products.width = 300 #max_lenth_info * 8

        #self.r_order_products.content = ft.Text(f"{self.order_products_cnt}", color=ft.Colors.WHITE, size=14)

        for div in self.dividers:
            div.height = self.d_column_size['el_height'] * (cnt_items - 2) + 25 + 40  #25 это высота крайних элементов


        self.page.update()



    def save_count(self, e):
        for k, v in self.d_cnt_info.items():
            new_value = int(v.value)
            self.order_products[k]["cnt"] = new_value


            req = ReqOrders()

            req.update_order(self.order_id, order_products=json.dumps(list(self.order_products.values())))

            self.order_content_short_text.value = f"{self.order_products_cnt}"
            self.r_order_products.content = self.order_content_short

            for div in self.dividers:
                div.height = self.d_column_size['el_height']

            self.r_order_products.width = self.d_column_size['order_products']

            self.page.update()




    def add_to_basket(self, e):

        def confirm(e):
            dlg_add_to_basket.open = False
            self.page.update()

        def cancel(e):
            dlg_add_to_basket.open = False
            self.page.update()

        def on_item_submit(e):
            product = req.get_product_by_item_no(row_1.value)
            if product:
                row_2.value = product.name
            else:
                row_2.value = ""
                row_3.value = "Товар по артикулу не найден"

            dlg_add_to_basket.content.update()

        self.flag_serch = False
        self.l_products = []
        def on_name_change(e):
            text = row_2.value
            text_ln = len(text)

            if text_ln >= 3 and not self.flag_serch:
                self.l_products = req.get_products_by_name_part(text)
                self.flag_serch = True
            if self.flag_serch and text_ln < 3:
                #Для сброса предыдущий выборки
                self.l_products = []
                self.flag_serch = False
                row_3.value = ""
                dlg_add_to_basket.content.update()

            filtered = [product for product in self.l_products if product.name.lower().startswith(text.lower())]
            if filtered:
                row_3.value = "\n".join([f"{x.name}" for x in filtered])
            elif self.flag_serch:
                row_3.value = "Товар не найден"

            dlg_add_to_basket.content.update()


        req = ReqProduct()

        dlg_add_to_basket = ft.AlertDialog(
            modal=True,
            title=ft.Text("Добавить товар"),
            content=ft.Column(height=150, controls=[]),
            actions=[
                ft.TextButton("Сохранить", on_click=confirm),
                ft.TextButton("Отмена", on_click=cancel),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        row_1 = ft.TextField(label="Артикул", on_submit=on_item_submit)
        row_2 = ft.TextField(label="Название", on_change=on_name_change)
        row_3 = ft.Text(value="Варианты", height=80, font_family="cupurum", size=12)

        dlg_add_to_basket.content.controls = [
            row_1,
            row_2,
            row_3
        ]

        self.page.open(dlg_add_to_basket)
        self.page.update()







    def set_edit_view(self, e):
        v_delivery_address = self.r_delivery_address.content.value
        v_status = self.r_status.content.value
        v_comment = self.r_comment.content.value
        v_order_products = self.r_order_products.content.value

        self.r_container_icon.content = self.r_content_edit

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

        self.r_delivery_address.content = ft.TextField(v_delivery_address, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)
        self.r_comment.content = ft.TextField(v_comment, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)
        self.r_order_products.content = ft.TextField(v_order_products, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)

        self.r_status.content = ft.TextField(v_status, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)

        self.dd_status = ft.Dropdown(
            width=self.d_column_size['status'],
            editable=False,
            border_color=textFieldColor,
            color="white",
            hint_text=v_status,
            hint_style=ft.TextStyle(font_family="cupurum", size=15, color="white"),
            menu_width=self.d_column_size['status'] * 1.5,
            options=self.l_status_options
        )

        self.r_status.content = self.dd_status

        self.page.update()

    def save(self, e):
        v_delivery_address = self.r_delivery_address.content.value
        v_status = self.r_status.content.value
        v_comment = self.r_comment.content.value
        v_order_products = self.r_order_products.content.value

        if(v_delivery_address != self.delivery_address or
                v_status != self.status or
                v_comment != self.comment or
                v_order_products != self.order_products_cnt
        ):
            self.delivery_address = v_delivery_address
            self.status = v_status
            self.comment = v_comment
            self.order_products_cnt = v_order_products

            req = ReqOrders()
            req.update_order(self.order_id,
                             delivery_address=self.delivery_address,
                             status=self.status,
                             comment=self.comment,
                             #order_products_cnt=self.order_products_cnt
                             )

            self.set_read_view()
            self.page.update()

    def cancel(self, e):
        self.set_read_view()
        self.page.update()

    def delete_dialog(self, e):
        def order_delete_handle_close(e):
            dlg_order_delete.open = False
            self.page.update()

        def order_delete_handle_yes(e):
            self.column_with_rows.controls.remove(self)
            dlg_order_delete.open = False

            req = ReqOrders()
            req.delete_order(self.order_id)

            self.page.update()


        dlg_order_delete = ft.AlertDialog(
            title=ft.Text("Подтверждение"),
            content=ft.Text("Удалить Заказ?"),
            actions=[
                ft.TextButton("Yes", on_click=order_delete_handle_yes),
                ft.TextButton("No", on_click=order_delete_handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.open(dlg_order_delete)
        self.page.update()

