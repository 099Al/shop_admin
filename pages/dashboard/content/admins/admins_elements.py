import flet as ft

from database.models.models import Admin, AdminRoles
from database.requests.req_admins import ReqAdmins
from pages.config.errors import d_error_messages
from pages.config.info_messages import snack_message_pass
from pages.config.sizes import d_admin_column_size
from pages.config.style import defaultFontColor, secondaryBgColor, textFieldColor
from utils.functions import hash_password_


class AdminRow(ft.Row):
    def __init__(self, page, admin, roles, column_with_rows, **kwargs):
        super().__init__()
        self.page = page
        self.column_with_rows = column_with_rows  # ссылка на список продуктов, чтобы отсюда ее модифицировать
        self.l_roles = roles

        self.d_column_size = d_admin_column_size
        self.d_error_messages = d_error_messages


        self.admin: Admin = admin

        self.telegram_id: str = self.admin.telegram_id
        self.telegram_name: str = self.admin.telegram_name
        self.telegram_link: str = self.admin.telegram_link
        self.name: str = self.admin.name
        self.phone: str = self.admin.phone
        self.email: str = self.admin.email
        self.role: str = self.admin.role

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
        self.r_password_reset = ft.Container(width=self.d_column_size['c_password'], alignment=ft.alignment.bottom_left)

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

        self.r_name.content = self._field(text=self.name, width=self.d_column_size['c_name'], max_lines=2)
        self.r_phone.content = self._field(text=self.phone, width=self.d_column_size['c_phone'])
        self.r_email.content = self._field(text=self.email, width=self.d_column_size['c_email'])
        self.r_telegram_name.content = self._field(text=self.telegram_name, width=self.d_column_size['c_telegram_name'])
        self.r_telegram_link.content = self._field(text=self.telegram_link, width=self.d_column_size['c_telegram_link'])
        self.r_role.content = self._field(text=(self.role).replace("_", " ").title(), width=self.d_column_size['c_role'])  #todo: error while edit name
        self.r_password_reset.content = ft.CupertinoButton(content=ft.Text("Сбросить", color=ft.Colors.WHITE, size=14), on_click=self.reset_password, width=self.d_column_size['c_password'])


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

        if (v_name != self.name or
               v_phone != self.phone or
               v_email != self.email or
               v_telegram_name != self.telegram_name or
               v_telegram_link != self.telegram_link or
               v_role != self.role
               ):


            self.name = v_name
            self.phone = v_phone
            self.email = v_email
            self.telegram_name = v_telegram_name
            self.telegram_link = v_telegram_link
            self.role = v_role

            req = ReqAdmins()
            req.update_user(
                self.telegram_id,
                name=self.name,
                phone=self.phone,
                email=self.email,
                telegram_name=self.telegram_name,
                telegram_link=self.telegram_link,
                role=self.role
            )


        self.set_read_view()
        self.page.update()




    def cancel(self, e):
        self.set_read_view()
        self.page.update()




    def delete_dialog(self, e):
        def delete_admin_handle_yes(e):
            req = ReqAdmins()
            req.delete_admin(self.telegram_id)
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
        curr_user_role = self.page.session.get('auth_role')
        SUPER_ROLE = AdminRoles.SUPER_ADMIN.value

        def _reset_password_handle_yes(e):
            if curr_user_role != SUPER_ROLE:
                curr_pass = row_0.value
                if hash_password_(curr_pass) != self.admin.password:
                    row_0.border_color = ft.Colors.RED
                    row_3.value = "Неверный текущий пароль"
                    row_3.visible = True
                    dlg_reset_password.content.update()
                    return

            new_pass = row_1.value
            confirm_pass = row_2.value
            if new_pass == confirm_pass:
                if curr_user_role != SUPER_ROLE:
                    if hash_password_(new_pass) == self.admin.password:
                        row_3.value = "Новый пароль совпадает с текущим"
                        row_3.visible = True
                        dlg_reset_password.content.update()
                        return
                req.set_password(self.telegram_id, hash_password_(new_pass))
                dlg_reset_password.open = False
                snack_message_pass.open = True
                self.page.update()
            else:
                row_2.border_color = ft.Colors.RED
                row_3.visible = True
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

        def _on_change_pass_2(e):
            row_3.visible = False
            dlg_reset_password.content.update()

        def _on_change_pass_1(e):
            row_2.border_color = ft.Colors.BLACK
            row_3.visible = False      #dlg_reset_password.content.controls[2].visible = False
            dlg_reset_password.content.update()

        def _on_change_pass_0(e):
            # row_0.border_color = ft.Colors.BLACK
            row_3.visible = False
            dlg_reset_password.content.update()

        dlg_reset_password = ft.AlertDialog(
            modal=True,
            title=ft.Text("Сброс пароля"),
            content=ft.Column(height=120, controls=[]),
            actions=[
                ft.TextButton("Yes", on_click=_reset_password_handle_yes),
                ft.TextButton("No", on_click=_reset_password_handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        row_1 = ft.TextField(label="новый пароль", password=True, on_change=_on_change_pass_1)
        row_2 = ft.TextField(label="повторите пароль", password=True, on_focus=_set_border_color_focus,
                             on_blur=_set_border_color, on_change=_on_change_pass_2)
        row_3 = ft.Text(value="Пароли не совпадают", color=ft.Colors.RED, visible=False)
        if curr_user_role == SUPER_ROLE:
            dlg_reset_password.content.controls = [
                row_1,
                row_2,
                row_3,
            ]
        else:
            row_0 = ft.TextField(label="текущий пароль", password=True, on_change=_on_change_pass_0, on_focus=_set_border_color_focus,
                             on_blur=_set_border_color)
            dlg_reset_password.content.height = 190
            dlg_reset_password.content.controls = [
                row_0,
                row_1,
                row_2,
                row_3,
            ]

        self.page.open(dlg_reset_password)
        self.page.update()


    def __repr__(self):
        return (f'{self.__class__.__name__} (id={self.telegram_id}, name={self.name}, role={self.role})')