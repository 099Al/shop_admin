import flet as ft

from database.models.models import Client, ClientsBan
from database.requests.req_clients import ReqClients
from pages.config.sizes import d_client_column_size
from pages.config.style import defaultFontColor, secondaryBgColor, textFieldColor


class ClientRow(ft.Row):
    def __init__(self, page, client, column_with_rows, l_ban_options, **kwargs):
        super().__init__()
        self.page = page
        self.column_with_rows = column_with_rows  # ссылка на список продуктов, чтобы отсюда ее модифицировать

        self.l_ban_options = l_ban_options
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
        self.r_is_banned.content = self._field(d_ban.get(self.is_banned, None), self.d_column_size['c_is_banned'])
        self.r_ban_reason.content = self._field(self.ban_reason, self.d_column_size['c_ban_reason'])


    def set_edit_view(self, e):
        v_name = self.r_name.content.value
        v_phone = self.r_phone.content.value
        v_email = self.r_email.content.value
        v_telegram_name = self.r_telegram_name.content.value
        v_telegram_link = self.r_telegram_link.content.value
        v_is_banned = self.r_is_banned.content.value
        v_ban_reason = self.r_ban_reason.content.value



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

        self.r_name.content = ft.TextField(v_name, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15, multiline=True)
        self.r_phone.content = ft.TextField(v_phone, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)
        self.r_email.content = ft.TextField(v_email, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)
        self.r_telegram_name.content = ft.TextField(v_telegram_name, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)
        self.r_telegram_link.content = ft.TextField(v_telegram_link, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)

        self.r_ban_reason.content = ft.TextField(v_ban_reason, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)

        self.dd_ban = ft.Dropdown(
            width=self.d_column_size['c_is_banned'],
            editable=False,
            border_color=textFieldColor,
            color="white",
            hint_text=v_is_banned,
            hint_style=ft.TextStyle(font_family="cupurum", size=15, color="white"),
            menu_width=self.d_column_size['c_is_banned'] * 1.5,
            # menu_height=300,
            options=self.l_ban_options

        )

        self.r_is_banned.content = self.dd_ban

        self.page.update()

    def save(self, e):
        v_name = self.r_name.content.value
        v_phone = self.r_phone.content.value
        v_email = self.r_email.content.value
        v_telegram_name = self.r_telegram_name.content.value
        v_telegram_link = self.r_telegram_link.content.value
        v_is_banned = int(self.r_is_banned.content.value)
        v_ban_reason = self.r_ban_reason.content.value

        if (v_name != self.name or
                v_phone != self.phone or
                v_email != self.email or
                v_telegram_name != self.telegram_name or
                v_telegram_link != self.telegram_link or
                v_is_banned != self.is_banned or
                v_ban_reason != self.ban_reason
        ):


            self.name = v_name
            self.phone = v_phone
            self.email = v_email
            self.telegram_name = v_telegram_name
            self.telegram_link = v_telegram_link
            self.is_banned = v_is_banned
            self.ban_reason = v_ban_reason

            req = ReqClients()

            req.update_client(self.telegram_id,
                              name=self.name,
                              phone=self.phone,
                              email=self.email,
                              telegram_name=self.telegram_name,
                              telegram_link=self.telegram_link,
                              is_banned=self.is_banned,
                              ban_reason=self.ban_reason)

            self.set_read_view()
            self.page.update()


    def cancel(self, e):
        self.set_read_view()
        self.page.update()




    def delete_dialog(self, e):
        def client_delete_handle_close(e):
            dlg_client_delete.open = False
            self.page.update()

        def client_delete_handle_yes(e):
            self.column_with_rows.controls.remove(self)
            dlg_client_delete.open = False

            req = ReqClients()
            req.delete_client(self.telegram_id)

            self.page.update()


        dlg_client_delete = ft.AlertDialog(
            title=ft.Text("Подтверждение"),
            content=ft.Text("Удалить этого клиента?"),
            actions=[
                ft.TextButton("Yes", on_click=client_delete_handle_yes),
                ft.TextButton("No", on_click=client_delete_handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.open(dlg_client_delete)
        self.page.update()
