import flet as ft

from database.models.models import Admin
from database.requests.req_admins import ReqAdmins
from pages.config.errors import d_error_messages
from pages.config.sizes import d_admin_column_size
from pages.config.style import defaultFontColor, secondaryBgColor, textFieldColor


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