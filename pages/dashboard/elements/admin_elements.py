import flet as ft

from database.connect import DataBase
from database.requests.req_admins import ReqAdmins
from pages.config.style import *


class AdminRow(ft.Row):
    def __init__(self, **kwargs):
        super().__init__()
        self.page = kwargs["page"]
        #self.error_message = kwargs["error_message"]
        self.telegram_id = kwargs["telegram_id"]

        self.role = kwargs["role"]
        self.name = kwargs["name"]
        self.phone = kwargs["phone"]
        self.email = kwargs["email"]
        self.login = kwargs["login"]

        self.d_width = kwargs["d_width"]

        self.l_elements = kwargs["l_elements"]

        self.el_divider = ft.Container(
            height=25,
            width=1,
            bgcolor="white",
            margin=0,
            padding=0
        )

        self.r_content_edit = ft.Row(controls=[
            ft.Container(
                scale=0.8,
                # bgcolor="blue",
                margin=ft.margin.only(left=47),
                content=ft.IconButton(ft.icons.EDIT, on_click=self.edit)
            )
        ])

        self.r_container_icon = ft.Container(
            width=80,
            content=self.r_content_edit
        )

        self.r_content_delete = ft.Container(
            scale=0.8,
            margin=ft.margin.only(left=0),
            content=ft.IconButton(ft.icons.DELETE, on_click=self.delete_dialog)
        )


        self.r_telegram_id = self.f_field(text=self.telegram_id, width=self.d_width['telegram_id'])
        self.r_role = self.f_field(text=self.role, width=self.d_width['role'])
        self.r_name = self.f_field(text=self.name, width=self.d_width['name'])
        self.r_phone = self.f_field(text=self.phone, width=self.d_width['phone'])
        self.r_email = self.f_field(text=self.email, width=self.d_width['email'])
        self.r_login = self.f_field(text=self.login, width=self.d_width['login'])

        self.controls = [
            self.r_container_icon,
            self.el_divider,
            self.r_telegram_id,
            self.el_divider,
            self.r_role,
            self.el_divider,
            self.r_name,
            self.el_divider,
            self.r_phone,
            self.el_divider,
            self.r_email,
            self.el_divider,
            self.r_login,
            self.el_divider,
            self.r_content_delete
        ]


    def f_field(self, text, width):
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

    def resize(self, d_width):
        self.r_telegram_id.width = d_width["telegram_id"]
        self.r_role.width = d_width["role"]
        self.r_name.width = d_width["name"]
        self.r_phone.width = d_width["phone"]
        self.r_email.width = d_width["email"]
        self.r_login.width = d_width["login"]

    def edit(self, e):
        v_text = self.r_name.content.value
        # self.category_text = v_text  # save text
        self.p_name = v_text
        self.r_name.content = ft.TextField(v_text, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor,
                                           text_size=15)

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

    def delete_dialog(self, e):
        def delete_category_handle_yes(e):
            db = DataBase()
            req = ReqAdmins(db)
            req.delete_admin(self.telegram_id)

            for x in self.l_elements:
                if x.telegram_id == self.telegram_id:
                    self.l_elements.remove(x)

            dlg_delete.open = False
            self.page.update()

        def delete_category_handle_close(e):
            dlg_delete.open = False
            self.page.update()

        dlg_delete = ft.AlertDialog(
            modal=True,
            title=ft.Text("Подтверждение"),
            content=ft.Text("Вы действительно хотите удалить пользователя?"),
            actions=[
                ft.TextButton("Yes", on_click=delete_category_handle_yes),
                ft.TextButton("No", on_click=delete_category_handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = dlg_delete
        dlg_delete.open = True
        self.page.update()

    def save(self, e):
        pass

    def cancel(self, e):
        self.r_container_icon.content = self.r_content_edit
        self.r_name.content = ft.Text(self.p_name, color=defaultFontColor, size=15, font_family="cupurum")
        self.r_container_icon.update()
        self.r_name.update()

class AdminHeader():
    def __init__(self, letter_size):
        super().__init__()

        self.w_letter = letter_size

        self.el_divider = ft.Container(
            height=25,
            width=1,
            bgcolor="white",
            margin=0,
            padding=0
        )

        self.d_headers = {
            "telegram_id": 1*self.w_letter,
            "role": 4*self.w_letter,
            "name": 4*self.w_letter,
            "phone": 5*self.w_letter,
            "email": 5*self.w_letter,
            "login": 5*self.w_letter,
        }


    def header_size(self):
        return self.d_headers

    def f_field(self, text, width):
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
    def build(self):

        l_cotrols = [ft.Container(width=80,)]
        for k, v in self.d_headers.items():
            l_cotrols.append(self.el_divider)
            l_cotrols.append(self.f_field(text=k, width=v))
        l_cotrols.append(self.el_divider)

        return ft.Row(
            controls=l_cotrols,
            height=50,
            vertical_alignment=ft.CrossAxisAlignment.END,
        )

    def resize(self, d_width):
        self.d_headers["telegram_id"] = d_width["telegram_id"]
        self.d_headers["role"] = d_width["role"]
        self.d_headers["name"] = d_width["name"]
        self.d_headers["phone"] = d_width["phone"]
        self.d_headers["email"] = d_width["email"]
        self.d_headers["login"] = d_width["login"]
