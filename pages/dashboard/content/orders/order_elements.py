import flet as ft

from pages.config.sizes import d_order_column_size
from pages.config.style import defaultFontColor


class OrderRow(ft.Row):
    def __init__(self, page, order_info, column_with_rows, **kwargs):
        super().__init__()
        self.page = page
        self.order_info = order_info
        self.column_with_rows = column_with_rows
        self.d_column_size = d_order_column_size

        self.order_info = order_info

        self.phone = self.order_info.phone
        self.telegram_link = self.order_info.telegram_link

        self.order_id: int = self.order_info.id
        self.user_tg_id: str = self.order_info.user_tg_id
        self.order_sum: float = self.order_info.order_sum
        self.status: str = self.order_info.status
        self.payment_status: str = self.order_info.payment_status
        self.delivery_address: str = self.order_info.delivery_address
        self.created_at: str = self.order_info.created_at
        self.comment: str = self.order_info.comment
        self.order_products: str = self.order_info.order_products

        self._init_ui_components()

        self.set_read_view()

    def _init_ui_components(self):
        """Initialize all UI components"""
        # Divider element
        self.el_divider = ft.Container(
                height=self.d_column_size['el_height'],
                width=1,
                bgcolor="white",
                margin=0,
                padding=0
        )
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
        self.r_phone = ft.Container(width=self.d_column_size['phone'], alignment=ft.alignment.bottom_left)
        self.r_telegram_link = ft.Container(width=self.d_column_size['telegram_link'], alignment=ft.alignment.bottom_left)
        self.r_order_sum = ft.Container(width=self.d_column_size['order_sum'], alignment=ft.alignment.bottom_left)
        self.r_status = ft.Container(width=self.d_column_size['status'], alignment=ft.alignment.bottom_left)
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
            self.r_phone,
            self.el_divider,
            self.r_telegram_link,
            self.el_divider,
            self.r_order_sum,
            self.el_divider,
            self.r_status,
            self.el_divider,
            self.r_delivery_address,
            self.el_divider,
            self.r_created_at,
            self.el_divider,
            self.r_comment,
            self.el_divider,
            self.r_order_products,
            self.el_divider,
            self.r_delete_container,
        ]

    def set_read_view(self):
        self.r_container_icon.content = self.r_content_edit
        self.r_phone.content = self._field(self.phone, self.d_column_size['phone'])
        self.r_telegram_link.content = self._field(self.telegram_link, self.d_column_size['telegram_link'])
        self.r_order_sum.content = self._field(self.order_sum, self.d_column_size['order_sum'])
        self.r_status.content = self._field(self.status, self.d_column_size['status'])
        self.r_delivery_address.content = self._field(self.delivery_address, self.d_column_size['delivery_address'])
        self.r_created_at.content = self._field(self.created_at, self.d_column_size['created_at'])
        self.r_comment.content = self._field(self.comment, self.d_column_size['comment'])
        self.r_order_products.content = self._field(self.order_products, self.d_column_size['order_products'])

    def set_edit_view(self, e):
        pass

    def delete_dialog(self, e):
        pass
