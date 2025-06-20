import flet as ft

from database.models.models import Admin
from database.requests.req_admins import ReqAdmins
from pages.config.errors import d_error_messages
from pages.config.info_messages import snack_message_pass
from pages.config.sizes import d_admin_column_size
from pages.config.style import defaultFontColor, secondaryBgColor, textFieldColor
from pages.dashboard.content.sort_header import SortHeader
from utils.functions import hash_password_


class AdminHeader(ft.Row):
    def __init__(self, page, rows_controls, **kwargs):
        super().__init__()
        self.page = page
        self.rows_controls: list[AdminRow] = rows_controls  # ссылка на список
        self.d_column_size = d_admin_column_size

        self.el_divider = ft.Container(
            height=25,
            width=1,
            bgcolor="white",
            margin=0,
            padding=0
        )


    def build(self):

        sort_headers = []

        def _reset_all_sort_headers_except(active_header):
            for hdr in sort_headers:
                if hdr != active_header:
                    hdr.reset_sort()

        sort_telegram = SortHeader(self.page, self.rows_controls, default_sort_key='admin_telegram_id', sort_key_type=int, sort_key_reverse=False, reset_others_callback=_reset_all_sort_headers_except)
        sort_role = SortHeader(self.page, self.rows_controls, default_sort_key='admin_telegram_id', sort_key_type=int, sort_key_reverse=False, reset_others_callback=_reset_all_sort_headers_except)
        sort_phone = SortHeader(self.page, self.rows_controls, default_sort_key='admin_telegram_id', sort_key_type=int, sort_key_reverse=False, reset_others_callback=_reset_all_sort_headers_except)
        sort_name = SortHeader(self.page, self.rows_controls, default_sort_key='admin_telegram_id', sort_key_type=int, sort_key_reverse=False, reset_others_callback=_reset_all_sort_headers_except)

        sort_headers.append(sort_telegram)
        sort_headers.append(sort_role)
        sort_headers.append(sort_phone)
        sort_headers.append(sort_name)

        header_controls = [
            ft.Container(
                width=self.d_column_size["c_edit"],
            ),
            self.el_divider,
            sort_telegram.attribute_header_with_sort("Telegram", self.d_column_size["c_telegram_name"], str, 'admin_telegram_name'),
            self.el_divider,
            sort_role.attribute_header_with_sort("Role", self.d_column_size["c_role"], str, 'admin_role'),
            self.el_divider,
            sort_phone.attribute_header_with_sort("Телефон", self.d_column_size["c_phone"], str, 'admin_phone'),
            self.el_divider,
            self._create_header_cell("Email", self.d_column_size["c_email"]),
            self.el_divider,
            sort_name.attribute_header_with_sort("Имя", self.d_column_size["c_name"], str, 'admin_name'),
            self.el_divider,
            self._create_header_cell("Telegram Link", self.d_column_size["c_telegram_link"]),
            self.el_divider,
            self._create_header_cell("Пароль", self.d_column_size["c_reset_password"]),
        ]

        return ft.Row(
            controls=header_controls,
            height=50,
            vertical_alignment=ft.CrossAxisAlignment.END
        )

    def _create_header_cell(self, text, width, visible=True):
        return ft.Container(
            content=ft.Text(
                text,
                color=defaultFontColor,
                size=15,
                font_family="cupurum",
            ),
            width=width,
            alignment=ft.alignment.bottom_left,
            visible=visible
        )


class AdminRow(ft.Row):
    def __init__(self, page, admin, roles, column_with_rows, **kwargs):
        super().__init__()
        self.page = page
        self.column_with_rows = column_with_rows  # ссылка на список продуктов, чтобы отсюда ее модифицировать
        self.l_roles = roles

        self.d_column_size = d_admin_column_size
        self.d_error_messages = d_error_messages


        self.admin: Admin = admin

        self.admin_telegram_id: str = self.admin.telegram_id
        self.admin_telegram_name: str = self.admin.telegram_name
        self.admin_telegram_link: str = self.admin.telegram_link
        self.admin_name: str = self.admin.name
        self.admin_phone: str = self.admin.phone
        self.admin_email: str = self.admin.email
        self.admin_role: str = self.admin.role

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
        self.r_role = ft.Container(width=self.d_column_size['c_role'], alignment=ft.alignment.bottom_left)
        self.r_password_reset = ft.Container(width=self.d_column_size['c_reset_password'], alignment=ft.alignment.bottom_left)

    def _init_edit_button(self):
        self.r_content_edit = ft.Row(controls=[
            ft.Container(
                scale=0.8,
                # bgcolor="blue",
                margin=ft.margin.only(left=47),
                content=ft.IconButton(ft.icons.EDIT, on_click=self.edit)
            )
        ])

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
        # сборка элементов в строку
        self.controls = [
            self.r_container_icon,
            ft.Container(
                content=ft.Row(
                    controls=[
                self.el_divider,
                self.r_telegram_name,
                self.el_divider,
                self.r_role,
                self.el_divider,
                self.r_phone,
                self.el_divider,
                self.r_email,
                self.el_divider,
                self.r_name,
                self.el_divider,
                self.r_telegram_link,
                self.el_divider,
                self.r_password_reset
        ]
                ),
                border=ft.border.only(bottom=ft.border.BorderSide(0.1, "white")),

            ),
            self.r_delete_container,
        ]

    def set_read_view(self):
        self.r_container_icon.content = self.r_content_edit

        self.r_name.content = self._field(text=self.admin_name, width=self.d_column_size['c_name'], max_lines=2)
        self.r_phone.content = self._field(text=self.admin_phone, width=self.d_column_size['c_phone'])
        self.r_email.content = self._field(text=self.admin_email, width=self.d_column_size['c_email'])
        self.r_telegram_name.content = self._field(text=self.admin_telegram_name, width=self.d_column_size['c_telegram_name'])
        self.r_telegram_link.content = self._field(text=self.admin_telegram_link, width=self.d_column_size['c_telegram_link'])
        self.r_role.content = self._field(text=self.admin_role, width=self.d_column_size['c_role'])
        self.r_password_reset.content = ft.CupertinoButton(content=ft.Text("Сбросить", color=ft.Colors.WHITE, size=14), on_click=self.reset_password, width=self.d_column_size['c_reset_password'])


    def edit(self, e):
        v_name = self.r_name.content.value
        v_phone = self.r_phone.content.value
        v_email = self.r_email.content.value
        v_telegram_name = self.r_telegram_name.content.value
        v_telegram_link = self.r_telegram_link.content.value
        v_role = self.r_role.content.value


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

        self.dd_menu = ft.Dropdown(
            width=self.d_column_size['c_role'],
            editable=False,
            border_color=textFieldColor,
            color="white",
            hint_text=v_role,
            hint_style=ft.TextStyle(font_family="cupurum", size=15, color="white"),
            menu_width=self.d_column_size['c_role']*1.5,
            #menu_height=300,
            options=self.l_roles

        )

        self.r_role.content = self.dd_menu
        #self.r_role.content = ft.TextField(v_role, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)


        self.page.update()

    def save(self, e):

        v_name = self.r_name.content.value
        v_phone = self.r_phone.content.value
        v_email = self.r_email.content.value
        v_telegram_name = self.r_telegram_name.content.value
        v_telegram_link = self.r_telegram_link.content.value
        v_role = self.r_role.content.value

        if (v_name != self.admin_name or
               v_phone != self.admin_phone or
               v_email != self.admin_email or
               v_telegram_name != self.admin_telegram_name or
               v_telegram_link != self.admin_telegram_link or
               v_role != self.admin_role
               ):


            self.admin_name = v_name
            self.admin_phone = v_phone
            self.admin_email = v_email
            self.admin_telegram_name = v_telegram_name
            self.admin_telegram_link = v_telegram_link
            self.admin_role = v_role

            req = ReqAdmins()
            req.update_user(
                self.admin_telegram_id,
                name=self.admin_name,
                phone=self.admin_phone,
                email=self.admin_email,
                telegram_name=self.admin_telegram_name,
                telegram_link=self.admin_telegram_link,
                role=self.admin_role
            )


        self.set_read_view()
        self.page.update()




    def cancel(self, e):
        self.set_read_view()
        self.page.update()




    def delete_dialog(self, e):
        def delete_admin_handle_yes(e):
            req = ReqAdmins()
            req.delete_admin(self.admin_telegram_id)
            self.column_with_rows.controls.remove(self)
            dlg_delete.open = False
            self.page.update()

        def delete_admin_handle_close(e):
            dlg_delete.open = False
            self.page.update()

        dlg_delete = ft.AlertDialog(
            modal=True,
            title=ft.Text("Подтверждение"),
            content=ft.Text("Удалить пользователя из администратороров?"),
            actions=[
                ft.TextButton("Yes", on_click=delete_admin_handle_yes),
                ft.TextButton("No", on_click=delete_admin_handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.open(dlg_delete)
        self.page.update()

    def reset_password(self, e):
        req = ReqAdmins()
        # role = page.session.get('auth_role')
        # if role == 'super_admin':

        def _reset_password_handle_yes(e):
            new_pass = dlg_reset_password.content.controls[0].value
            confirm_pass = dlg_reset_password.content.controls[1].value
            if new_pass == confirm_pass:
                req.set_password(self.admin_telegram_id,  hash_password_(new_pass))
                dlg_reset_password.open = False
                snack_message_pass.open = True
                self.page.update()

            else:
                dlg_reset_password.content.controls[1].border_color = ft.Colors.RED
                dlg_reset_password.content.controls[2].visible = True
                dlg_reset_password.content.update()

        def _reset_password_handle_close(e):
            dlg_reset_password.open = False
            self.page.update()


        def _set_border_color_focus(e):
            e.control.border_color = ft.Colors.PRIMARY
            e.control.update()

        def _set_border_color(e):
            e.control.border_color = ft.Colors.BLACK
            e.control.update()

        def _close_message(e):
            dlg_reset_password.content.controls[2].visible = False
            dlg_reset_password.content.update()

        def _close_message_1(e):
            dlg_reset_password.content.controls[1].border_color = ft.Colors.BLACK
            dlg_reset_password.content.controls[2].visible = False
            dlg_reset_password.content.update()



        dlg_reset_password = ft.AlertDialog(
            modal=True,
            title=ft.Text("Сброс пароля"),
            content=ft.Column(
                controls=[
                ft.TextField(label="новый пароль", password=True, on_change=_close_message_1),
                ft.TextField(label="повторите пароль", password=True, on_focus=_set_border_color_focus, on_blur=_set_border_color, on_change=_close_message),
                ft.Text(value="Пароли не совпадают", color=ft.Colors.RED, visible=False),
            ],
            height=120,
            ),
            actions=[
                ft.TextButton("Yes", on_click=_reset_password_handle_yes),
                ft.TextButton("No", on_click=_reset_password_handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.open(dlg_reset_password)
        self.page.update()


    def __repr__(self):
        return (f'{self.__class__.__name__} (id={self.admin_telegram_id}, name={self.admin_name}, role={self.admin_role})')