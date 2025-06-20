import flet as ft

from database.models.models import Client, ClientsBan
from pages.config.sizes import d_client_column_size
from pages.config.style import defaultFontColor


class ClientRow(ft.Row):
    def __init__(self, page, client, column_with_rows, **kwargs):
        super().__init__()
        self.page = page
        self.column_with_rows = column_with_rows  # ссылка на список продуктов, чтобы отсюда ее модифицировать

        self.d_column_size = d_client_column_size
        #self.d_error_messages = d_error_messages


        self.client: Client = client

        self.telegram_id: str = self.client.telegram_id
        self.telegram_name: str = self.client.telegram_name
        self.telegram_link: str = self.client.telegram_link
        self.name: str = self.client.name
        self.phone: str = self.client.phone
        self.email: str = self.client.email
        self.is_banned: int = self.client.is_banned  #значения из db
        self.ban_reason: str = self.client.ban_reason

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
        self.r_name = ft.Container(width=self.d_column_size['c_name'], alignment=ft.alignment.bottom_left)
        self.r_phone = ft.Container(width=self.d_column_size['c_phone'], alignment=ft.alignment.bottom_left)
        self.r_email = ft.Container(width=self.d_column_size['c_email'], alignment=ft.alignment.bottom_left)
        self.r_telegram_name = ft.Container(width=self.d_column_size['c_telegram_name'], alignment=ft.alignment.bottom_left)
        self.r_telegram_link = ft.Container(width=self.d_column_size['c_telegram_link'], alignment=ft.alignment.bottom_left)
        self.r_is_banned = ft.Container(width=self.d_column_size['c_is_banned'], alignment=ft.alignment.bottom_left)
        self.r_ban_reason = ft.Container(width=self.d_column_size['c_ban_reason'], alignment=ft.alignment.bottom_left)

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
            width=self.d_column_size['c_edit'],
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
            self.el_divider,
            self.r_name,
            self.el_divider,
            self.r_phone,
            self.el_divider,
            self.r_email,
            self.el_divider,
            self.r_telegram_name,
            self.el_divider,
            self.r_telegram_link,
            self.el_divider,
            self.r_is_banned,
            self.el_divider,
            self.r_ban_reason,
            self.el_divider,
            self.r_delete_container,
        ]


    def set_read_view(self):

        d_ban = {1: "Бан", 0: None}

        self.r_container_icon.content = self.r_content_edit

        self.r_name.content = self._field(self.name, self.d_column_size['c_name'])
        self.r_phone.content = self._field(self.phone, self.d_column_size['c_phone'])
        self.r_email.content = self._field(self.email, self.d_column_size['c_email'])
        self.r_telegram_name.content = self._field(self.telegram_name, self.d_column_size['c_telegram_name'])
        self.r_telegram_link.content = self._field(self.telegram_link, self.d_column_size['c_telegram_link'])
        self.r_is_banned.content = self._field(d_ban[self.is_banned], self.d_column_size['c_is_banned'])
        self.r_ban_reason.content = self._field(self.ban_reason, self.d_column_size['c_ban_reason'])


    def set_edit_view(self, e):
        self.r_container_icon.content = self.r_content_edit

    def delete_dialog(self, e):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Подтвердите удаление"),
            content=ft.Text("Вы уверены, что хотите удалить этого клиента?"),
            actions=[
                ft.TextButton("Отменить", on_click=self.cancel_delete),
                ft.TextButton("Удалить", on_click=self.delete),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog.open = True
        self.page.update()

    def cancel_delete(self, e):
        self.page.dialog.open = False
        self.page.update()

    def delete(self, e):
        self.column_with_rows.controls.remove(self)
        self.page.dialog.open = False